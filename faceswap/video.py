"""Pipeline de vídeo: lê o vídeo, troca os rostos quadro a quadro e
gera um MP4 (H.264) com o áudio original preservado."""
from __future__ import annotations

import subprocess
import time
from typing import Callable

import cv2
import imageio_ffmpeg
import numpy as np

from .ai_swapper import AISwapper, ai_available
from .classic import ClassicSwapper
from .landmarks import FaceLandmarker, detect_single

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


class NoFaceError(RuntimeError):
    pass


def load_image(path: str) -> np.ndarray:
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Não consegui abrir a imagem: {path}")
    return img


def build_swapper(source_bgr: np.ndarray, engine: str = "auto", blend: str = "seamless"):
    lm = detect_single(source_bgr)
    if lm is None:
        raise NoFaceError("Nenhum rosto encontrado na FOTO enviada. Use uma foto de frente, nítida.")
    if engine == "auto":
        engine = "ia" if ai_available() else "classico"
    if engine == "ia":
        return AISwapper(source_bgr, lm)
    return ClassicSwapper(source_bgr, lm, blend=blend)


class _Smoother:
    """Suaviza os pontos no tempo (reduz tremedeira)."""

    def __init__(self, alpha: float = 0.55):
        self.alpha = alpha
        self.prev: list[np.ndarray] = []

    def __call__(self, faces: list[np.ndarray]) -> list[np.ndarray]:
        out = []
        for f in faces:
            c = f.mean(0)
            best, bd = None, 1e9
            for p in self.prev:
                d = np.linalg.norm(p.mean(0) - c)
                if d < bd:
                    best, bd = p, d
            size = np.ptp(f[:, 0]) + 1
            if best is not None and bd < size * 0.3:
                # movimento grande -> segue rápido; pequeno -> suaviza mais
                move = np.abs(f - best).mean() / size
                a = np.clip(self.alpha + move * 8, self.alpha, 1.0)
                f = a * f + (1 - a) * best
            out.append(f)
        self.prev = out
        return out


def process_video(video_path: str, image_path: str, out_path: str, engine: str = "auto",
                  blend: str = "seamless", all_faces: bool = True, max_side: int = 720,
                  max_seconds: float | None = None,
                  progress: Callable[[float, str], None] | None = None) -> dict:
    progress = progress or (lambda p, m: None)
    t0 = time.time()
    src = load_image(image_path)
    swapper = build_swapper(src, engine, blend)
    progress(0.01, f"Rosto da foto encontrado. Motor: {swapper.name}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Não consegui abrir o vídeo.")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    if fps <= 1 or fps > 120:
        fps = 25.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    scale = min(1.0, max_side / max(W, H)) if max_side else 1.0
    ow, oh = int(W * scale) // 2 * 2, int(H * scale) // 2 * 2
    limit = int(max_seconds * fps) if max_seconds else None
    if limit and total:
        total = min(total, limit)

    cmd = [FFMPEG, "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{ow}x{oh}", "-r", f"{fps:.6f}", "-i", "-",
           "-i", video_path, "-map", "0:v:0", "-map", "1:a:0?",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    landmarker = FaceLandmarker(max_faces=4 if all_faces else 1, video_mode=True)
    smoother = _Smoother()
    n = swapped = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok or (limit and n >= limit):
                break
            if scale != 1.0 or frame.shape[1] != ow or frame.shape[0] != oh:
                frame = cv2.resize(frame, (ow, oh), interpolation=cv2.INTER_AREA)
            faces = smoother(landmarker.detect(frame))
            if not all_faces and len(faces) > 1:
                faces = [max(faces, key=lambda f: np.ptp(f[:, 0]) * np.ptp(f[:, 1]))]
            for i, f in enumerate(faces):
                frame = swapper.swap_face(frame, f, face_id=i)
            if faces:
                swapped += 1
            proc.stdin.write(frame.tobytes())
            n += 1
            if n % 5 == 0:
                el = time.time() - t0
                p = n / total if total else 0.5
                eta = (el / max(p, 1e-3)) - el if total else 0
                progress(min(0.99, 0.02 + 0.97 * p),
                         f"Quadro {n}/{total or '?'} · {n / el:.1f} q/s · faltam ~{int(eta)}s")
    finally:
        cap.release()
        landmarker.close()
        try:
            proc.stdin.close()
        except Exception:
            pass
        err = proc.stderr.read().decode(errors="ignore")
        proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg falhou: {err[-500:]}")
    if n == 0:
        raise ValueError("O vídeo não tem quadros legíveis.")
    if swapped == 0:
        raise NoFaceError("Nenhum rosto foi encontrado no VÍDEO.")
    info = {"frames": n, "frames_with_face": swapped, "fps": fps, "size": f"{ow}x{oh}",
            "engine": swapper.name, "seconds": round(time.time() - t0, 1)}
    progress(1.0, "Pronto!")
    return info


def preview_frame(video_path: str, image_path: str, engine: str = "auto", blend: str = "seamless",
                  at: float = 0.3, max_side: int = 720) -> np.ndarray:
    """Troca o rosto em um único quadro (pré-visualização rápida)."""
    src = load_image(image_path)
    swapper = build_swapper(src, engine, blend)
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(total * at))
    ok, frame = cap.read()
    cap.release()
    if not ok:
        raise ValueError("Não consegui ler o vídeo.")
    s = min(1.0, max_side / max(frame.shape[:2]))
    if s < 1:
        frame = cv2.resize(frame, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    lm = FaceLandmarker(video_mode=False)
    try:
        faces = lm.detect(frame)
    finally:
        lm.close()
    if not faces:
        raise NoFaceError("Nenhum rosto nesse quadro do vídeo.")
    for i, f in enumerate(faces):
        frame = swapper.swap_face(frame, f, i)
    return frame
