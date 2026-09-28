"""Linha de comando: troca o rosto de um vídeo pelo rosto de uma foto.

Exemplos:
    python trocar_rosto.py video.mp4 foto.jpg
    python trocar_rosto.py video.mp4 foto.jpg -o resultado.mp4 --motor ia
    python trocar_rosto.py video.mp4 foto.jpg --mistura suave --resolucao 1080 --so-maior
"""
import argparse
import sys
import warnings

warnings.filterwarnings("ignore")

from faceswap import process_video  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Coloca o rosto da FOTO na pessoa do VÍDEO.")
    ap.add_argument("video")
    ap.add_argument("foto")
    ap.add_argument("-o", "--saida", default="resultado.mp4")
    ap.add_argument("--motor", choices=["auto", "classico", "ia"], default="auto")
    ap.add_argument("--mistura", choices=["seamless", "suave"], default="seamless")
    ap.add_argument("--resolucao", type=int, default=720, help="lado maior máximo (0 = original)")
    ap.add_argument("--segundos", type=float, default=0, help="processa só os N primeiros segundos")
    ap.add_argument("--so-maior", action="store_true", help="troca só o maior rosto")
    a = ap.parse_args()

    def prog(p, m):
        print(f"\r[{int(p * 100):3d}%] {m:<60}", end="", flush=True)

    info = process_video(a.video, a.foto, a.saida, engine=a.motor, blend=a.mistura,
                         all_faces=not a.so_maior, max_side=a.resolucao,
                         max_seconds=a.segundos or None, progress=prog)
    print(f"\nSalvo em {a.saida}  {info}")


if __name__ == "__main__":
    sys.exit(main())
