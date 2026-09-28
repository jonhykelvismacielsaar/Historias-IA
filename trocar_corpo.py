"""Linha de comando: troca a PESSOA INTEIRA do vídeo pelo personagem da foto.

Exemplos:
    # local, grátis, sem GPU (marionete 2D)
    python trocar_corpo.py video.mp4 personagem.png

    # IA de ponta na nuvem (Wan 2.2 Animate Replace)
    python trocar_corpo.py video.mp4 personagem.png --nuvem deapi --chave SUA_CHAVE
    python trocar_corpo.py video.mp4 personagem.png --nuvem fal   # usa FAL_KEY do .env
"""
import argparse
import sys
import warnings

warnings.filterwarnings("ignore")

from bodyswap.cloud import process_cloud  # noqa: E402
from bodyswap.video import process_body_video  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Coloca o personagem da FOTO no lugar da pessoa do VÍDEO.")
    ap.add_argument("video")
    ap.add_argument("foto")
    ap.add_argument("-o", "--saida", default="resultado_corpo.mp4")
    ap.add_argument("--nuvem", choices=["deapi", "fal"], help="usa a IA Wan 2.2 Animate na nuvem")
    ap.add_argument("--chave", help="chave da API (ou DEAPI_API_KEY / FAL_KEY no .env)")
    ap.add_argument("--qualidade", default="720p", choices=["480p", "580p", "720p"])
    ap.add_argument("--resolucao", type=int, default=720, help="motor local: lado maior máximo")
    ap.add_argument("--segundos", type=float, default=0, help="processa só os N primeiros segundos")
    a = ap.parse_args()

    def prog(p, m):
        print(f"\r[{int(p * 100):3d}%] {m:<70}", end="", flush=True)

    if a.nuvem:
        info = process_cloud(a.video, a.foto, a.saida, provider=a.nuvem, api_key=a.chave,
                             resolution=a.qualidade, max_seconds=a.segundos or None, progress=prog)
    else:
        info = process_body_video(a.video, a.foto, a.saida, max_side=a.resolucao,
                                  max_seconds=a.segundos or 15, progress=prog)
    print(f"\nSalvo em {a.saida}  {info}")


if __name__ == "__main__":
    sys.exit(main())
