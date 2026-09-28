"""Motor de IA (alta qualidade): inswapper_128 + ArcFace (w600k_r50).

É o mesmo modelo usado por Roop, FaceFusion, ReActor e Deep-Live-Cam.
Implementado direto com onnxruntime (sem depender da lib `insightface`).

Arquivos necessários na pasta `models/` (rode `python baixar_modelos.py`):
  - inswapper_128.onnx   (~530 MB)
  - w600k_r50.onnx       (~170 MB, faz parte do pacote buffalo_l)

Licença dos modelos: InsightFace — uso NÃO comercial / pesquisa.
"""
from __future__ import annotations

import os
from pathlib import Path

import cv2
import numpy as np

from .landmarks import five_points

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
INSWAPPER = MODELS_DIR / "inswapper_128.onnx"
ARCFACE = MODELS_DIR / "w600k_r50.onnx"

ARCFACE_DST = np.array([[38.2946, 51.6963], [73.5318, 51.5014], [56.0252, 71.7366],
                        [41.5493, 92.3655], [70.7299, 92.2041]], dtype=np.float32)


def ai_available() -> bool:
    return INSWAPPER.exists() and ARCFACE.exists()


def _estimate_norm(kps: np.ndarray, size: int) -> np.ndarray:
    if size % 112 == 0:
        ratio, dx = size / 112.0, 0.0
    else:
        ratio, dx = size / 128.0, 8.0 * size / 128.0
    dst = ARCFACE_DST * ratio
    dst[:, 0] += dx
    M, _ = cv2.estimateAffinePartial2D(kps.astype(np.float32), dst, method=cv2.LMEDS)
    return M


def _session(path: Path):
    import onnxruntime as ort
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = max(1, os.cpu_count() or 1)
    providers = [p for p in ("CUDAExecutionProvider", "CoreMLExecutionProvider",
                             "CPUExecutionProvider") if p in ort.get_available_providers()]
    return ort.InferenceSession(str(path), sess_options=opts, providers=providers)


class AISwapper:
    name = "ia"

    def __init__(self, source_bgr: np.ndarray, source_landmarks: np.ndarray, **_):
        if not ai_available():
            raise FileNotFoundError(
                "Modelos de IA não encontrados em models/. Rode: python baixar_modelos.py")
        import onnx
        from onnx import numpy_helper

        model = onnx.load(str(INSWAPPER))
        self.emap = numpy_helper.to_array(model.graph.initializer[-1])
        del model
        self.swap_sess = _session(INSWAPPER)
        self.swap_inputs = [i.name for i in self.swap_sess.get_inputs()]
        self.swap_out = self.swap_sess.get_outputs()[0].name

        arc = _session(ARCFACE)
        kps = five_points(source_landmarks)
        M = _estimate_norm(kps, 112)
        aligned = cv2.warpAffine(source_bgr, M, (112, 112), borderValue=0.0)
        blob = cv2.dnn.blobFromImage(aligned, 1.0 / 127.5, (112, 112),
                                     (127.5, 127.5, 127.5), swapRB=True)
        emb = arc.run(None, {arc.get_inputs()[0].name: blob})[0].reshape(-1)
        emb = emb / np.linalg.norm(emb)
        latent = emb.reshape(1, -1) @ self.emap
        self.latent = (latent / np.linalg.norm(latent)).astype(np.float32)

    def swap_face(self, frame: np.ndarray, dst_landmarks: np.ndarray, face_id: int = 0) -> np.ndarray:
        kps = five_points(dst_landmarks)
        M = _estimate_norm(kps, 128)
        aimg = cv2.warpAffine(frame, M, (128, 128), borderValue=0.0)
        blob = cv2.dnn.blobFromImage(aimg, 1.0 / 255.0, (128, 128), (0, 0, 0), swapRB=True)
        pred = self.swap_sess.run([self.swap_out], {self.swap_inputs[0]: blob,
                                                    self.swap_inputs[1]: self.latent})[0]
        fake = np.clip(255 * pred.transpose(0, 2, 3, 1)[0], 0, 255).astype(np.uint8)[:, :, ::-1]

        h, w = frame.shape[:2]
        IM = cv2.invertAffineTransform(M)
        fake_full = cv2.warpAffine(fake, IM, (w, h), borderValue=0.0)
        white = cv2.warpAffine(np.full((128, 128), 255, np.float32), IM, (w, h), borderValue=0.0)
        white[white > 20] = 255
        ys, xs = np.where(white == 255)
        if len(xs) == 0:
            return frame
        size = int(np.sqrt((ys.max() - ys.min()) * (xs.max() - xs.min())))
        k = max(size // 10, 10)
        mask = cv2.erode(white, np.ones((k, k), np.uint8), iterations=1)
        k = max(size // 20, 5)
        mask = cv2.GaussianBlur(mask, (2 * k + 1, 2 * k + 1), 0) / 255.0
        mask = mask[..., None]
        return (mask * fake_full + (1 - mask) * frame).astype(np.uint8)
