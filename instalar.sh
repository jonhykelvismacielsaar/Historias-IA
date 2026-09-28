#!/usr/bin/env bash
# Instala tudo o que é preciso (Linux/macOS). No Windows use os mesmos comandos no PowerShell.
set -e
cd "$(dirname "$0")"
python3 -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -r requirements.txt
# o mediapipe instala o OpenCV "com janela", que precisa de libGL; em servidor usamos o headless
.venv/bin/pip uninstall -y opencv-python opencv-contrib-python >/dev/null 2>&1 || true
.venv/bin/pip install --force-reinstall --no-deps opencv-contrib-python-headless
.venv/bin/python baixar_modelos.py || echo "(Sem os modelos de IA: o motor clássico vai funcionar mesmo assim.)"
echo "Pronto! Rode:  .venv/bin/python app.py   e abra http://localhost:7860"
