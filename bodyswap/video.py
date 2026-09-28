"""Troca do CORPO INTEIRO (motor local, CPU): pessoa do vídeo -> personagem da foto.

Etapas:
  1. Lê o vídeo, detecta a pose (33 pontos) e a máscara da pessoa em cada quadro.
  2. Suaviza a pose no tempo (tira tremedeira).
  3. Apaga a pessoa original (preenche o fundo com outros quadros / inpainting).
  4. Rigga a foto do personagem e a move com o esqueleto de cada quadro.
  5. Ajusta a luz do personagem à cena e junta tudo. O áudio original é mantido.
"""
from __future__ import annotations

import subprocess
import time
from typing import Callable

import cv2
import imageio_ffmpeg
import numpy as np

from .background import BackgroundFiller
from .pose import PoseDetector, PoseResult, plausible
from .puppet import Character, NoPersonError, skeleton_mask

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def _smooth_poses(poses: list[PoseResult | None], sigma: float = 1.2) -> list[PoseResult | None]:
    """Suavização gaussiana centrada (offline) + preenche buracos curtos."""
    n = len(poses)
    idx = [i for i, p in enumerate(poses) if p is not None]
    if not idx:
        return poses
    pts = np.stack([poses[i].pts for i in idx])
    vis = np.stack([poses[i].vis for i in idx])
    z = np.stack([poses[i].z for i in idx])
    out: list[PoseResult | None] = []
    r = int(3 * sigma) + 1
    for t in range(n):
        # quadros válidos próximos
        near = [k for k, i in enumerate(idx) if abs(i - t) <= r]
        if not near:
            out.append(None)  # sem pose confiável: quadro fica original
            continue
        wts = np.array([np.exp(-0.5 * ((idx[k] - t) / sigma) ** 2) for k in near])[:, None]
        wts /= wts.sum()
        p = (pts[near] * wts[..., None]).sum(0)
        v = (vis[near] * wts).sum(0)
        zz = (z[near] * wts).sum(0)
        base = poses[t] if poses[t] is not None else poses[idx[near[len(near) // 2]]]
        out.append(PoseResult(p.astype(np.float32), v, zz, base.mask))
    return out


def _transfer_poses(poses, bg: "BackgroundFiller", max_gap: int = 15):
    """Quadros sem pose confiável herdam a pose (e a máscara) boa mais próxima,
    levada pelo movimento da câmera (homografia)."""
    good = [i for i, p in enumerate(poses) if p is not None]
    if not good:
        return poses
    out = list(poses)
    for t, p in enumerate(poses):
        if p is not None:
            continue
        j = min(good, key=lambda g: abs(g - t))
        if abs(j - t) > max_gap:
            continue
        src = poses[j]
        h, w = bg.masks[t].shape
        if bg.static:
            pts = src.pts.copy()
            bg.masks[t] = np.maximum(bg.masks[t], bg.masks[j])
        else:
            H = bg._homography(j, t)
            if H is None:
                continue
            pts = cv2.perspectiveTransform(src.pts[None].astype(np.float32), H)[0]
            wm = cv2.warpPerspective(bg.masks[j], H, (w, h), flags=cv2.INTER_NEAREST)
            bg.masks[t] = np.maximum(bg.masks[t], wm)
        out[t] = PoseResult(pts.astype(np.float32), src.vis, src.z, None)
    return out


def _smooth_1d(x: np.ndarray, sigma: float = 3.0) -> np.ndarray:
    r = int(3 * sigma)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    xp = np.pad(x, r, mode="edge")
    return np.convolve(xp, k, mode="valid")


def process_body_video(video_path: str, image_path: str, out_path: str, max_side: int = 720,
                       max_seconds: float | None = 15, harmonize: float = 0.35,
                       progress: Callable[[float, str], None] | None = None) -> dict:
    progress = progress or (lambda p, m: None)
    t0 = time.time()
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError("Não consegui abrir a foto.")
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    progress(0.01, "Recortando e 'riggando' o personagem da foto...")
    char = Character(img)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Não consegui abrir o vídeo.")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    fps = fps if 1 < fps <= 120 else 25.0
    W, H = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    sc = min(1.0, max_side / max(W, H)) if max_side else 1.0
    ow, oh = int(W * sc) // 2 * 2, int(H * sc) // 2 * 2
    limit = int(max_seconds * fps) if max_seconds else None
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 0
    if limit:
        total = min(total, limit) if total else limit

    # ---------- passo 1: pose + máscara
    det = PoseDetector(video_mode=True)
    frames, masks, poses = [], [], []
    dil = max(5, int(oh * 0.025)) | 1
    kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dil, dil))
    while True:
        ok, f = cap.read()
        if not ok or (limit and len(frames) >= limit):
            break
        if f.shape[1] != ow or f.shape[0] != oh:
            f = cv2.resize(f, (ow, oh), interpolation=cv2.INTER_AREA)
        p = det(f)
        m = np.zeros((oh, ow), np.uint8)
        if p is not None:
            m = cv2.dilate((p.mask > 0.3).astype(np.uint8) * 255, kern)
            p.mask = None  # economiza memória
        frames.append(f)
        masks.append(m)
        poses.append(p)
        if len(frames) % 5 == 0:
            progress(0.02 + 0.28 * len(frames) / max(total, 1), f"Analisando movimento: quadro {len(frames)}/{total}")
    cap.release()
    det.close()
    n = len(frames)
    if n == 0:
        raise ValueError("O vídeo não tem quadros legíveis.")
    poses = [p if plausible(p) else None for p in poses]
    if all(p is None for p in poses):
        raise NoPersonError("Não encontrei nenhuma pessoa de corpo no VÍDEO.")

    progress(0.31, "Calculando o movimento da câmera...")
    bg = BackgroundFiller(frames, masks)
    poses = _smooth_poses(_transfer_poses(poses, bg), sigma=1.2)

    # escala personagem->vídeo, estável no tempo
    s_t = np.array([char.robust_scale(p) if p is not None else np.nan for p in poses])
    good = ~np.isnan(s_t)
    s_t = np.interp(np.arange(n), np.nonzero(good)[0], s_t[good])
    s_t = _smooth_1d(s_t, 4.0)

    # reforça a máscara da pessoa com o esqueleto (roupa que o recorte perdeu)
    for t in range(n):
        if poses[t] is not None:
            masks[t] = np.maximum(masks[t], skeleton_mask(poses[t], (oh, ow)))

    # ---------- passo 2: fundo limpo (o BackgroundFiller já foi criado acima)
    progress(0.33, "Apagando a pessoa original do vídeo...")

    # luz: média de brilho/cor da pessoa original x personagem (global, sem piscar)
    lab_char = cv2.cvtColor(char.img, cv2.COLOR_BGR2LAB).astype(np.float32)
    c_mean = lab_char[char.alpha > 127].mean(0)
    samp = [i for i in np.linspace(0, n - 1, min(n, 12)).astype(int) if masks[i].any()]
    if samp and harmonize > 0:
        vals = np.concatenate([cv2.cvtColor(frames[i], cv2.COLOR_BGR2LAB)[masks[i] > 0] for i in samp]).astype(np.float32)
        shift = (vals.mean(0) - c_mean) * harmonize
        shift[1:] *= 0.5  # cor muda menos que brilho
    else:
        shift = np.zeros(3, np.float32)

    # ---------- passo 3: renderização
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
           "-s", f"{ow}x{oh}", "-r", f"{fps:.6f}", "-i", "-", "-i", video_path,
           "-map", "0:v:0", "-map", "1:a:0?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    rendered = 0
    try:
        for t in range(n):
            out = bg.fill(t) if poses[t] is not None else frames[t]
            if poses[t] is not None:
                rgb, a = char.render(poses[t], out.shape, s=float(s_t[t]))
                if rgb is not None:
                    if np.any(shift):
                        lab = cv2.cvtColor(rgb, cv2.COLOR_BGR2LAB).astype(np.float32) + shift
                        rgb = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
                    af = cv2.GaussianBlur(a, (3, 3), 0).astype(np.float32)[..., None] / 255.0
                    out = (rgb * af + out * (1 - af)).astype(np.uint8)
                    rendered += 1
            proc.stdin.write(out.tobytes())
            if t % 5 == 0:
                el = time.time() - t0
                progress(0.35 + 0.64 * (t + 1) / n, f"Gerando: quadro {t + 1}/{n} · {el:.0f}s")
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        err = proc.stderr.read().decode(errors="ignore")
        proc.wait()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg falhou: {err[-400:]}")
    info = {"frames": n, "frames_com_personagem": rendered, "fps": round(fps, 2),
            "size": f"{ow}x{oh}", "engine": "corpo-local", "seconds": round(time.time() - t0, 1),
            "camera": "parada" if bg.static else "em movimento"}
    progress(1.0, "Pronto!")
    return info
