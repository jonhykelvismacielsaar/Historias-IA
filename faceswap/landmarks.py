"""Detecção de rostos e pontos faciais (478 pontos) usando MediaPipe.

Funciona 100% em CPU e os modelos já vêm dentro do pacote `mediapipe`,
então não precisa baixar nada extra.
"""
from __future__ import annotations

import os

os.environ.setdefault("GLOG_minloglevel", "2")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import cv2
import mediapipe as mp
import numpy as np

_fm = mp.solutions.face_mesh

# Índices úteis da malha do MediaPipe
FACE_OVAL = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365,
             379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93,
             234, 127, 162, 21, 54, 103, 67, 109]
INNER_LIPS = [78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308,
              324, 318, 402, 317, 14, 87, 178, 88, 95]
OUTER_LIPS = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291,
              375, 321, 405, 314, 17, 84, 181, 91, 146]
LEFT_EYE = [33, 246, 161, 160, 159, 158, 157, 173, 133, 155, 154, 153, 145, 144, 163, 7]
RIGHT_EYE = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]


def five_points(lm: np.ndarray) -> np.ndarray:
    """5 pontos no padrão ArcFace/InsightFace: olho esq., olho dir., nariz,
    canto esq. da boca, canto dir. da boca (esquerda/direita da imagem)."""
    if lm.shape[0] >= 478:  # com íris refinada
        le, re_ = lm[468], lm[473]
    else:
        le, re_ = lm[LEFT_EYE].mean(0), lm[RIGHT_EYE].mean(0)
    return np.array([le, re_, lm[1], lm[61], lm[291]], dtype=np.float32)


class FaceLandmarker:
    """Encontra todos os rostos de um quadro e devolve os pontos em pixels."""

    def __init__(self, max_faces: int = 4, video_mode: bool = True, min_conf: float = 0.4):
        self.max_faces = max_faces
        self.mesh = _fm.FaceMesh(static_image_mode=not video_mode, max_num_faces=max_faces,
                                 refine_landmarks=True, min_detection_confidence=min_conf,
                                 min_tracking_confidence=0.5)
        # Para rostos pequenos/longe da câmera (fallback)
        self.static_mesh = _fm.FaceMesh(static_image_mode=True, max_num_faces=1,
                                        refine_landmarks=True, min_detection_confidence=min_conf)
        self.detector = mp.solutions.face_detection.FaceDetection(model_selection=1,
                                                                  min_detection_confidence=min_conf)

    def close(self):
        for m in (self.mesh, self.static_mesh, self.detector):
            try:
                m.close()
            except Exception:
                pass

    @staticmethod
    def _to_px(face_lms, w, h, ox=0, oy=0):
        return np.array([(p.x * w + ox, p.y * h + oy) for p in face_lms.landmark], dtype=np.float32)

    def detect(self, bgr: np.ndarray) -> list[np.ndarray]:
        h, w = bgr.shape[:2]
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        res = self.mesh.process(rgb)
        faces = []
        if res.multi_face_landmarks:
            faces = [self._to_px(f, w, h) for f in res.multi_face_landmarks]
        if faces:
            return faces

        # Fallback: detector de longo alcance + malha no recorte ampliado
        det = self.detector.process(rgb)
        if not det.detections:
            return []
        for d in det.detections[: self.max_faces]:
            bb = d.location_data.relative_bounding_box
            cx, cy = (bb.xmin + bb.width / 2) * w, (bb.ymin + bb.height / 2) * h
            size = max(bb.width * w, bb.height * h) * 2.0
            x0, y0 = int(max(0, cx - size / 2)), int(max(0, cy - size / 2))
            x1, y1 = int(min(w, cx + size / 2)), int(min(h, cy + size / 2))
            crop = rgb[y0:y1, x0:x1]
            if crop.size == 0:
                continue
            scale = 1.0
            if max(crop.shape[:2]) < 256:  # amplia rostos muito pequenos
                scale = 256 / max(crop.shape[:2])
                crop = cv2.resize(crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            r = self.static_mesh.process(np.ascontiguousarray(crop))
            if r.multi_face_landmarks:
                ch, cw = crop.shape[:2]
                pts = self._to_px(r.multi_face_landmarks[0], cw, ch) / scale
                pts[:, 0] += x0
                pts[:, 1] += y0
                faces.append(pts)
        return faces


def detect_single(bgr: np.ndarray) -> np.ndarray | None:
    """Maior rosto de uma foto (usado para a imagem de origem)."""
    lm = FaceLandmarker(max_faces=4, video_mode=False)
    try:
        faces = lm.detect(bgr)
    finally:
        lm.close()
    if not faces:
        return None
    return max(faces, key=lambda f: np.ptp(f[:, 0]) * np.ptp(f[:, 1]))
