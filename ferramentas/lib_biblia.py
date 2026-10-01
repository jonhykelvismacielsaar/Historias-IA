#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lib_biblia.py — Tabelas canônicas e utilidades de texto bíblico.

Usada por todos os scripts do projeto "Bíblia Completa — Roteiro Cinematográfico".
Reúne a tabela de livros (ordem canônica, nomes em PT/hebraico, abreviações de
cada fonte: WLC/morphhb, SBLGNT, Targum, Peshitta, Bíblia em português) e as
funções de limpeza de texto hebraico/grego.
"""

from __future__ import annotations

import re
import unicodedata

# ---------------------------------------------------------------------------
# 1. Tabela canônica dos 66 livros (ordem protestante)
# ---------------------------------------------------------------------------
# slug       : identificador usado no projeto (nomes de pasta/arquivo)
# nome_pt    : nome em português
# nome_he    : nome hebraico (quando houver)
# wlc        : nome do arquivo em morphhb/wlc (hebraico massorético)
# pt_abbrev  : abreviação usada no JSON da Bíblia em português (thiagobodruk)
# sblgnt     : nome do arquivo do Novo Testamento grego (MorphGNT/SBLGNT)
# testamento : AT / NT
# grupo      : Torá, Históricos, Sapienciais, Profetas Maiores/Menores, Evangelhos...
LIVROS = [
    # --- TORÁ (Pentateuco) ---
    dict(ordem=1,  slug="genesis",     nome_pt="Gênesis",            nome_he="בְּרֵאשִׁית (Bereshit)",  wlc="Gen",  pt_abbrev="gn",  sblgnt=None, tent="AT", grupo="Torá"),
    dict(ordem=2,  slug="exodo",       nome_pt="Êxodo",              nome_he="שְׁמוֹת (Shemot)",       wlc="Exod", pt_abbrev="ex",  sblgnt=None, tent="AT", grupo="Torá"),
    dict(ordem=3,  slug="levitico",    nome_pt="Levítico",           nome_he="וַיִּקְרָא (Vayikra)",    wlc="Lev",  pt_abbrev="lv",  sblgnt=None, tent="AT", grupo="Torá"),
    dict(ordem=4,  slug="numeros",     nome_pt="Números",            nome_he="בְּמִדְבַּר (Bamidbar)", wlc="Num",  pt_abbrev="nm",  sblgnt=None, tent="AT", grupo="Torá"),
    dict(ordem=5,  slug="deuteronomio",nome_pt="Deuteronômio",       nome_he="דְּבָרִים (Devarim)",    wlc="Deut", pt_abbrev="dt",  sblgnt=None, tent="AT", grupo="Torá"),
    # --- HISTÓRICOS ---
    dict(ordem=6,  slug="josue",       nome_pt="Josué",              nome_he="יְהוֹשֻׁעַ",             wlc="Josh", pt_abbrev="js",  sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=7,  slug="juizes",      nome_pt="Juízes",             nome_he="שׁוֹפְטִים",             wlc="Judg", pt_abbrev="jz",  sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=8,  slug="rute",        nome_pt="Rute",               nome_he="רוּת",                   wlc="Ruth", pt_abbrev="rt",  sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=9,  slug="1samuel",     nome_pt="1 Samuel",           nome_he="שְׁמוּאֵל א׳",           wlc="1Sam", pt_abbrev="1sm", sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=10, slug="2samuel",     nome_pt="2 Samuel",           nome_he="שְׁמוּאֵל ב׳",           wlc="2Sam", pt_abbrev="2sm", sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=11, slug="1reis",       nome_pt="1 Reis",             nome_he="מְלָכִים א׳",            wlc="1Kgs", pt_abbrev="1rs", sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=12, slug="2reis",       nome_pt="2 Reis",             nome_he="מְלָכִים ב׳",            wlc="2Kgs", pt_abbrev="2rs", sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=13, slug="1cronicas",   nome_pt="1 Crônicas",         nome_he="דִּבְרֵי הַיָּמִים א׳",   wlc="1Chr", pt_abbrev="1cr", sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=14, slug="2cronicas",   nome_pt="2 Crônicas",         nome_he="דִּבְרֵי הַיָּמִים ב׳",   wlc="2Chr", pt_abbrev="2cr", sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=15, slug="esdras",      nome_pt="Esdras",             nome_he="עֶזְרָא",                wlc="Ezra", pt_abbrev="ed",  sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=16, slug="neemias",     nome_pt="Neemias",            nome_he="נְחֶמְיָה",              wlc="Neh",  pt_abbrev="ne",  sblgnt=None, tent="AT", grupo="Históricos"),
    dict(ordem=17, slug="ester",       nome_pt="Ester",              nome_he="אֶסְתֵּר",                wlc="Esth", pt_abbrev="et",  sblgnt=None, tent="AT", grupo="Históricos"),
    # --- SAPIENCIAIS / POÉTICOS ---
    dict(ordem=18, slug="jo",          nome_pt="Jó",                 nome_he="אִיּוֹב",                wlc="Job",  pt_abbrev="jó",  sblgnt=None, tent="AT", grupo="Sapienciais"),
    dict(ordem=19, slug="salmos",      nome_pt="Salmos",             nome_he="תְּהִלִּים",             wlc="Ps",   pt_abbrev="sl",  sblgnt=None, tent="AT", grupo="Sapienciais"),
    dict(ordem=20, slug="proverbios",  nome_pt="Provérbios",         nome_he="מִשְׁלֵי",               wlc="Prov", pt_abbrev="pv",  sblgnt=None, tent="AT", grupo="Sapienciais"),
    dict(ordem=21, slug="eclesiastes", nome_pt="Eclesiastes",        nome_he="קֹהֶלֶת",                wlc="Eccl", pt_abbrev="ec",  sblgnt=None, tent="AT", grupo="Sapienciais"),
    dict(ordem=22, slug="cantares",    nome_pt="Cantares",           nome_he="שִׁיר הַשִּׁירִים",       wlc="Song", pt_abbrev="ct",  sblgnt=None, tent="AT", grupo="Sapienciais"),
    # --- PROFETAS MAIORES ---
    dict(ordem=23, slug="isaias",      nome_pt="Isaías",             nome_he="יְשַׁעְיָהוּ",            wlc="Isa",  pt_abbrev="is",  sblgnt=None, tent="AT", grupo="Profetas Maiores"),
    dict(ordem=24, slug="jeremias",    nome_pt="Jeremias",           nome_he="יִרְמְיָהוּ",             wlc="Jer",  pt_abbrev="jr",  sblgnt=None, tent="AT", grupo="Profetas Maiores"),
    dict(ordem=25, slug="lamentacoes", nome_pt="Lamentações",        nome_he="אֵיכָה",                 wlc="Lam",  pt_abbrev="lm",  sblgnt=None, tent="AT", grupo="Profetas Maiores"),
    dict(ordem=26, slug="ezequiel",    nome_pt="Ezequiel",           nome_he="יְחֶזְקֵאל",             wlc="Ezek", pt_abbrev="ez",  sblgnt=None, tent="AT", grupo="Profetas Maiores"),
    dict(ordem=27, slug="daniel",      nome_pt="Daniel",             nome_he="דָּנִיֵּאל",              wlc="Dan",  pt_abbrev="dn",  sblgnt=None, tent="AT", grupo="Profetas Maiores"),
    # --- PROFETAS MENORES ---
    dict(ordem=28, slug="oseias",      nome_pt="Oseias",             nome_he="הוֹשֵׁעַ",               wlc="Hos",  pt_abbrev="os",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=29, slug="joel",        nome_pt="Joel",               nome_he="יוֹאֵל",                 wlc="Joel", pt_abbrev="jl",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=30, slug="amos",        nome_pt="Amós",               nome_he="עָמוֹס",                 wlc="Amos", pt_abbrev="am",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=31, slug="obadias",     nome_pt="Obadias",            nome_he="עֹבַדְיָה",              wlc="Obad", pt_abbrev="ob",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=32, slug="jonas",       nome_pt="Jonas",              nome_he="יוֹנָה",                 wlc="Jonah",pt_abbrev="jn",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=33, slug="miqueias",    nome_pt="Miqueias",           nome_he="מִיכָה",                 wlc="Mic",  pt_abbrev="mq",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=34, slug="naum",        nome_pt="Naum",               nome_he="נַחוּם",                 wlc="Nah",  pt_abbrev="na",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=35, slug="habacuque",   nome_pt="Habacuque",          nome_he="חֲבַקּוּק",              wlc="Hab",  pt_abbrev="hc",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=36, slug="sofonias",    nome_pt="Sofonias",           nome_he="צְפַנְיָה",              wlc="Zeph", pt_abbrev="sf",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=37, slug="ageu",        nome_pt="Ageu",               nome_he="חַגַּי",                 wlc="Hag",  pt_abbrev="ag",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=38, slug="zacarias",    nome_pt="Zacarias",           nome_he="זְכַרְיָה",              wlc="Zech", pt_abbrev="zc",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    dict(ordem=39, slug="malaquias",   nome_pt="Malaquias",          nome_he="מַלְאָכִי",              wlc="Mal",  pt_abbrev="ml",  sblgnt=None, tent="AT", grupo="Profetas Menores"),
    # --- NOVO TESTAMENTO ---
    dict(ordem=40, slug="mateus",      nome_pt="Mateus",             nome_he="מַתִּתְיָהוּ",           wlc=None,   pt_abbrev="mt",  sblgnt="Mt", tent="NT", grupo="Evangelhos"),
    dict(ordem=41, slug="marcos",      nome_pt="Marcos",             nome_he="מַרְקוֹס",               wlc=None,   pt_abbrev="mc",  sblgnt="Mk", tent="NT", grupo="Evangelhos"),
    dict(ordem=42, slug="lucas",       nome_pt="Lucas",              nome_he="לוּקָס",                 wlc=None,   pt_abbrev="lc",  sblgnt="Lk", tent="NT", grupo="Evangelhos"),
    dict(ordem=43, slug="joao",        nome_pt="João",               nome_he="יוֹחָנָן",               wlc=None,   pt_abbrev="jo",  sblgnt="Jn", tent="NT", grupo="Evangelhos"),
    dict(ordem=44, slug="atos",        nome_pt="Atos",               nome_he="מַעֲשֵׂי הַשְּׁלִיחִים",  wlc=None,   pt_abbrev="atos", sblgnt="Ac", tent="NT", grupo="História NT"),
    dict(ordem=45, slug="romanos",     nome_pt="Romanos",            nome_he="אֶל הָרוֹמִיִּים",        wlc=None,   pt_abbrev="rm",  sblgnt="Ro", tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=46, slug="1corintios",  nome_pt="1 Coríntios",        nome_he="אֶל הַקּוֹרִנְתִּים א׳",   wlc=None,   pt_abbrev="1co", sblgnt="1Co",tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=47, slug="2corintios",  nome_pt="2 Coríntios",        nome_he="אֶל הַקּוֹרִנְתִּים ב׳",   wlc=None,   pt_abbrev="2co", sblgnt="2Co",tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=48, slug="galatas",     nome_pt="Gálatas",            nome_he="אֶל הַגָּלָטִים",         wlc=None,   pt_abbrev="gl",  sblgnt="Ga", tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=49, slug="efesios",     nome_pt="Efésios",            nome_he="אֶל הָאֶפֶסִים",          wlc=None,   pt_abbrev="ef",  sblgnt="Eph",tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=50, slug="filipenses",  nome_pt="Filipenses",         nome_he="אֶל הַפִילִפִּים",        wlc=None,   pt_abbrev="fp",  sblgnt="Php",tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=51, slug="colossenses", nome_pt="Colossenses",        nome_he="אֶל הַקּוֹלוֹסִים",        wlc=None,   pt_abbrev="cl",  sblgnt="Col",tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=52, slug="1tessalonicenses", nome_pt="1 Tessalonicenses", nome_he="אֶל הַתַּסְלוֹנִיקִים א׳", wlc=None, pt_abbrev="1ts", sblgnt="1Th", tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=53, slug="2tessalonicenses", nome_pt="2 Tessalonicenses", nome_he="אֶל הַתַּסְלוֹנִיקִים ב׳", wlc=None, pt_abbrev="2ts", sblgnt="2Th", tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=54, slug="1timoteo",    nome_pt="1 Timóteo",          nome_he="אֶל טִימוֹתֵיאוֹס א׳",    wlc=None,   pt_abbrev="1tm", sblgnt="1Ti",tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=55, slug="2timoteo",    nome_pt="2 Timóteo",          nome_he="אֶל טִימוֹתֵיאוֹס ב׳",    wlc=None,   pt_abbrev="2tm", sblgnt="2Ti",tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=56, slug="tito",        nome_pt="Tito",               nome_he="אֶל טִיטוֹס",            wlc=None,   pt_abbrev="tt",  sblgnt="Tit",tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=57, slug="filemom",     nome_pt="Filemom",            nome_he="אֶל פִּילֵימוֹן",         wlc=None,   pt_abbrev="fm",  sblgnt="Phm",tent="NT", grupo="Cartas de Paulo"),
    dict(ordem=58, slug="hebreus",     nome_pt="Hebreus",            nome_he="אֶל הָעִבְרִים",          wlc=None,   pt_abbrev="hb",  sblgnt="Heb",tent="NT", grupo="Cartas Gerais"),
    dict(ordem=59, slug="tiago",       nome_pt="Tiago",              nome_he="יַעֲקֹב",                 wlc=None,   pt_abbrev="tg",  sblgnt="Jas",tent="NT", grupo="Cartas Gerais"),
    dict(ordem=60, slug="1pedro",      nome_pt="1 Pedro",            nome_he="פֶּטְרוֹס א׳",           wlc=None,   pt_abbrev="1pe", sblgnt="1Pe",tent="NT", grupo="Cartas Gerais"),
    dict(ordem=61, slug="2pedro",      nome_pt="2 Pedro",            nome_he="פֶּטְרוֹס ב׳",           wlc=None,   pt_abbrev="2pe", sblgnt="2Pe",tent="NT", grupo="Cartas Gerais"),
    dict(ordem=62, slug="1joao",       nome_pt="1 João",             nome_he="יוֹחָנָן א׳",            wlc=None,   pt_abbrev="1jo", sblgnt="1Jn",tent="NT", grupo="Cartas Gerais"),
    dict(ordem=63, slug="2joao",       nome_pt="2 João",             nome_he="יוֹחָנָן ב׳",            wlc=None,   pt_abbrev="2jo", sblgnt="2Jn",tent="NT", grupo="Cartas Gerais"),
    dict(ordem=64, slug="3joao",       nome_pt="3 João",             nome_he="יוֹחָנָן ג׳",            wlc=None,   pt_abbrev="3jo", sblgnt="3Jn",tent="NT", grupo="Cartas Gerais"),
    dict(ordem=65, slug="judas",       nome_pt="Judas",              nome_he="יְהוּדָה",                wlc=None,   pt_abbrev="jd",  sblgnt="Jud",tent="NT", grupo="Cartas Gerais"),
    dict(ordem=66, slug="apocalipse",  nome_pt="Apocalipse",         nome_he="הִתְגַּלּוּת",            wlc=None,   pt_abbrev="ap",  sblgnt="Re", tent="NT", grupo="Apocalíptico"),
]

POR_ORDEM     = {l["ordem"]: l for l in LIVROS}
POR_SLUG      = {l["slug"]: l for l in LIVROS}
POR_PT_ABBREV = {l["pt_abbrev"]: l for l in LIVROS}
POR_WLC       = {l["wlc"]: l for l in LIVROS if l["wlc"]}
POR_SBLGNT    = {l["sblgnt"]: l for l in LIVROS if l["sblgnt"]}

# Nomes hebraicos/gregos usados nos corpora aramaicos (aramaic-root-atlas)
NOME_ARAMAICO_PARA_SLUG = {
    "Genesis": "genesis", "Exodus": "exodo", "Leviticus": "levitico", "Numbers": "numeros",
    "Deuteronomy": "deuteronomio", "Joshua": "josue", "Judges": "juizes", "Ruth": "rute",
    "1 Samuel": "1samuel", "2 Samuel": "2samuel", "1 Kings": "1reis", "2 Kings": "2reis",
    "1 Chronicles": "1cronicas", "2 Chronicles": "2cronicas", "Ezra": "esdras",
    "Nehemiah": "neemias", "Esther": "ester", "Job": "jo", "Psalms": "salmos",
    "Proverbs": "proverbios", "Ecclesiastes": "eclesiastes", "Song of Songs": "cantares",
    "Isaiah": "isaias", "Jeremiah": "jeremias", "Lamentations": "lamentacoes",
    "Ezekiel": "ezequiel", "Daniel": "daniel", "Hosea": "oseias", "Joel": "joel",
    "Amos": "amos", "Obadiah": "obadias", "Jonah": "jonas", "Micah": "miqueias",
    "Nahum": "naum", "Habakkuk": "habacuque", "Zephaniah": "sofonias", "Haggai": "ageu",
    "Zechariah": "zacarias", "Malachi": "malaquias",
    "Matthew": "mateus", "Mark": "marcos", "Luke": "lucas", "John": "joao",
    "Acts": "atos", "Romans": "romanos", "1 Corinthians": "1corintios",
    "2 Corinthians": "2corintios", "Galatians": "galatas", "Ephesians": "efesios",
    "Philippians": "filipenses", "Colossians": "colossenses",
    "1 Thessalonians": "1tessalonicenses", "2 Thessalonians": "2tessalonicenses",
    "1 Timothy": "1timoteo", "2 Timothy": "2timoteo", "Titus": "tito",
    "Philemon": "filemom", "Hebrews": "hebreus", "James": "tiago", "1 Peter": "1pedro",
    "2 Peter": "2pedro", "1 John": "1joao", "2 John": "2joao", "3 John": "3joao",
    "Jude": "judas", "Revelation": "apocalipse",
}

# ---------------------------------------------------------------------------
# 2. Listas de caracteres para limpeza
# ---------------------------------------------------------------------------
_NIQQUD_E_TEAMIM = re.compile(r"[\u0591-\u05C7\u05EF\uFB1D-\uFB4F]")
_SOFRIM = str.maketrans({"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"})

CANON_66 = [l["slug"] for l in LIVROS]
TORA = ["genesis", "exodo", "levitico", "numeros", "deuteronomio"]


def remover_niqqud(texto_hebraico: str) -> str:
    """Remove niqqud (vogais) e te'amim (acentos de cantilação), mantendo consoantes."""
    return _NIQQUD_E_TEAMIM.sub("", texto_hebraico)


def normalizar_consoantes(texto_hebraico: str) -> str:
    """Versão comparável: sem niqqud/te'amim, sem pontuação massorética, letras finais unificadas."""
    t = remover_niqqud(texto_hebraico)
    t = re.sub(r"[־–—׃|{}\[\]]", " ", t)
    t = re.sub(r"[\u200b-\u200f\u202a-\u202e]", "", t)
    t = t.replace("׀", " ")
    t = t.translate(_SOFRIM)
    return re.sub(r"\s+", " ", t).strip()


def limpar_servos_para_json(texto: str) -> str:
    """Remove marcadores de estrutura do WLC/OSIS que não são texto bíblico."""
    return (texto.replace("{פ}", "").replace("{ס}", "")
                 .replace("(פ)", "").replace("(ס)", "").strip())


def ref(livro_slug: str, capitulo: int, versiculo: int) -> str:
    """Referência legível: 'Gênesis 1:1'."""
    return f"{POR_SLUG[livro_slug]['nome_pt']} {capitulo}:{versiculo}"


def contar_palavras_hebraico(texto: str) -> int:
    return len(normalizar_consoantes(texto).split())


def transliterar_simples(texto_hebraico: str) -> str:
    """Transliteração aproximada (sem vogais) — apenas apoio de leitura, não acadêmica."""
    mapa = {
        "א": "ʾ", "ב": "b", "ג": "g", "ד": "d", "ה": "h", "ו": "w", "ז": "z",
        "ח": "ḥ", "ט": "ṭ", "י": "y", "כ": "k", "ך": "k", "ל": "l", "מ": "m",
        "ם": "m", "נ": "n", "ן": "n", "ס": "s", "ע": "ʿ", "פ": "p", "ף": "p",
        "צ": "ṣ", "ץ": "ṣ", "ק": "q", "ר": "r", "ש": "š", "ת": "t",
    }
    return "".join(mapa.get(c, c if c == " " else "") for c in normalizar_consoantes(texto_hebraico))


def transliterar_grego(texto: str) -> str:
    """Transliteração simplificada do grego (apoio de leitura)."""
    regras = [("ου", "ou"), ("αι", "ai"), ("ει", "ei"), ("οι", "oi"), ("αυ", "au"),
              ("ευ", "eu"), ("ου", "ou"), ("θ", "th"), ("φ", "ph"), ("χ", "ch"),
              ("ψ", "ps"), ("ξ", "x"), ("η", "ē"), ("ω", "ō"), ("υ", "y")]
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    for a, b in regras:
        t = t.replace(a, b)
    return t
