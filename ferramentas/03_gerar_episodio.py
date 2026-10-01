#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_gerar_episodio.py — Monta o JSON final de um episódio.

Fluxo de produção:
  1. A "curadoria" (arquivo em roteiro/curadoria/EP-XXXX.json) traz a parte criativa:
     narração da voz de Deus, prompts de imagem/vídeo, câmera, som, presença do pincel.
  2. Este script junta a curadoria com o TEXTO REAL das Escrituras, lido do corpus
     consolidado (hebraico massorético com niqqud, Targum Onkelos em aramaico,
     Septuaginta em grego, Peshitta em siríaco, grego do NT e português).
  3. O resultado é um episódio completo, pronto para gerar imagem e vídeo, com
     prompts em inglês (melhor desempenho em Midjourney/Sora/Veo/Kling) e tradução
     em português para revisão.

Uso:
  python3 ferramentas/03_gerar_episodio.py EP-0001
  python3 ferramentas/03_gerar_episodio.py --todos
"""

from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_biblia import POR_SLUG, ref as referencia_biblica, transliterar_grego, transliterar_simples

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(RAIZ, "dados", "processado", "versiculos")
CURADORIA = os.path.join(RAIZ, "roteiro", "curadoria")
SAIDA = os.path.join(RAIZ, "roteiro", "episodios")
INDICE = os.path.join(RAIZ, "roteiro", "indice_episodios.json")

FRAMES_POR_EPISODIO = 12
SEGUNDOS_POR_FRAME = 5

# ---------------------------------------------------------------------------
# ESTILO VISUAL BASE — o conceito do projeto:
# "Deus pintando o quadro": realismo pictórico, pincel flutuante, nada de figura divina.
# No vídeo: a câmera ENTRA na pintura e a cena ganha vida.
# ---------------------------------------------------------------------------
ESTILO_BASE_EN = (
    "Hyper-realistic cinematic oil painting on coarse linen canvas, thick impasto brushwork "
    "with glistening wet paint ridges, museum-grade baroque realism fused with photoreal detail, "
    "dramatic chiaroscuro, volumetric god-rays, immense biblical scale, epic composition, "
    "rich earthy palette of ochre, deep umber, crimson and gold, subtle craquelure of old varnish, "
    "shallow depth of field, ultra-detailed texture of canvas weave, 8k, masterpiece, no text, no watermark"
)

PINCEL_EN = (
    "a single large wooden-handled artist's brush floating in mid-air at the edge of the composition, "
    "bristles wet with fresh pigment, a gleaming trail of just-painted paint behind the brush at the upper corner, "
    "the brush is clearly mid-stroke, painting this very scene into existence"
)

SEM_PINCEL_EN = (
    "no brush visible in this frame, no painter, no human figure, the painting already fully alive without any artist present"
)

ESTILO_VIDEO_BASE_EN = (
    "the camera flies INTO the surface of the painting and the painted brushstrokes bloom into living three-dimensional reality; "
    "the wet oil paint dissolves into real matter, texture and depth; continuous single take, "
    "cinematic 24fps, volumetric light, floating dust motes, physically accurate motion, shallow depth of field, "
    "no text, no watermark, no on-screen graphics"
)

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def carregar_corpus() -> dict:
    corpus = {}
    for arq in os.listdir(CORPUS):
        if arq.endswith(".json"):
            with open(os.path.join(CORPUS, arq), encoding="utf-8") as fh:
                d = json.load(fh)
            corpus[d["slug"]] = d
    return corpus


def versiculos_do_trecho(corpus: dict, slug: str, capitulo: int, v_ini: int, v_fim: int) -> list:
    livro = corpus[slug]
    caps = livro["capitulos"].get(str(capitulo), {})
    saida = []
    for v in range(v_ini, v_fim + 1):
        dado = caps.get(str(v))
        if dado:
            saida.append((v, dado))
    return saida


def bloco_original(slug: str, capitulo: int, versos: list) -> dict:
    """Texto original do trecho, com transliteração de apoio."""
    he = " ".join(d.get("he", "") for _, d in versos).strip()
    he_limpo = " ".join(d.get("he_limpo", "") for _, d in versos).strip()
    targum = " ".join(d.get("targum_onkelos", "") for _, d in versos).strip()
    targum_jon = " ".join(d.get("targum_jonathan", "") or d.get("targum_writings", "") for _, d in versos).strip()
    peshitta = " ".join(d.get("peshitta", "") for _, d in versos).strip()
    lxx = " ".join(d.get("lxx_grego", "") for _, d in versos).strip()
    grego_nt = " ".join(d.get("grego_sblgnt", "") for _, d in versos).strip()
    pt = " ".join(d.get("pt_aa", "") for _, d in versos).strip()
    out = {
        "referencia": f"{POR_SLUG[slug]['nome_pt']} {capitulo}:{versos[0][0]}" + (
            f"-{versos[-1][0]}" if versos[-1][0] != versos[0][0] else ""),
        "pt_almeida": pt,
    }
    if he:
        out["hebraico_mt"] = he
        out["hebraico_transliteracao"] = transliterar_simples(he)
    if targum:
        out["targum_onkelos_aramaico"] = targum
    if targum_jon:
        out["targum_profetas_aramaico"] = targum_jon
    if peshitta:
        out["peshitta_siriaco"] = peshitta
        out["fonte_peshitta"] = "Peshitta (siríaco) — ETCBC / dukhrana / SEDRA, domínio público"
    if lxx:
        out["septuaginta_grego"] = lxx
    if grego_nt:
        out["grego_sblgnt"] = grego_nt
        out["grego_transliteracao"] = transliterar_grego(grego_nt)
    return out


def contar_palavras(texto: str) -> int:
    return len(re.findall(r"[\wÀ-ÿ']+", texto or ""))


# ---------------------------------------------------------------------------
# Montagem
# ---------------------------------------------------------------------------
def montar_episodio(numero: str, corpus: dict, indice: dict) -> dict:
    caminho_cur = os.path.join(CURADORIA, f"{numero}.json")
    if not os.path.exists(caminho_cur):
        raise FileNotFoundError(f"Curadoria não encontrada: {caminho_cur}")
    with open(caminho_cur, encoding="utf-8") as fh:
        cur = json.load(fh)

    # Episódio correspondente no índice geral
    plano = next((e for e in indice["episodios"] if e["id"] == numero), None)

    slug = cur.get("slug")
    capitulo = cur.get("capitulo")
    trecho_versos = []
    original = {}
    if slug and capitulo:
        v_ini = cur.get("versiculo_inicial") or (plano["faixa_versiculos"][0] if plano else 1)
        v_fim = cur.get("versiculo_final") or (plano["faixa_versiculos"][1] if plano else v_ini)
        trecho_versos = versiculos_do_trecho(corpus, slug, capitulo, v_ini, v_fim)
        if trecho_versos:
            original = bloco_original(slug, capitulo, trecho_versos)

    frames = []
    for i, f in enumerate(cur["frames"], start=1):
        t_ini = (i - 1) * SEGUNDOS_POR_FRAME
        t_fim = i * SEGUNDOS_POR_FRAME
        pincel = f.get("pincel", True)
        estilo_visual = f.get("estilo_visual") or ESTILO_BASE_EN
        partes_imagem = [
            f["imagem_scene_en"],
            estilo_visual,
            PINCEL_EN if pincel else SEM_PINCEL_EN,
            f"Lighting and mood: {f.get('luz_en', 'dramatic volumetric light')}",
            f"Aspect ratio {f.get('proporcao', '16:9')}",
        ]
        prompt_imagem = ". ".join(p.strip().rstrip(".") for p in partes_imagem if p) + "."
        prompt_imagem_neg = f.get("imagem_negativo_en",
            "text, letters, numbers, subtitles, captions, burned-in words, lower thirds, titles, watermark, signature, logo, human face of God, "
            "depiction of the divine figure, cartoon, cgi look, low resolution, blurry, deformed anatomy, extra limbs, "
            "modern objects, anachronism")
        prompt_video = (
            f"{ESTILO_VIDEO_BASE_EN}. Movement: {f['video_movimento_en']}. "
            f"Camera: {f.get('camera_en','slow cinematic dolly-in')}. "
            f"{'Duration 5 seconds, ' if True else ''}sound of the scene implied visually, seamless loop-friendly ending."
        )
        narracao = f.get("narracao", "")
        frames.append({
            "frame": i,
            "titulo": f.get("titulo", f"Frame {i}"),
            "tempo": {"inicio": f"00:{t_ini:02d}.0", "fim": f"00:{t_fim:02d}.0", "duracao_s": SEGUNDOS_POR_FRAME},
            "referencia_biblica": f.get("referencia") or (cur.get("referencia") or ""),
            "versiculos_cobertos": f.get("versiculos", []),
            "acao_cena": f.get("acao_cena_pt", ""),
            "pincel_flutuante": pincel,
            "falas": {
                "narrador_deus_pt": narracao,
                "narrador_palavras": contar_palavras(narracao),
                "narrador_limite_palavras_5s": 20,
                "personagens_pt": f.get("falas_personagens", []),
                "texto_da_passagem_pt": f.get("texto_passagem_pt", ""),
            },
            "prompt_imagem": {
                "modelo_alvo": f.get("modelo_imagem", "Midjourney v7 / Flux / SDXL (modo foto-realista)"),
                "prompt_en": prompt_imagem,
                "negative_prompt_en": prompt_imagem_neg,
                "parametros": f.get("parametros_imagem",
                    {"aspect_ratio": "16:9", "resolucao": "3840x2160", "stylize": 250, "style": "raw", "chaos": 0,
                     "variacao": "Sempre 16:9 horizontal (3840x2160). Não gerar versão vertical."}),
                "prompt_pt_para_revisao": f.get("imagem_pt_revisao", ""),
            },
            "prompt_video": {
                "modelo_alvo": f.get("modelo_video", "Sora / Veo 3 / Kling 2.x / Runway Gen-4 / Luma"),
                "prompt_en": prompt_video,
                "negative_prompt_en": f.get("video_negativo_en",
                    "text, subtitles, captions, burned-in words, lower thirds, titles, watermark, jump cuts, morphing faces, extra fingers, flicker, jitter, "
                    "camera shake, speed ramp, cartoon physics"),
                "parametros": f.get("parametros_video",
                    {"duracao_s": 5, "fps": 24, "movimento_camera": f.get("camera_en", "slow cinematic dolly-in"),
                     "loop": "final neutro para emenda perfeita", "resolucao": "3840x2160"}),
                "prompt_pt_para_revisao": f.get("video_pt_revisao", ""),
            },
            "audio": {
                "sfx": f.get("sfx", []),
                "trilha": f.get("trilha", ""),
                "mixagem": f.get("mixagem", "Voz do narrador em primeiro plano, trilha a -18 dB, SFX a -12 dB"),
            },
            "continuidade": f.get("continuidade", "Manter paleta, pincel e iluminação do frame anterior."),
        })

    n_frames = len(frames)
    episodio = {
        "id": numero,
        "projeto": "Bíblia Completa — Roteiro Cinematográfico",
        "titulo": cur["titulo"],
        "temporada": plano["temporada_nome"] if plano else cur.get("temporada_nome", ""),
        "livro": cur.get("nome_livro") or (POR_SLUG[slug]["nome_pt"] if slug else cur.get("nome_livro", "")),
        "passagem": cur.get("referencia", ""),
        "idioma_falas": "Português do Brasil (PT-BR)",
        "narrador": cur.get("narrador", {
            "personagem": "DEUS (a voz do Criador narrando a própria obra)",
            "perspectiva": "primeira pessoa do singular",
            "timbre": "voz masculina grave, serena, onisciente, com autoridade e ternura",
            "referencias_de_tom": ["Morgan Freeman", "Liam Neeson", "voz de documentário épico"],
            "ritmo": "lento e solene; pausas longas; nunca apressado",
            "direcao": "Cada fala deve caber em 5 segundos (até ~20 palavras). Sem gritos. O poder está na calma.",
            "idioma": "PT-BR neutro, sem sotaque regional",
        }),
        "especificacoes_tecnicas": {
            "frames": n_frames,
            "segundos_por_frame": SEGUNDOS_POR_FRAME,
            "duracao_total_s": n_frames * SEGUNDOS_POR_FRAME,
            "proporcoes": ["16:9 (3840x2160) — formato único, sempre horizontal"],
            "fps": 24,
            "estilo_base_imagem_en": ESTILO_BASE_EN,
            "estilo_base_video_en": ESTILO_VIDEO_BASE_EN,
        },
        "conceito_visual": cur.get("conceito_visual",
            "Deus pinta cada quadro: realismo de pintura a óleo, com um pincel flutuante que acabou de passar "
            "pela tela. Deus nunca aparece — apenas o rastro do pincel. No vídeo, a câmera entra na pintura e "
            "a cena ganha vida tridimensional."),
        "texto_biblico_do_episodio": original,
        "frames": frames,
        "producao": {
            "status": cur.get("status", "roteiro_completo"),
            "gerado_por": "ferramentas/03_gerar_episodio.py",
            "observacoes": cur.get("observacoes", []),
        },
    }
    return episodio


def validar(ep: dict) -> list:
    problemas = []
    if len(ep["frames"]) != FRAMES_POR_EPISODIO:
        problemas.append(f"{ep['id']}: {len(ep['frames'])} frames (esperado {FRAMES_POR_EPISODIO})")
    for f in ep["frames"]:
        palavras = f["falas"]["narrador_palavras"]
        if palavras > 22:
            problemas.append(f"{ep['id']} frame {f['frame']}: narração com {palavras} palavras (limite ~20 em 5 s)")
        if not f["prompt_imagem"]["prompt_en"] or not f["prompt_video"]["prompt_en"]:
            problemas.append(f"{ep['id']} frame {f['frame']}: prompt vazio")
    return problemas


def gerar(numeros: list):
    corpus = carregar_corpus()
    with open(INDICE, encoding="utf-8") as fh:
        indice = json.load(fh)
    os.makedirs(SAIDA, exist_ok=True)
    todos_problemas = []
    for numero in numeros:
        ep = montar_episodio(numero, corpus, indice)
        caminho = os.path.join(SAIDA, f"{numero}.json")
        with open(caminho, "w", encoding="utf-8") as fh:
            json.dump(ep, fh, ensure_ascii=False, indent=1)
        problemas = validar(ep)
        todos_problemas += problemas
        print(f"✔ {numero}: {ep['titulo']} — {len(ep['frames'])} frames — {caminho}")
    if todos_problemas:
        print("\n⚠ Avisos de validação:")
        for p in todos_problemas:
            print("  -", p)
    else:
        print("\nTudo validado: 12 frames por episódio, narração dentro do tempo, prompts preenchidos.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] == "--todos":
        numeros = sorted(a[:-5] for a in os.listdir(CURADORIA) if a.endswith(".json")) if os.path.isdir(CURADORIA) else []
    else:
        numeros = args
    if not numeros:
        print("Nenhuma curadoria encontrada em roteiro/curadoria/.")
    else:
        gerar(numeros)
