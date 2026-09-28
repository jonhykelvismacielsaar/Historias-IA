"""Baixa os modelos do motor de IA (alta qualidade) para a pasta models/.

    python baixar_modelos.py

Baixa:
  - inswapper_128.onnx  (~530 MB)  – troca de rosto (InsightFace)
  - w600k_r50.onnx      (~170 MB)  – reconhece a identidade do rosto (do pacote buffalo_l)

Se o download falhar (rede bloqueada), baixe manualmente por um dos links
abaixo e coloque os arquivos dentro de models/.

Licença: modelos InsightFace – apenas uso NÃO comercial / pesquisa.
"""
from __future__ import annotations

import hashlib
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

MODELS = Path(__file__).resolve().parent / "models"
INSWAPPER_SHA256 = "e4a3f08c753cb72d04e10aa0f7dbe3deebbf39567d4ead6dce08e98aa49e16af"

INSWAPPER_URLS = [
    "https://github.com/facefusion/facefusion-assets/releases/download/models/inswapper_128.onnx",
    "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx",
    "https://huggingface.co/facefusion/models-3.0.0/resolve/main/inswapper_128.onnx",
]
ARCFACE_URLS = [  # (url, é_zip)
    ("https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip", True),
    ("https://github.com/facefusion/facefusion-assets/releases/download/models-3.0.0/arcface_w600k_r50.onnx", False),
    ("https://huggingface.co/facefusion/models-3.0.0/resolve/main/arcface_w600k_r50.onnx", False),
]


def _download(url: str, dest: Path) -> bool:
    print(f"  -> {url}")
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(tmp, "wb") as f:
            total = int(r.headers.get("Content-Length") or 0)
            done = 0
            while chunk := r.read(1 << 20):
                f.write(chunk)
                done += len(chunk)
                if total:
                    print(f"\r     {done / 1e6:7.1f} / {total / 1e6:.1f} MB", end="", flush=True)
        print()
        tmp.replace(dest)
        return True
    except Exception as e:  # noqa: BLE001
        print(f"\n     falhou: {e}")
        tmp.unlink(missing_ok=True)
        return False


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main() -> int:
    MODELS.mkdir(exist_ok=True)
    ok = True

    ins = MODELS / "inswapper_128.onnx"
    if ins.exists():
        print("inswapper_128.onnx já existe.")
    else:
        print("Baixando inswapper_128.onnx ...")
        if not any(_download(u, ins) for u in INSWAPPER_URLS):
            ok = False
    if ins.exists() and _sha256(ins) != INSWAPPER_SHA256:
        print("  AVISO: o hash do inswapper_128.onnx é diferente do oficial (arquivo alterado?).")

    arc = MODELS / "w600k_r50.onnx"
    if arc.exists():
        print("w600k_r50.onnx já existe.")
    else:
        print("Baixando w600k_r50.onnx ...")
        got = False
        for url, is_zip in ARCFACE_URLS:
            if is_zip:
                z = MODELS / "buffalo_l.zip"
                if _download(url, z):
                    with zipfile.ZipFile(z) as zf:
                        name = next((n for n in zf.namelist() if n.endswith("w600k_r50.onnx")), None)
                        if name:
                            with zf.open(name) as src, open(arc, "wb") as dst:
                                shutil.copyfileobj(src, dst)
                            got = True
                    z.unlink(missing_ok=True)
            else:
                got = _download(url, arc)
            if got:
                break
        ok = ok and got

    if ok:
        print("\nTudo pronto! O motor de IA será usado automaticamente.")
        return 0
    print("\nNão consegui baixar tudo. Baixe manualmente e coloque em models/:")
    print("  inswapper_128.onnx :", INSWAPPER_URLS[0])
    print("  w600k_r50.onnx     : dentro de", ARCFACE_URLS[0][0])
    print("O motor CLÁSSICO continua funcionando sem esses arquivos.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
