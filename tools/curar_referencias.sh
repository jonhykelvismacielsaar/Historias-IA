#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# curar_referencias.sh — Monta o acervo de referências visuais do projeto.
#
# Fonte: "La Grande Bible de Tours" — 241 gravuras de Gustave Doré (1832-1883),
# digitalizadas por Felix Just, S.J. (catholic-resources.org) e distribuídas pelo
# projeto Aionian Bible. TODAS em DOMÍNIO PÚBLICO (o autor morreu em 1883).
#
# Repositório: https://github.com/Nainoia-Inc/AionianBible_GustaveDore_LaGrandeBibledeTours
#
# O que este script faz:
#   1. Clona o repositório em /tmp (fora do projeto — são 1,5 GB).
#   2. Seleciona as estampas que cobrem a narrativa de Gênesis a Apocalipse.
#   3. Reduz para 1200 px de largura e recomprime em JPEG (fica ~350 KB cada).
#   4. Salva em fontes/dore/ numeradas e nomeadas em português.
#
# Uso:  bash tools/curar_referencias.sh
# ---------------------------------------------------------------------------
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP=/tmp/dore
DEST="$RAIZ/fontes/dore"

if [ ! -d "$TMP/.git" ]; then
  echo ">> clonando o acervo Doré (modo econômico)..."
  git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/Nainoia-Inc/AionianBible_GustaveDore_LaGrandeBibledeTours.git "$TMP"
fi

cd "$TMP"
git sparse-checkout set --no-cone '/*.jpg' 2>/dev/null || true
git checkout --quiet 2>/dev/null || true

mkdir -p "$DEST"

# número no acervo  →  nome em português (ordem narrativa da Bíblia)
MAPA=(
"001|EP01_A-Criacao-a-Luz"
"002|EP02_A-Criacao-de-Eva"
"003|EP03_Adao-e-Eva-expulsos-do-Eden"
"004|EP04_Caim-e-Abel-oferecem-sacrificios"
"006|EP06_O-mundo-destruido-pelas-aguas"
"010|EP08_A-Torre-de-Babel"
"011|EP09_Abraao-vai-para-Canaa"
"012|EP11_Abraao-e-os-tres-anjos"
"013|EP11_Lo-foge-enquanto-Sodoma-arde"
"016|EP12_O-sacrificio-de-Isaque"
"021|EP13_O-sonho-de-Jaco"
"024|EP13_Jaco-luta-com-o-anjo"
"026|EP14_Jose-vendido-pelos-irmaos"
"027|EP14_Jose-interpreta-o-sonho-de-Farao"
"028|EP15_Jose-se-revela-aos-irmaos"
"030|EP16_Moises-crianca-no-Nilo"
"035|EP17_A-decima-praga-deve-conter"
"037|EP18_Os-egipcios-se-afogam-no-mar"
"039|EP19_A-entrega-da-Lei-no-Monte-Sinai"
"041|EP20_Moises-quebra-as-tabuas-da-Lei"
"044|EP22_A-serpente-de-bronze"
"048|EP24_As-muralhas-de-Jerico-caem"
"053|EP25_Josue-manda-o-sol-parar"
"065|EP26_Sansao-e-Dalila"
"071|EP27_Rute-e-Boaz"
"075|EP29_Davi-mata-Golias"
"085|EP32_A-morte-de-Absalao"
"090|EP33_O-julgamento-de-Salomao"
"102|EP34_Elias-sobe-ao-ceu-em-carruagem-de-fogo"
"110|EP40_O-profeta-Isaias"
"114|EP41_O-profeta-Jeremias"
"118|EP42_A-visao-do-vale-de-ossos-secos"
"123|EP43_Sadraque-Mesaque-e-Abednego-na-fornalha"
"125|EP43_Daniel-na-cova-dos-leoes"
"133|EP45_O-Retorno-do-Exilio-Esdras-le-a-Lei"
"136|EP37_Jo-recebe-a-noticia-de-suas-desgracas"
"138|EP44_Jonas-e-vomitado-pela-baleia"
"161|EP46_A-Anunciacao"
"162|EP46_O-nascimento-de-Jesus"
"163|EP46_Os-magos-guiados-pela-estrela"
"167|EP47_Joao-Batista-preg-no-deserto"
"168|EP47_O-batismo-de-Jesus"
"169|EP47_A-tentacao-de-Jesus"
"175|EP49_O-Sermao-do-Monte"
"184|EP51_Jesus-alimenta-a-multidao"
"185|EP51_Jesus-caminha-sobre-o-mar"
"187|EP52_A-Transfiguracao"
"197|EP53_A-ressurreicao-de-Lazaro"
"202|EP55_A-Ultima-Ceia"
"203|EP56_Jesus-ora-no-getsemani"
"205|EP56_Judas-trai-Jesus"
"213|EP57_Jesus-e-pregado-na-cruz"
"215|EP57_A-crucificacao"
"216|EP57_Trevas-na-crucificacao"
"220|EP58_O-anjo-e-as-mulheres-no-tumulo-vazio"
"223|EP59_Jesus-sobe-ao-ceu"
"224|EP60_O-Espirito-Santo-desce-sobre-os-discipulos"
"229|EP61_A-conversao-de-Saulo"
"235|EP63_Paulo-sofre-naufragio"
"236|EP70_Joao-na-ilha-de-Patmos"
"240|EP76_O-Juizo-Final"
"241|EP77_A-Nova-Jerusalem"
)

echo ">> processando ${#MAPA[@]} estampas..."
total=0
for item in "${MAPA[@]}"; do
  num="${item%%|*}"; nome="${item##*|}"
  src=$(ls Gustave-Dore-Bible-Tour-*-"$num"-*.jpg 2>/dev/null | head -1 || true)
  if [ -z "$src" ]; then echo "   !! não encontrado: $num"; continue; fi
  convert "$src" -resize 1000x -quality 78 -strip "$DEST/$nome.jpg"
  total=$((total+1))
done

echo ">> $total imagens gravadas em $DEST"
echo ">> tamanho: $(du -sh "$DEST" | cut -f1)"
