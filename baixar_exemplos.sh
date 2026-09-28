#!/usr/bin/env bash
# Baixa os vídeos/imagens de exemplo oficiais do Wan 2.2 Animate (para testar).
# Ficam em amostras/wan/ (fora do Git).
set -e
cd "$(dirname "$0")"
tmp=$(mktemp -d)
git clone -q --depth 1 --filter=blob:none --sparse https://github.com/Wan-Video/Wan2.2.git "$tmp/wan"
git -C "$tmp/wan" sparse-checkout set examples/wan_animate
mkdir -p amostras/wan
cp -r "$tmp/wan/examples/wan_animate/"* amostras/wan/
rm -rf "$tmp"
echo "Exemplos em amostras/wan/{animate,replace}/ (video.mp4 + image.jpeg)"
echo "Teste:  .venv/bin/python trocar_corpo.py amostras/wan/animate/video.mp4 amostras/wan/animate/image.jpeg"
