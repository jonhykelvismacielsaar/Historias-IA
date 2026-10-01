#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_estudo_fidelidade.py — Estudo de fidelidade textual da Torá (e de toda a Bíblia).

Compara, versículo por versículo, as testemunhas textuais disponíveis:
  * Hebraico massorético (WLC / Aleppo-Leningrado) — com niqqud e te'amim
  * Targum Onkelos (aramaico) — a tradução judaica antiga da Torá
  * Targum Jonathan (aramaico) — Profetas
  * Septuaginta de Swete (grego) — a versão dos LXX
  * Peshitta (siríaco) — versão cristã oriental
  * Almeida Atualizada (português)

Produz:
  estudo/comparacao-tora/<livro>.csv ...... comparação completa, versículo a versículo
  estudo/dados_fidelidade.json ............ métricas por livro e por versículo
  estudo/01-fidelidade-textual-da-tora.md . análise escrita (gerada com dados reais)
"""

from __future__ import annotations

import csv
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_biblia import LIVROS, POR_SLUG, TORA

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(RAIZ, "dados", "processado", "versiculos")
ESTUDO = os.path.join(RAIZ, "estudo")
SAIDA_CSV = os.path.join(ESTUDO, "comparacao-tora")


def carregar(slug: str) -> dict:
    with open(os.path.join(CORPUS, f"{slug}.json"), encoding="utf-8") as fh:
        return json.load(fh)


def palavras(txt: str) -> int:
    return len((txt or "").split())


def analisar_livro(slug: str) -> dict:
    dados = carregar(slug)
    linhas = []
    est = {"he": [], "targum": [], "lxx": [], "peshitta": [], "pt": [], "razao_targum_he": [], "razao_lxx_he": []}
    for cap in sorted(dados["capitulos"], key=int):
        for ver in sorted(dados["capitulos"][cap], key=int):
            v = dados["capitulos"][cap][ver]
            he = v.get("he", "")
            targum = v.get("targum_onkelos", "")
            lxx = v.get("lxx_grego", "")
            pesh = v.get("peshitta", "")
            pt = v.get("pt_aa", "")
            n_he, n_targum, n_lxx, n_pesh, n_pt = map(palavras, (he, targum, lxx, pesh, pt))
            if n_he:
                est["he"].append(n_he)
            if n_targum:
                est["targum"].append(n_targum)
            if n_lxx:
                est["lxx"].append(n_lxx)
            if n_pesh:
                est["peshitta"].append(n_pesh)
            if n_pt:
                est["pt"].append(n_pt)
            if n_he and n_targum:
                est["razao_targum_he"].append(round(n_targum / n_he, 3))
            if n_he and n_lxx:
                est["razao_lxx_he"].append(round(n_lxx / n_he, 3))
            linhas.append({
                "capitulo": int(cap), "versiculo": int(ver),
                "referencia": f"{dados['livro']} {cap}:{ver}",
                "hebraico_mt": he, "hebraico_sem_niqqud": v.get("he_limpo", ""),
                "palavras_hebraico": n_he,
                "targum_onkelos": targum, "palavras_targum": n_targum,
                "septuaginta_grego": lxx, "palavras_lxx": n_lxx,
                "peshitta_siriaco": pesh, "palavras_peshitta": n_pesh,
                "portugues_aa": pt, "palavras_portugues": n_pt,
                "tem_targum": bool(targum), "tem_lxx": bool(lxx), "tem_peshitta": bool(pesh),
            })
    resumo = {
        "livro": dados["livro"], "slug": slug,
        "capitulos": len(dados["capitulos"]), "versiculos": len(linhas),
        "palavras_hebraico_total": sum(est["he"]),
        "palavras_targum_total": sum(est["targum"]),
        "palavras_lxx_total": sum(est["lxx"]),
        "palavras_peshitta_total": sum(est["peshitta"]),
        "palavras_portugues_total": sum(est["pt"]),
        "media_palavras_hebraico": round(statistics.mean(est["he"]), 2) if est["he"] else 0,
        "media_palavras_targum": round(statistics.mean(est["targum"]), 2) if est["targum"] else 0,
        "media_palavras_lxx": round(statistics.mean(est["lxx"]), 2) if est["lxx"] else 0,
        "media_razao_targum_hebraico": round(statistics.mean(est["razao_targum_he"]), 3) if est["razao_targum_he"] else 0,
        "media_razao_lxx_hebraico": round(statistics.mean(est["razao_lxx_he"]), 3) if est["razao_lxx_he"] else 0,
        "versiculos_com_targum": sum(1 for l in linhas if l["tem_targum"]),
        "versiculos_com_lxx": sum(1 for l in linhas if l["tem_lxx"]),
        "versiculos_com_peshitta": sum(1 for l in linhas if l["tem_peshitta"]),
    }
    return resumo, linhas


def principais_diferencas(linhas: list, n: int = 15) -> dict:
    """Encontra os versículos em que o Targum e a LXX mais se afastam da contagem do MT."""
    com_targum = [l for l in linhas if l["palavras_hebraico"] and l["palavras_targum"]]
    com_lxx = [l for l in linhas if l["palavras_hebraico"] and l["palavras_lxx"]]
    mais_expandidos = sorted(com_targum, key=lambda l: l["palavras_targum"] - l["palavras_hebraico"], reverse=True)[:n]
    lxx_mais_longos = sorted(com_lxx, key=lambda l: l["palavras_lxx"] - l["palavras_hebraico"], reverse=True)[:n]
    lxx_mais_curtos = sorted(com_lxx, key=lambda l: l["palavras_lxx"] - l["palavras_hebraico"])[:n]
    return {"targum_mais_expandidos": mais_expandidos, "lxx_mais_longos": lxx_mais_longos, "lxx_mais_curtos": lxx_mais_curtos}


def main():
    os.makedirs(SAIDA_CSV, exist_ok=True)
    os.makedirs(ESTUDO, exist_ok=True)
    resultados = {}
    todas_linhas_tora = []
    for livro in LIVROS:
        slug = livro["slug"]
        resumo, linhas = analisar_livro(slug)
        resultados[slug] = resumo
        if slug in TORA:
            todas_linhas_tora += linhas
            with open(os.path.join(SAIDA_CSV, f"{slug}.csv"), "w", encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(linhas[0].keys()))
                w.writeheader()
                w.writerows(linhas)

    dif = principais_diferencas(todas_linhas_tora, 20)
    dados = {
        "gerado_por": "ferramentas/04_estudo_fidelidade.py",
        "descricao": "Métricas de fidelidade textual comparando hebraico massorético, Targum Onkelos, Septuaginta e Peshitta.",
        "por_livro": resultados,
        "tora_consolidada": {
            "versiculos": len(todas_linhas_tora),
            "palavras_hebraico": sum(l["palavras_hebraico"] for l in todas_linhas_tora),
            "palavras_targum": sum(l["palavras_targum"] for l in todas_linhas_tora),
            "palavras_lxx": sum(l["palavras_lxx"] for l in todas_linhas_tora),
            "palavras_peshitta": sum(l["palavras_peshitta"] for l in todas_linhas_tora),
            "palavras_portugues": sum(l["palavras_portugues"] for l in todas_linhas_tora),
        },
        "principais_diferencas": {
            k: [{kk: ll[kk] for kk in ("referencia", "palavras_hebraico", "palavras_targum", "palavras_lxx",
                                       "hebraico_mt", "targum_onkelos", "septuaginta_grego", "portugues_aa")}
                for ll in v]
            for k, v in dif.items()
        },
    }
    with open(os.path.join(ESTUDO, "dados_fidelidade.json"), "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=1)

    print("=== TORÁ (consolidado) ===")
    for k, v in dados["tora_consolidada"].items():
        print(f"  {k}: {v:,}".replace(",", "."))
    print("\n=== Por livro ===")
    for slug in TORA:
        r = resultados[slug]
        print(f"  {r['livro']:14s} vs={r['versiculos']:5d} | palavras HE={r['palavras_hebraico_total']:6d} "
              f"TARGUM={r['palavras_targum_total']:6d} LXX={r['palavras_lxx_total']:6d} "
              f"PESH={r['palavras_peshitta_total']:6d} PT={r['palavras_portugues_total']:6d} | "
              f"razão Targum/HE={r['media_razao_targum_hebraico']:.3f} LXX/HE={r['media_razao_lxx_hebraico']:.3f}")
    print("\n=== 5 versículos mais expandidos pelo Targum Onkelos ===")
    for l in dif["targum_mais_expandidos"][:5]:
        print(f"  {l['referencia']}: HE {l['palavras_hebraico']} → TARGUM {l['palavras_targum']}")


if __name__ == "__main__":
    main()
