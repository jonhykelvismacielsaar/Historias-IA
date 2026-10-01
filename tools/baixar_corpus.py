#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
baixar_corpus.py — Baixa o texto BÍBLICO NAS LÍNGUAS ORIGINAIS para uso offline.

Fontes (ambas de domínio público / licença aberta):
  * Antigo Testamento em HEBRAICO  -> Westminster Leningrad Codex (WLC)
    repo: openscriptures/morphhb  (CC-BY 4.0 — atribuição obrigatória)
  * Novo Testamento em GREGO       -> Robinson & Pierpont, Byzantine Majority Text
    repo: byztxt/byzantine-majority-text  (domínio público)

Uso:
    python3 tools/baixar_corpus.py            # baixa tudo
    python3 tools/baixar_corpus.py --so-genesis

Saída:
    dados/hebraico/WLC.json      {livro: {capitulo: {versiculo: "texto"}}}
    dados/grego/BYZ.json         {livro: {capitulo: {versiculo: "texto"}}}
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

API = "https://api.github.com/repos/{repo}/contents/{path}?ref=master"
BLOB = "https://api.github.com/repos/{repo}/git/blobs/{sha}"
HEADERS = {"User-Agent": "corpus-biblico/1.0", "Accept": "application/vnd.github+json"}

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(RAIZ, "dados")

# ordem canônica dos livros do AT e nome do arquivo no repo morphhb
LIVROS_AT = [
    ("Gênesis", "Gen"), ("Êxodo", "Exod"), ("Levítico", "Lev"), ("Números", "Num"),
    ("Deuteronômio", "Deut"), ("Josué", "Josh"), ("Juízes", "Judg"), ("Rute", "Ruth"),
    ("1 Samuel", "1Sam"), ("2 Samuel", "2Sam"), ("1 Reis", "1Kgs"), ("2 Reis", "2Kgs"),
    ("1 Crônicas", "1Chr"), ("2 Crônicas", "2Chr"), ("Esdras", "Ezra"),
    ("Neemias", "Neh"), ("Ester", "Esth"), ("Jó", "Job"), ("Salmos", "Ps"),
    ("Provérbios", "Prov"), ("Eclesiastes", "Eccl"), ("Cantares", "Song"),
    ("Isaías", "Isa"), ("Jeremias", "Jer"), ("Lamentações", "Lam"),
    ("Ezequiel", "Ezek"), ("Daniel", "Dan"), ("Oseias", "Hos"), ("Joel", "Joel"),
    ("Amós", "Amos"), ("Obadias", "Obad"), ("Jonas", "Jonah"), ("Miqueias", "Mic"),
    ("Naum", "Nah"), ("Habacuque", "Hab"), ("Sofonias", "Zeph"), ("Ageu", "Hag"),
    ("Zacarias", "Zech"), ("Malaquias", "Mal"),
]


def pegar_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def pegar_blob(repo, sha):
    """Retorna o conteúdo bruto (bytes) de um blob do git, mesmo se > 1 MB."""
    data = pegar_json(BLOB.format(repo=repo, sha=sha))
    if data.get("encoding") == "base64":
        return base64.b64decode(data["content"])
    req = urllib.request.Request(data["url"], headers=HEADERS)
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.read()


def baixar_livro_hebraico(repo, nome, arquivo):
    """Baixa um livro do WLC e devolve {cap: {vers: texto_sem_acentuacao_morfologica}}."""
    meta = pegar_json(API.format(repo=repo, path="wlc/" + arquivo + ".xml"))
    bruto = pegar_blob(repo, meta["sha"])
    raiz = ET.fromstring(bruto)
    ns = raiz.tag.split("}")[0] + "}" if "}" in raiz.tag else ""
    livro = {}
    for versiculo in raiz.iter(ns + "verse"):
        osis = versiculo.get("osisID", "")          # Ex.: Gen.1.1
        partes = osis.split(".")
        if len(partes) != 3:
            continue
        _, cap, vers = partes
        # junta o texto de todos os <w> (palavras) ignorando <note> (variantes ketiv/qere)
        pedacos = []
        for no in versiculo.iter():
            if no.tag.endswith("note"):
                continue
            if no.text:
                pedacos.append(no.text)
            if no.tail:
                pedacos.append(no.tail)
        texto = " ".join("".join(pedacos).replace("/", "").split())
        livro.setdefault(cap, {})[vers] = texto
    return nome, livro


def baixar_hebraico(so_genesis=False):
    repo = "openscriptures/morphhb"
    destino = os.path.join(DADOS, "hebraico")
    os.makedirs(destino, exist_ok=True)
    resultado = {}
    lista = LIVROS_AT[:1] if so_genesis else LIVROS_AT
    with ThreadPoolExecutor(max_workers=6) as pool:
        futuros = [pool.submit(baixar_livro_hebraico, repo, n, a) for n, a in lista]
        for i, f in enumerate(futuros, 1):
            nome, livro = f.result()
            resultado[nome] = livro
            cap = len(livro)
            vers = sum(len(v) for v in livro.values())
            print(f"[HEBRAICO {i:>2}/{len(lista)}] {nome:<14} {cap:>3} caps  {vers:>4} vers.")
    caminho = os.path.join(destino, "WLC.json")
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=0)
    print("->", caminho, f"({os.path.getsize(caminho)/1e6:.2f} MB)")
    return resultado


# ----------------------------------------------------------------------------
# Novo Testamento grego — Byzantine Majority Text (Robinson & Pierpont)
# arquivos: csv-unicode/ccat/no-variants/<CODIGO>.csv  ->  chapter,verse,text
# ----------------------------------------------------------------------------
LIVROS_NT = [
    ("Mateus", "MAT"), ("Marcos", "MAR"), ("Lucas", "LUK"), ("João", "JOH"),
    ("Atos", "ACT"), ("Romanos", "ROM"), ("1 Coríntios", "1CO"), ("2 Coríntios", "2CO"),
    ("Gálatas", "GAL"), ("Efésios", "EPH"), ("Filipenses", "PHP"), ("Colossenses", "COL"),
    ("1 Tessalonicenses", "1TH"), ("2 Tessalonicenses", "2TH"), ("1 Timóteo", "1TI"),
    ("2 Timóteo", "2TI"), ("Tito", "TIT"), ("Filemom", "PHM"), ("Hebreus", "HEB"),
    ("Tiago", "JAM"), ("1 Pedro", "1PE"), ("2 Pedro", "2PE"), ("1 João", "1JO"),
    ("2 João", "2JO"), ("3 João", "3JO"), ("Judas", "JUD"), ("Apocalipse", "REV"),
]


def baixar_livro_grego(repo, nome, codigo):
    caminho = "csv-unicode/ccat/no-variants/%s.csv" % codigo
    meta = pegar_json(API.format(repo=repo, path=caminho))
    bruto = pegar_blob(repo, meta["sha"]).decode("utf-8", "replace")
    livro = {}
    for linha in bruto.splitlines()[1:]:
        partes = linha.split(",", 2)
        if len(partes) < 3:
            continue
        cap, vers, texto = partes[0].strip(), partes[1].strip(), partes[2].strip()
        texto = texto.strip('"').strip()
        if not cap.isdigit():
            continue
        livro.setdefault(cap, {})[vers] = texto
    return nome, livro


def baixar_grego():
    repo = "byztxt/byzantine-majority-text"
    destino = os.path.join(DADOS, "grego")
    os.makedirs(destino, exist_ok=True)
    resultado = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futuros = [pool.submit(baixar_livro_grego, repo, n, c) for n, c in LIVROS_NT]
        for i, f in enumerate(futuros, 1):
            nome, livro = f.result()
            if not livro:
                continue
            resultado[nome] = livro
            vers = sum(len(v) for v in livro.values())
            print(f"[GREGO {i:>2}/{len(LIVROS_NT)}] {nome:<18} {len(livro):>3} caps  {vers:>4} vers.")
    caminho = os.path.join(destino, "BYZ.json")
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=0)
    print("->", caminho, f"({os.path.getsize(caminho)/1e6:.2f} MB)")
    return resultado


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--so-genesis", action="store_true")
    ap.add_argument("--hebraico", action="store_true")
    ap.add_argument("--grego", action="store_true")
    args = ap.parse_args()
    tudo = not (args.hebraico or args.grego)
    if tudo or args.hebraico:
        baixar_hebraico(so_genesis=args.so_genesis)
    if (tudo or args.grego) and not args.so_genesis:
        baixar_grego()
    print("concluído.")
