"""Troca do CORPO INTEIRO na nuvem com a IA Wan 2.2 Animate (modo "Replace").

É o modelo de ponta, aberto, da Alibaba (14 bilhões de parâmetros). Ele
substitui a pessoa do vídeo pelo personagem da foto, mantendo os movimentos,
as expressões, a câmera e a luz da cena. Precisa de uma GPU de 24–80 GB, por
isso roda num provedor na nuvem:

  * deAPI  (https://deapi.ai)  – cadastro dá US$ 5 de crédito grátis, sem cartão.
                                 Limite: 8 s por vídeo, até 852 px.
                                 Chave: variável DEAPI_API_KEY
  * fal.ai (https://fal.ai)    – US$ 0,04/s (480p) a US$ 0,08/s (720p).
                                 Chave: variável FAL_KEY

A chave também pode ser digitada na interface web (não é salva em disco).
"""
from __future__ import annotations

import base64
import mimetypes
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Callable

import requests

from .video import FFMPEG

ROOT = Path(__file__).resolve().parent.parent
PROVIDERS = {
    "deapi": {"nome": "deAPI", "env": "DEAPI_API_KEY", "max_s": 8.0, "max_side": 832},
    "fal": {"nome": "fal.ai", "env": "FAL_KEY", "max_s": 10.0, "max_side": 1280},
}
DEAPI = os.environ.get("DEAPI_BASE", "https://api.deapi.ai")
DEAPI_MODEL = "Wan2_2_Animate_14B_INT8"
FAL_ENDPOINT = "fal-ai/wan/v2.2-14b/animate/replace"
FAL_QUEUE = os.environ.get("FAL_QUEUE_BASE", "https://queue.fal.run")


class CloudError(RuntimeError):
    pass


def load_env():
    """Lê um arquivo .env simples (CHAVE=valor) na raiz do projeto."""
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def get_key(provider: str, key: str | None = None) -> str | None:
    load_env()
    return key or os.environ.get(PROVIDERS[provider]["env"])


def available_providers() -> dict[str, bool]:
    load_env()
    return {p: bool(os.environ.get(c["env"])) for p, c in PROVIDERS.items()}


def _prepare_video(src: str, dst: str, max_s: float, max_side: int, fps: int = 24):
    """Corta a duração, reduz a resolução (múltiplos de 16) e padroniza para H.264."""
    vf = (f"scale='if(gt(iw,ih),min({max_side},iw),-2)':'if(gt(iw,ih),-2,min({max_side},ih))',"
          f"scale='trunc(iw/16)*16':'trunc(ih/16)*16',fps={fps}")
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", src, "-t", f"{max_s}", "-vf", vf,
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "128k", dst]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise CloudError(f"Falha ao preparar o vídeo: {r.stderr[-300:]}")


def _video_size(path: str) -> tuple[int, int]:
    import cv2
    cap = cv2.VideoCapture(path)
    w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return w, h


def _data_uri(path: str) -> str:
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


def _download(url: str, dst: str):
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dst, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)


def _mux_audio(video_ai: str, original: str, out: str):
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", video_ai, "-i", original,
           "-map", "0:v:0", "-map", "1:a:0?", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", "-movflags", "+faststart", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise CloudError(f"Falha ao juntar o áudio: {r.stderr[-300:]}")


# ------------------------------------------------------------------ deAPI
def _run_deapi(video: str, image: str, key: str, progress, resolution: str) -> str:
    w, h = _video_size(video)
    target = {"480p": 480, "580p": 576, "720p": 768}.get(resolution, 768)
    s = min(1.0, target / max(w, h), 852 / max(w, h))
    ow, oh = max(256, int(w * s) // 16 * 16), max(256, int(h * s) // 16 * 16)
    hdr = {"Authorization": f"Bearer {key}", "Accept": "application/json"}
    progress(0.12, "Enviando para a deAPI (Wan 2.2 Animate)...")
    with open(video, "rb") as fv, open(image, "rb") as fi:
        r = requests.post(f"{DEAPI}/api/v2/videos/replacements", headers=hdr, timeout=300,
                          files={"video": ("video.mp4", fv, "video/mp4"),
                                 "ref_image": (Path(image).name, fi, mimetypes.guess_type(image)[0] or "image/png")},
                          data={"model": DEAPI_MODEL, "width": ow, "height": oh})
    if r.status_code >= 400:
        raise CloudError(f"deAPI recusou o pedido ({r.status_code}): {r.text[:400]}")
    rid = r.json()["data"]["request_id"]
    t0 = time.time()
    while True:
        time.sleep(5)
        j = requests.get(f"{DEAPI}/api/v2/jobs/{rid}", headers=hdr, timeout=60).json()["data"]
        st = j.get("status")
        pr = float(j.get("progress") or 0) / 100
        progress(0.15 + 0.75 * pr, f"deAPI: {st} {int(pr * 100)}% · {int(time.time() - t0)}s")
        if st == "done":
            return j["result_url"]
        if st == "error":
            raise CloudError(f"deAPI falhou: {j.get('error_reason') or j.get('error_code')}"
                             f" (reembolsado: {j.get('refunded')})")
        if time.time() - t0 > 1800:
            raise CloudError("Tempo esgotado esperando a deAPI.")


# ------------------------------------------------------------------ fal.ai
def _run_fal(video: str, image: str, key: str, progress, resolution: str) -> str:
    hdr = {"Authorization": f"Key {key}", "Content-Type": "application/json"}
    body = {"video_url": _data_uri(video), "image_url": _data_uri(image),
            "resolution": resolution if resolution in ("480p", "580p", "720p") else "480p",
            "video_quality": "high"}
    progress(0.12, "Enviando para o fal.ai (Wan 2.2 Animate Replace)...")
    r = requests.post(f"{FAL_QUEUE}/{FAL_ENDPOINT}", headers=hdr, json=body, timeout=300)
    if r.status_code >= 400:
        raise CloudError(f"fal.ai recusou o pedido ({r.status_code}): {r.text[:400]}")
    j = r.json()
    status_url, response_url = j["status_url"], j["response_url"]
    t0 = time.time()
    while True:
        time.sleep(5)
        s = requests.get(status_url, headers=hdr, timeout=60).json()
        st = s.get("status")
        el = int(time.time() - t0)
        progress(min(0.9, 0.15 + el / 600), f"fal.ai: {st} · {el}s"
                 + (f" · posição na fila {s.get('queue_position')}" if st == "IN_QUEUE" else ""))
        if st == "COMPLETED":
            break
        if st not in ("IN_QUEUE", "IN_PROGRESS"):
            raise CloudError(f"fal.ai falhou: {s}")
        if el > 1800:
            raise CloudError("Tempo esgotado esperando o fal.ai.")
    res = requests.get(response_url, headers=hdr, timeout=60).json()
    if "video" not in res:
        raise CloudError(f"fal.ai não devolveu vídeo: {str(res)[:300]}")
    return res["video"]["url"]


def process_cloud(video_path: str, image_path: str, out_path: str, provider: str = "deapi",
                  api_key: str | None = None, resolution: str = "720p",
                  max_seconds: float | None = None,
                  progress: Callable[[float, str], None] | None = None) -> dict:
    progress = progress or (lambda p, m: None)
    if provider not in PROVIDERS:
        raise CloudError(f"Provedor desconhecido: {provider}")
    cfg = PROVIDERS[provider]
    key = get_key(provider, api_key)
    if not key:
        raise CloudError(f"Falta a chave da API do {cfg['nome']}. Crie uma conta, copie a chave e "
                         f"cole na interface (ou coloque {cfg['env']}=... no arquivo .env).")
    t0 = time.time()
    secs = min(cfg["max_s"], max_seconds or cfg["max_s"])
    with tempfile.TemporaryDirectory() as tmp:
        prep = os.path.join(tmp, "entrada.mp4")
        progress(0.03, f"Preparando o vídeo (até {secs:.0f}s)...")
        _prepare_video(video_path, prep, secs, cfg["max_side"])
        try:
            url = (_run_deapi if provider == "deapi" else _run_fal)(prep, image_path, key, progress, resolution)
        except requests.RequestException as e:
            raise CloudError(f"Não consegui falar com o {cfg['nome']}: {e}") from e
        progress(0.93, "Baixando o resultado...")
        raw = os.path.join(tmp, "ia.mp4")
        _download(url, raw)
        _mux_audio(raw, prep, out_path)
    progress(1.0, "Pronto!")
    return {"engine": f"Wan 2.2 Animate ({cfg['nome']})", "seconds": round(time.time() - t0, 1),
            "duracao_max": secs}
