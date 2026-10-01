#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# 00_baixar_fontes.sh — baixa TODAS as fontes originais da Bíblia usadas no projeto
#
# Uso:
#   bash ferramentas/00_baixar_fontes.sh            # baixa e deixa tudo pronto
#   bash ferramentas/00_baixar_fontes.sh --extrair  # só reexpande o que está comprimido
#
# Fontes (todas de licença livre / domínio público):
#   openscriptures/morphhb ......... Hebraico massorético (WLC/OSHB) com niqqud e te'amim
#   thiagobodruk/biblia ............ Português (Almeida Atualizada, ACF, NVI)
#   morphgnt/sblgnt ................ Grego do Novo Testamento (SBLGNT)
#   eliranwong/LXX-Swete-1930 ...... Septuaginta de Swete (1909), grego
#   Jossifresben/aramaic-root-atlas  Aramaico: Targum Onkelos, Targum Jonathan,
#                                    Targum dos Escritos, Peshitta (AT e NT), aramaico bíblico
#   scrollmapper/bible_databases_deuterocanonical ... 69 obras deuterocanônicas e apócrifas
#                                    (Enoque, Jubileus, Tobias, Judite, Macabeus, Siraque...)
# ---------------------------------------------------------------------------
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRUTO="$RAIZ/dados/bruto"
mkdir -p "$BRUTO"
cd "$BRUTO"

baixar() { # repo, branch, arquivo-de-saida
  local repo="$1" branch="$2" saida="$3"
  if [ -f "$saida" ]; then echo "· já existe: $saida"; return; fi
  echo "↓ baixando $repo ($branch)…"
  curl -sL --retry 3 -o "$saida" "https://codeload.github.com/$repo/tar.gz/refs/heads/$branch"
  echo "  ok: $(du -h "$saida" | cut -f1)"
}

extrair() {
  echo "· expandindo arquivos de origem…"
  # Hebraico massorético
  [ -f morphhb_wlc.tgz ] && [ ! -d morphhb/wlc ] && { mkdir -p morphhb && tar xzf morphhb_wlc.tgz -C morphhb; }
  # Grego do NT
  [ -f sblgnt.tgz ] && [ ! -d sblgnt ] && tar xzf sblgnt.tgz
  # Apócrifos / deuterocanônicos
  [ -f deutero.tgz ] && [ ! -d deutero ] && tar xzf deutero.tgz
  # Septuaginta (CSVs comprimidos individualmente)
  for g in lxx_swete/*.csv.gz; do [ -f "$g" ] && [ ! -f "${g%.gz}" ] && gunzip -k "$g"; done
  # Corpora aramaicos
  mkdir -p aramaic_atlas/data/corpora
  for g in aramaico_corpora_gz/*.csv.gz; do [ -f "$g" ] && [ ! -f "aramaic_atlas/data/corpora/$(basename "${g%.gz}")" ] && gunzip -ck "$g" > "aramaic_atlas/data/corpora/$(basename "${g%.gz}")"; done
  echo "· pronto."
}

if [ "${1:-}" != "--extrair" ]; then
  echo "=== 1/2 — Baixando o texto hebraico, grego, aramaico e português ==="
  baixar openscriptures/morphhb master morphhb.tgz
  baixar morphgnt/sblgnt master sblgnt_tmp.tgz
  baixar eliranwong/LXX-Swete-1930 master lxx_swete_tmp.tgz
  baixar thiagobodruk/biblia master biblia_tmp.tgz
  baixar Jossifresben/aramaic-root-atlas main aramaic_atlas_tmp.tgz
  baixar scrollmapper/bible_databases_deuterocanonical master deutero_tmp.tgz

  echo "=== 2/2 — Organizando ==="
  mkdir -p morphhb/wlc
  tar xzf morphhb.tgz --strip-components=1 -C morphhb --wildcards '*/wlc/*' 2>/dev/null || true
  tar xzf sblgnt_tmp.tgz --strip-components=1 -C . --one-top-level=sblgnt 2>/dev/null || { mkdir -p sblgnt && tar xzf sblgnt_tmp.tgz -C sblgnt --strip-components=1; }
  mkdir -p lxx_swete && tar xzf lxx_swete_tmp.tgz -C lxx_swete --strip-components=1
  mkdir -p biblia-master && tar xzf biblia_tmp.tgz -C biblia-master --strip-components=1
  mkdir -p aramaic_atlas && tar xzf aramaic_atlas_tmp.tgz -C aramaic_atlas --strip-components=1
  mkdir -p deutero && tar xzf deutero_tmp.tgz -C deutero --strip-components=1
  rm -f morphhb.tgz sblgnt_tmp.tgz lxx_swete_tmp.tgz biblia_tmp.tgz aramaic_atlas_tmp.tgz deutero_tmp.tgz
fi

extrair
echo
echo "Fontes disponíveis em: $BRUTO"
du -sh "$BRUTO"
echo
echo "Próximo passo:  python3 ferramentas/01_consolidar_corpus.py"
