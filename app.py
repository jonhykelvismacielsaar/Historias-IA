"""Interface web: envie um VÍDEO + uma FOTO e receba o vídeo com o rosto trocado.

Uso:  python app.py   (abre em http://0.0.0.0:7860)
"""
from __future__ import annotations

import os
import threading
import uuid
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import cv2
from flask import Flask, jsonify, render_template, request, send_from_directory

from bodyswap.cloud import PROVIDERS, available_providers, process_cloud
from bodyswap.video import process_body_video
from faceswap import NoFaceError, ai_available, preview_frame, process_video

ROOT = Path(__file__).resolve().parent
UPLOADS = ROOT / "uploads"
OUTPUTS = ROOT / "saida"
UPLOADS.mkdir(exist_ok=True)
OUTPUTS.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500 MB

JOBS: dict[str, dict] = {}
LOCK = threading.Semaphore(1)  # um vídeo por vez (CPU limitada)


def _save_uploads(job_id: str):
    v = request.files.get("video")
    i = request.files.get("imagem")
    if not v or not i or not v.filename or not i.filename:
        raise ValueError("Envie o vídeo E a foto.")
    vp = UPLOADS / f"{job_id}_video{Path(v.filename).suffix.lower() or '.mp4'}"
    ip = UPLOADS / f"{job_id}_foto{Path(i.filename).suffix.lower() or '.jpg'}"
    v.save(vp)
    i.save(ip)
    return str(vp), str(ip)


def _opts():
    f = request.form
    return dict(engine=f.get("motor", "auto"), blend=f.get("mistura", "seamless"))


@app.get("/")
def index():
    return render_template("index.html", ia=ai_available(), nuvem=available_providers(),
                           provedores=PROVIDERS)


@app.post("/api/preview")
def api_preview():
    job_id = uuid.uuid4().hex[:10]
    try:
        vp, ip = _save_uploads(job_id)
        img = preview_frame(vp, ip, **_opts())
    except (NoFaceError, ValueError, FileNotFoundError) as e:
        return jsonify(erro=str(e)), 400
    name = f"{job_id}_preview.jpg"
    cv2.imwrite(str(OUTPUTS / name), img, [cv2.IMWRITE_JPEG_QUALITY, 92])
    return jsonify(url=f"/saida/{name}")


@app.post("/api/processar")
def api_processar():
    job_id = uuid.uuid4().hex[:10]
    try:
        vp, ip = _save_uploads(job_id)
    except ValueError as e:
        return jsonify(erro=str(e)), 400
    f = request.form
    modo = f.get("modo", "rosto")
    secs = float(f.get("limite", "0") or 0)
    if modo == "corpo":
        func = process_body_video
        opts = dict(max_side=int(f.get("resolucao", "720")), max_seconds=secs if secs > 0 else 15)
    elif modo == "nuvem":
        func = process_cloud
        opts = dict(provider=f.get("provedor", "deapi"), api_key=(f.get("chave") or "").strip() or None,
                    resolution=f.get("resolucao_ia", "720p"), max_seconds=secs if secs > 0 else None)
    else:
        func = process_video
        opts = _opts()
        opts["all_faces"] = f.get("todos", "1") == "1"
        opts["max_side"] = int(f.get("resolucao", "720"))
        opts["max_seconds"] = secs if secs > 0 else None
    out_name = f"{job_id}_resultado.mp4"
    JOBS[job_id] = {"status": "na_fila", "progresso": 0.0, "mensagem": "Na fila..."}

    def run():
        with LOCK:
            JOBS[job_id].update(status="processando", mensagem="Começando...")

            def prog(p, m):
                JOBS[job_id].update(progresso=round(p, 3), mensagem=m)
            try:
                info = func(vp, ip, str(OUTPUTS / out_name), progress=prog, **opts)
                JOBS[job_id].update(status="pronto", progresso=1.0, url=f"/saida/{out_name}",
                                    info=info, mensagem="Pronto!")
            except Exception as e:  # noqa: BLE001
                JOBS[job_id].update(status="erro", mensagem=str(e))

    threading.Thread(target=run, daemon=True).start()
    return jsonify(id=job_id)


@app.get("/api/status/<job_id>")
def api_status(job_id):
    job = JOBS.get(job_id)
    if not job:
        return jsonify(erro="Trabalho não encontrado"), 404
    return jsonify(job)


@app.get("/saida/<path:name>")
def saida(name):
    return send_from_directory(OUTPUTS, name, as_attachment=request.args.get("baixar") == "1")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    print(f"Motor de IA disponível: {ai_available()}")
    app.run(host="0.0.0.0", port=port, threaded=True)
