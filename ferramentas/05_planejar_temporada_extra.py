#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_planejar_temporada_extra.py — Planeja a TEMPORADA 9 (Extra):
os 69 livros deuterocanônicos e apócrifos que ficam fora dos 66 livros.

Inclui os textos que o usuário pediu ("até a Kabalá, se possível"): 1 Enoque,
Jubileus, Tobias, Judite, Sabedoria, Eclesiástico (Siraque), 1-4 Macabeus,
Baruc, 1-2 Esdras, Odes de Salomão, Salmos de Salomão, Testamentos dos Doze
Patriarcas, Apocalipse de Abraão, Ascensão de Isaías, José e Asenate e mais.

Saída: roteiro/indice_temporada_extra.json
       roteiro/INDICE-TEMPORADA-EXTRA.md
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import OrderedDict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRUTO = os.path.join(RAIZ, "dados", "bruto", "deutero", "sources", "en")
SAIDA = os.path.join(RAIZ, "roteiro")

FRAMES_POR_EPISODIO = 12
SEGUNDOS_POR_FRAME = 5
VERSICULOS_POR_EPISODIO = 12  # narrativa: 1 versículo por frame

# Classificação por família literária (define o tratamento no roteiro)
FAMILIA = {
    "1-enoch": "apocaliptico", "2-enoch": "apocaliptico", "3-baruch": "apocaliptico",
    "2-baruch": "apocaliptico", "4-baruch": "apocaliptico", "apocalypse-of-abraham": "apocaliptico",
    "apocalypse-of-elijah": "apocaliptico", "apocalypse-of-peter": "apocaliptico",
    "apocalypse-of-sedrach": "apocaliptico", "ascension-of-isaiah": "apocaliptico",
    "book-of-jubilees": "narrativo", "book-of-jasher": "narrativo",
    "book-of-tobit": "narrativo", "book-of-judith": "narrativo", "1-maccabees": "narrativo",
    "2-maccabees": "narrativo", "3-maccabees": "narrativo", "4-maccabees": "narrativo",
    "1-esdras": "narrativo", "2-esdras": "narrativo", "susanna": "narrativo",
    "bel-and-the-dragon": "narrativo", "greek-esther": "narrativo", "azar": "narrativo",
    "book-of-sirach": "sapiencial", "wisdom-of-solomon": "sapiencial",
    "psalms-of-solomon": "poetico", "odes-of-solomon": "poetico", "prayer-of-manasseh": "poetico",
    "five-psalms-of-david": "poetico", "songs-of-the-sabbath-sacrifice": "poetico",
    "genesis-apocryphon": "narrativo", "book-of-giants": "narrativo",
    "joseph-and-asenath": "narrativo", "lives-of-the-prophets": "narrativo",
    "testament-of-abraham": "testamento", "testament-of-isaac": "testamento",
    "testament-of-jacob": "testamento", "testament-of-job": "testamento",
    "testament-of-solomon": "testamento", "testament-of-moses": "testamento",
}

# Prelúdio próprio desta temporada
PRELUDIO_T9 = {
    "id": "EP-EXTRA-0001", "temporada_nome": "T9 — ESCRITOS EXTRA-BÍBLICOS (apócrifos, deuterocanônicos e místicos)",
    "livro": "Prelúdio da Temporada Extra", "referencia": "Prelúdio original — os livros que ficaram de fora",
    "titulo": "Os Livros que Ficaram de Fora do Cânon",
    "genero": "documentario", "frames": FRAMES_POR_EPISODIO, "status": "roteiro_completo_previsto",
    "observacao": ("Episódio de abertura que explica, com honestidade, por que estes 69 livros não estão "
                   "no cânon protestante de 66 livros: os judeus definiram o Tanakh em Yavneh (c. 90 d.C.); "
                   "católicos os chamam de deuterocanônicos; ortodoxos e a Igreja Etíope aceitam vários deles; "
                   "e a Igreja Etíope inclui Enoque e Jubileus no próprio cânon (isso é fato histórico)."),
}


def palavras(txt: str) -> int:
    return len(re.findall(r"[\wÀ-ÿ']+", txt or ""))


def planejar():
    plano = [PRELUDIO_T9]
    detalhe = OrderedDict()

    if not os.path.isdir(BRUTO):
        print("Fontes dos apócrifos não encontradas. Rode: bash ferramentas/00_baixar_fontes.sh")
        return

    numero = 1
    for pasta in sorted(os.listdir(BRUTO)):
        caminho = os.path.join(BRUTO, pasta)
        if not os.path.isdir(caminho):
            continue
        jsons = [f for f in os.listdir(caminho) if f.endswith(".json")]
        if not jsons:
            continue
        with open(os.path.join(caminho, jsons[0]), encoding="utf-8") as fh:
            dados = json.load(fh)
        books = dados.get("books", [])
        if not books:
            continue
        livro = books[0]
        nome = livro.get("name") or pasta
        capitulos = livro.get("chapters", [])
        n_versos = sum(len(c.get("verses", [])) for c in capitulos)
        palavras_total = sum(palavras(v.get("text", "")) for c in capitulos for v in c.get("verses", []))

        # Mesma regra: 12 frames de 5 s = 60 s por episódio
        n_episodios = max(1, -(-n_versos // VERSICULOS_POR_EPISODIO))
        familia = FAMILIA.get(pasta, "outro")

        for i in range(1, n_episodios + 1):
            v_ini = (i - 1) * VERSICULOS_POR_EPISODIO + 1
            v_fim = min(i * VERSICULOS_POR_EPISODIO, n_versos)
            plano.append({
                "id": f"EP-EXTRA-T9-{numero:04d}",
                "temporada_nome": PRELUDIO_T9["temporada_nome"],
                "livro": nome, "familia_literaria": familia,
                "referencia": f"{nome} (parte {i} de {n_episodios})",
                "faixa_versiculos": [v_ini, v_fim],
                "titulo": f"{nome} — parte {i}",
                "genero": familia,
                "frames": FRAMES_POR_EPISODIO,
                "duracao_segundos": FRAMES_POR_EPISODIO * SEGUNDOS_POR_FRAME,
                "status": "planejado",
            })
            numero += 1

        detalhe[nome] = {
            "pasta": pasta, "familia_literaria": familia,
            "capitulos": len(capitulos), "versiculos": n_versos,
            "palavras": palavras_total, "episodios": n_episodios,
        }

    total_seg = len(plano) * FRAMES_POR_EPISODIO * SEGUNDOS_POR_FRAME
    resultado = {
        "projeto": "Temporada 9 — Escritos Extra-Bíblicos",
        "aviso": ("Estes livros NÃO fazem parte do cânon protestante de 66 livros. "
                  "São apresentados como temporada separada e identificados como extra-bíblicos."),
        "totais": {
            "obras": len(detalhe),
            "episodios": len(plano),
            "frames": len(plano) * FRAMES_POR_EPISODIO,
            "duracao_horas": round(total_seg / 3600, 1),
        },
        "obras": detalhe,
        "episodios": plano,
    }

    os.makedirs(SAIDA, exist_ok=True)
    with open(os.path.join(SAIDA, "indice_temporada_extra.json"), "w", encoding="utf-8") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=1)

    linhas = ["# Temporada 9 — Escritos Extra-Bíblicos", "",
              "> **Aviso:** estes livros não fazem parte do cânon protestante de 66 livros.",
              "> São chamados de deuterocanônicos (católicos), apócrifos (protestantes) ou",
              "> parte do cânon (ortodoxos e Igreja Etíope). A série os apresenta numa temporada",
              "> separada, sempre identificados como extra-bíblicos.", "",
              f"- **Obras:** {len(detalhe)}",
              f"- **Episódios:** {len(plano)}",
              f"- **Frames:** {len(plano)*FRAMES_POR_EPISODIO}",
              f"- **Duração:** {total_seg/3600:.1f} horas", "",
              "| Obra | Família literária | Capítulos | Versículos | Episódios |",
              "|---|---|---|---|---|"]
    for nome, d in detalhe.items():
        linhas.append(f"| {nome} | {d['familia_literaria']} | {d['capitulos']} | {d['versiculos']} | {d['episodios']} |")
    with open(os.path.join(SAIDA, "INDICE-TEMPORADA-EXTRA.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas))

    print(f"Temporada 9: {len(detalhe)} obras | {len(plano)} episódios | {total_seg/3600:.1f} horas")
    for nome, d in list(detalhe.items())[:12]:
        print(f"  {nome[:48]:48s} {d['capitulos']:3d} caps {d['versiculos']:5d} vs → {d['episodios']:3d} eps")


if __name__ == "__main__":
    planejar()
