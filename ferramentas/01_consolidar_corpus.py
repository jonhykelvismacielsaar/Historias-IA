#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_consolidar_corpus.py — Reúne todas as fontes originais num corpus alinhado.

Fontes lidas (pasta dados/bruto/):
  * morphhb/wlc/*.xml ............ Hebraico massorético (Westminster Leningrad Codex / OSHB) — AT
  * biblia-master/json/*.json .... Português (Almeida Atualizada, ACF, NVI)
  * sblgnt/*.txt ................. Grego do NT (SBLGNT via MorphGNT)
  * lxx_swete/*.csv .............. Septuaginta de Swete (1909) — grego do AT
  * aramaic_atlas/data/corpora/ .. Aramaico: Targum Onkelos, Targum Jonathan, Targum dos Escritos,
                                   Peshitta (AT e NT, em siríaco) e aramaico bíblico
Saída (pasta dados/processado/versiculos/):
  <slug>.json  — todos os versículos do livro, em todas as versões disponíveis.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_biblia import (LIVROS, NOME_ARAMAICO_PARA_SLUG, POR_PT_ABBREV, POR_SBLGNT,
                        POR_WLC, limpar_servos_para_json, normalizar_consoantes,
                        remover_niqqud)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRUTO = os.path.join(RAIZ, "dados", "bruto")
SAIDA = os.path.join(RAIZ, "dados", "processado")

VERSAO_PT_PADRAO = "aa"   # Almeida Atualizada (domínio público) — pode trocar p/ acf ou nvi


# ---------------------------------------------------------------------------
# Hebraico massorético (WLC / OSHB)
# ---------------------------------------------------------------------------
def ler_hebraico() -> dict:
    resultado = {}
    pasta = os.path.join(BRUTO, "morphhb", "wlc")
    NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"

    def coletar(elemento, partes):
        """Percorre o versículo em ordem, restaurando maqqef (־) e sof pasuq (׃)."""
        tag = elemento.tag.split("}")[-1]
        if tag == "note":
            return
        if tag == "w":
            texto = (elemento.text or "").replace("/", "")
            partes.append(texto)
            return
        if tag == "seg":
            tipo = elemento.get("type", "")
            texto = (elemento.text or "").replace("/", "")
            if tipo == "x-maqqef" and partes:
                partes[-1] = partes[-1] + "־"
            elif texto.strip():
                partes.append(texto.strip())
            return
        for filho in elemento:
            coletar(filho, partes)

    for arq in sorted(os.listdir(pasta)):
        if not arq.endswith(".xml") or arq == "VerseMap.xml":
            continue
        livro = POR_WLC.get(arq[:-4])
        if not livro:
            continue
        tree = ET.parse(os.path.join(pasta, arq))
        raiz_xml = tree.getroot()
        versos = {}
        for verso in raiz_xml.iter(f"{NS}verse"):
            osis_id = verso.get("osisID")           # ex.: Gen.1.1
            if not osis_id:
                continue
            partes = osis_id.split(".")
            cap, ver = int(partes[1]), int(partes[2])
            palavras = []
            for filho in verso:
                coletar(filho, palavras)
            texto = " ".join(p for p in palavras if p).strip()
            texto = limpar_servos_para_json(texto)
            if not texto:
                continue
            versos.setdefault(cap, OrderedDict())[ver] = {
                "he": texto,
                "he_limpo": normalizar_consoantes(texto),
                "he_sem_vogais": remover_niqqud(texto).strip(),
            }
        resultado[livro["slug"]] = versos
    return resultado


# ---------------------------------------------------------------------------
# Português
# ---------------------------------------------------------------------------
def ler_portugues(versao: str = VERSAO_PT_PADRAO) -> dict:
    caminho = os.path.join(BRUTO, "biblia-master", "json", f"{versao}.json")
    with open(caminho, encoding="utf-8-sig") as fh:
        dados = json.load(fh)
    resultado = {}
    for bloco in dados:
        livro = POR_PT_ABBREV.get(bloco["abbrev"])
        if not livro:
            continue
        versos = {}
        for i_cap, capitulo in enumerate(bloco["chapters"], start=1):
            for i_ver, texto in enumerate(capitulo, start=1):
                if texto:
                    versos.setdefault(i_cap, OrderedDict())[i_ver] = texto.strip()
        resultado[livro["slug"]] = versos
    return resultado


# ---------------------------------------------------------------------------
# Grego do NT (SBLGNT / MorphGNT)
# ---------------------------------------------------------------------------
def ler_grego_nt() -> dict:
    resultado = {}
    pasta = os.path.join(BRUTO, "sblgnt")
    for arq in sorted(os.listdir(pasta)):
        if not arq.endswith("-morphgnt.txt"):
            continue
        sigla = arq.split("-")[1]
        livro = POR_SBLGNT.get(sigla)
        if not livro:
            continue
        versos = {}
        with open(os.path.join(pasta, arq), encoding="utf-8") as fh:
            for linha in fh:
                campos = linha.split()
                if len(campos) < 4:
                    continue
                bcv = campos[0]
                cap, ver = int(bcv[2:4]), int(bcv[4:6])
                palavra = campos[3]
                versos.setdefault(cap, OrderedDict()).setdefault(ver, []).append(palavra)
        resultado[livro["slug"]] = {
            cap: OrderedDict((v, " ".join(p)) for v, p in vs.items())
            for cap, vs in versos.items()
        }
    return resultado


# ---------------------------------------------------------------------------
# Septuaginta (Swete 1909)
# ---------------------------------------------------------------------------
def ler_lxx() -> dict:
    base = os.path.join(BRUTO, "lxx_swete")
    # id da palavra -> texto
    palavras = {}
    with open(os.path.join(base, "01-Swete_word_with_punctuations.csv"), encoding="utf-8") as fh:
        for linha in fh:
            partes = linha.rstrip("\n").split("\t")
            if len(partes) >= 2 and partes[0].isdigit():
                palavras[int(partes[0])] = partes[1]
    # id inicial -> referência
    marcos = []
    with open(os.path.join(base, "00-Swete_versification.csv"), encoding="utf-8") as fh:
        for linha in fh:
            partes = linha.rstrip("\n").split("\t")
            if len(partes) >= 2 and partes[0].isdigit():
                marcos.append((int(partes[0]), partes[1]))
    marcos.sort()
    resultado = {}
    for i, (id_ini, ref) in enumerate(marcos):
        id_fim = marcos[i + 1][0] if i + 1 < len(marcos) else (max(palavras) + 1)
        try:
            livro_abrev, resto = ref.split(".")
            cap, ver = resto.split(":")
            cap, ver = int(cap), int(ver)
        except ValueError:
            continue
        # Os nomes dos livros na versificação Swete seguem o padrão inglês abreviado
        from lib_biblia import NOME_ARAMAICO_PARA_SLUG
        slug = NOME_ARAMAICO_PARA_SLUG.get(livro_abrev)
        if not slug:
            slug = MAPA_LXX.get(livro_abrev)
        if not slug:
            continue
        texto = " ".join(palavras.get(k, "") for k in range(id_ini, id_fim)).strip()
        if texto:
            resultado.setdefault(slug, {}).setdefault(cap, OrderedDict())[ver] = texto
    return resultado


# Códigos de livro usados na versificação da Septuaginta de Swete (1909).
# Inclui os livros deuterocanônicos, também lidos por este script.
MAPA_LXX = {
    # Cânon protestante
    "Gen": "genesis", "Exo": "exodo", "Lev": "levitico", "Num": "numeros", "Deu": "deuteronomio",
    "Jos": "josue", "Jdg": "juizes", "Rut": "rute", "1Sa": "1samuel", "2Sa": "2samuel",
    "1Ki": "1reis", "2Ki": "2reis", "1Ch": "1cronicas", "2Ch": "2cronicas", "Ezr": "esdras",
    "Neh": "neemias", "Est": "ester", "Job": "jo", "Psa": "salmos", "Pss": "salmos",
    "Pro": "proverbios", "Ecc": "eclesiastes", "Sol": "cantares", "Isa": "isaias",
    "Jer": "jeremias", "Lam": "lamentacoes", "Eze": "ezequiel", "Dan": "daniel",
    "Hos": "oseias", "Joe": "joel", "Amo": "amos", "Oba": "obadias", "Jon": "jonas",
    "Mic": "miqueias", "Nah": "naum", "Hab": "habacuque", "Zep": "sofonias", "Hag": "ageu",
    "Zec": "zacarias", "Mal": "malaquias",
    # Deuterocanônicos / apócrifos de AT (também cobertos pela Septuaginta)
    "Tob": "tobias", "Jdt": "judite", "Wis": "sabedoria", "Sir": "eclesiastico", "Bar": "baruc",
    "1Ma": "1macabeus", "2Ma": "2macabeus", "3Ma": "3macabeus", "4Ma": "4macabeus",
    "1Es": "1esdras", "2Es": "2esdras", "Epj": "epistola_de_jeremias", "Sut": "susana",
    "Bel": "bel_e_o_dragao", "Ode": "odas", "Sip": "sabedoria", "Dat": "daniel", "Bet": "ester",
}


# ---------------------------------------------------------------------------
# Aramaico (Targum Onkelos/Jonathan/Escritos, Peshitta, aramaico bíblico)
# ---------------------------------------------------------------------------
def ler_aramaico() -> dict:
    corpora = os.path.join(BRUTO, "aramaic_atlas", "data", "corpora")
    resultado = {}
    arquivos = {
        "targum_onkelos.csv":  "targum_onkelos",
        "targum_jonathan.csv": "targum_jonathan",
        "targum_writings.csv": "targum_writings",
        "peshitta_nt.csv":     "peshitta",
        "peshitta_ot.csv":     "peshitta",
        "biblical_aramaic.csv": "aramaico_biblico",
    }
    for arquivo, chave in arquivos.items():
        caminho = os.path.join(corpora, arquivo)
        if not os.path.exists(caminho):
            continue
        with open(caminho, encoding="utf-8") as fh:
            for linha in csv.DictReader(fh):
                slug = NOME_ARAMAICO_PARA_SLUG.get(linha["book"])
                if not slug:
                    continue
                cap, ver = int(linha["chapter"]), int(linha["verse"])
                texto = linha["syriac"].strip()
                if not texto:
                    continue
                resultado.setdefault(slug, {}).setdefault(cap, OrderedDict()).setdefault(ver, {})[chave] = texto
    return resultado


# ---------------------------------------------------------------------------
# Consolidação
# ---------------------------------------------------------------------------
def consolidar():
    print("Lendo hebraico massorético (WLC/OSHB)…")
    he = ler_hebraico()
    print("  livros:", len(he), "| versículos:", sum(len(v) for l in he.values() for v in l.values()))

    print(f"Lendo português ({VERSAO_PT_PADRAO.upper()})…")
    pt = ler_portugues()
    print("  livros:", len(pt), "| versículos:", sum(len(v) for l in pt.values() for v in l.values()))

    print("Lendo grego do NT (SBLGNT)…")
    gr = ler_grego_nt()
    print("  livros:", len(gr), "| versículos:", sum(len(v) for l in gr.values() for v in l.values()))

    print("Lendo Septuaginta (Swete)…")
    lxx = ler_lxx()
    print("  livros:", len(lxx), "| versículos:", sum(len(v) for l in lxx.values() for v in l.values()))

    print("Lendo corpora aramaicos (Targum / Peshitta)…")
    ar = ler_aramaico()
    print("  livros:", len(ar), "| versículos:", sum(len(v) for l in ar.values() for v in l.values()))

    os.makedirs(os.path.join(SAIDA, "versiculos"), exist_ok=True)
    estatisticas = {}

    for livro in LIVROS:
        slug = livro["slug"]
        caps = set()
        for fonte in (he, pt, gr, lxx, ar):
            caps.update(fonte.get(slug, {}).keys())
        if not caps:
            continue
        dados_livro = {
            "livro": livro["nome_pt"],
            "slug": slug,
            "nome_hebraico": livro["nome_he"],
            "ordem": livro["ordem"],
            "testamento": livro["tent"],
            "grupo": livro["grupo"],
            "fontes": [],
            "capitulos": {},
        }
        disponiveis = []
        if slug in he:  disponiveis.append("hebraico_mt")
        if slug in ar:  disponiveis.append("aramaico")
        if slug in lxx: disponiveis.append("septuaginta_lxx")
        if slug in pt:  disponiveis.append(f"portugues_{VERSAO_PT_PADRAO}")
        if slug in gr:  disponiveis.append("grego_sblgnt")
        dados_livro["fontes"] = disponiveis

        n_versos = 0
        for cap in sorted(caps):
            versos_cap = {}
            numeros = set()
            for fonte in (he, pt, gr, lxx, ar):
                numeros.update(fonte.get(slug, {}).get(cap, {}).keys())
            for ver in sorted(numeros):
                registro = OrderedDict()
                if ver in he.get(slug, {}).get(cap, {}):
                    registro.update(he[slug][cap][ver])
                if ver in ar.get(slug, {}).get(cap, {}):
                    for k, v in ar[slug][cap][ver].items():
                        registro[k] = v
                if ver in lxx.get(slug, {}).get(cap, {}):
                    registro["lxx_grego"] = lxx[slug][cap][ver]
                if ver in gr.get(slug, {}).get(cap, {}):
                    registro["grego_sblgnt"] = gr[slug][cap][ver]
                if ver in pt.get(slug, {}).get(cap, {}):
                    registro[f"pt_{VERSAO_PT_PADRAO}"] = pt[slug][cap][ver]
                if registro:
                    versos_cap[str(ver)] = registro
                    n_versos += 1
            if versos_cap:
                dados_livro["capitulos"][str(cap)] = versos_cap

        dados_livro["estatisticas"] = {
            "capitulos": len(dados_livro["capitulos"]),
            "versiculos": n_versos,
            "palavras_hebraico": sum(
                len(v.get("he_limpo", "").split())
                for cs in dados_livro["capitulos"].values() for v in cs.values()
            ),
        }
        estatisticas[slug] = dados_livro["estatisticas"]
        with open(os.path.join(SAIDA, "versiculos", f"{slug}.json"), "w", encoding="utf-8") as fh:
            json.dump(dados_livro, fh, ensure_ascii=False, indent=1)

    total_caps = sum(e["capitulos"] for e in estatisticas.values())
    total_vers = sum(e["versiculos"] for e in estatisticas.values())
    total_palavras = sum(e["palavras_hebraico"] for e in estatisticas.values())
    resumo = {
        "gerado_por": "ferramentas/01_consolidar_corpus.py",
        "versao_portugues": VERSAO_PT_PADRAO,
        "livros": len(estatisticas),
        "capitulos": total_caps,
        "versiculos": total_vers,
        "palavras_hebraico_AT": total_palavras,
        "detalhe_por_livro": estatisticas,
    }
    with open(os.path.join(SAIDA, "indice_corpus.json"), "w", encoding="utf-8") as fh:
        json.dump(resumo, fh, ensure_ascii=False, indent=1)
    print(f"\nOK: {len(estatisticas)} livros | {total_caps} capítulos | {total_vers} versículos")
    print("Saída em:", os.path.join(SAIDA, "versiculos"))


if __name__ == "__main__":
    consolidar()
