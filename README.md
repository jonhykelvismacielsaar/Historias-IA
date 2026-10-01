# Bíblia Completa — Roteiro Cinematográfico em Episódios

Projeto que transforma **a Bíblia inteira** em uma série de episódios de 60 segundos, com o texto nas línguas originais baixado, comparado e traduzido — e cada frame entregue como prompt de imagem e prompt de vídeo em JSON.

> **Conceito visual da série:** *Deus pintando o quadro.* Cada frame é uma pintura a óleo hiper-realista sendo feita **naquele instante** por um pincel flutuante — e Deus nunca aparece, só o rastro de tinta fresca. No vídeo, a câmera **entra na pintura** e a cena ganha vida tridimensional.
>
> **Narrador:** a voz do próprio Deus, em PT-BR, contando a história em primeira pessoa — "Antes de haver tempo, estrelas ou mares, Eu já era".

---

## Números do projeto

| | Quantidade |
|---|---|
| Livros (cânon protestante) | **66** |
| Capítulos | **1.191** |
| Versículos | **32.579** |
| **Episódios (regra: 12 frames × 5 s = 60 s)** | **3.466** |
| Frames = imagens a gerar | **41.592** |
| Duração só do cânon | **57,8 horas** |
| Temporada Extra (69 apócrifos/deuterocanônicos) | +1.865 episódios |
| **TOTAL GERAL** | **5.331 episódios · 63.972 frames · ~89 horas de vídeo** |

---

## O que já está pronto

| Entrega | Onde está |
|---|---|
| ✅ Corpus multilíngue alinhado versículo por versículo | `dados/processado/versiculos/*.json` |
| ✅ Plano completo dos 3.466 episódios | `roteiro/indice_episodios.json` · `roteiro/plano_episodios.csv` |
| ✅ Índice geral legível | `roteiro/INDICE-GERAL.md` |
| ✅ Plano da Temporada Extra (69 obras) | `roteiro/INDICE-TEMPORADA-EXTRA.md` |
| ✅ **Episódio 0 (Prelúdio) pronto em JSON** | `roteiro/episodios/EP-0001.json` |
| ✅ **Episódio 1 (Gênesis 1:1-12) pronto em JSON** | `roteiro/episodios/EP-0002.json` |
| ✅ Estudo de fidelidade textual da Torá | `estudo/01-fidelidade-textual-da-tora.md` |
| ✅ Transcrição de pergaminhos reais e comparação | `estudo/02-pergaminhos-transcricao-e-comparacao.md` |
| ✅ Comparação da Torá versículo a versículo (CSV) | `estudo/comparacao-tora/*.csv` |
| 🔜 Episódios EP-0003 a EP-3466 (gerados a partir do mesmo molde) | `roteiro/curadoria/` |

### O que cada episódio JSON entrega

12 frames, cada um com:

* **tempo** (00:00–00:05, 00:05–00:10 … 00:55–01:00);
* **narração da voz de Deus em PT-BR**, fiel ao versículo, calibrada para caber em 5 s (máx. ~20 palavras);
* **texto bíblico literal** do trecho (legenda);
* **prompt de imagem em inglês** (Midjourney / Flux / SDXL) + prompt negativo + parâmetros;
* **prompt de vídeo em inglês** (Sora / Veo 3 / Kling / Runway / Luma) + prompt negativo + parâmetros;
* **câmera, movimento, luz, SFX, trilha, mixagem e continuidade**;
* **tradução dos prompts em português** para conferência.

Exemplo real (EP-0002, frame 3 — "Haja Luz"):

```json
"prompt_imagem": {
  "prompt_en": "The brush diving into a heavy golden pigment and slashing one single decisive stroke across the black canvas; the stroke does not light the painting, it IS the light… Hyper-realistic cinematic oil painting on coarse linen canvas, thick impasto brushwork… 8k, masterpiece, no text, no watermark.",
  "negative_prompt_en": "text, watermark, signature, letters, numbers, subtitles, logo, human face of God, depiction of the divine figure, cartoon, cgi look…",
  "parametros": { "aspect_ratio": "16:9", "resolucao": "3840x2160", "stylize": 250, "style": "raw" }
},
"prompt_video": {
  "prompt_en": "the camera flies INTO the surface of the painting and the painted brushstrokes bloom into living three-dimensional reality… Movement: the golden stroke tears across the frame leaving real light behind, shadows snap into the corners… Duration 5 seconds.",
  "parametros": { "duracao_s": 5, "fps": 24, "loop": "final neutro para emenda perfeita", "resolucao": "3840x2160" }
}
```

Proporções: **16:9 (3840×2160)** principal e **9:16 (2160×3840)** para Shorts/Reels/TikTok.

---

## As fontes originais baixadas

| Corpo textual | Língua | Origem |
|---|---|---|
| Westminster Leningrad Codex (WLC/OSHB) | Hebraico massorético com niqqud e te'amim | `openscriptures/morphhb` |
| Targum Onkelos · Targum Jonathan · Targum dos Escritos | **Aramaico** | `Jossifresben/aramaic-root-atlas` |
| Peshitta (AT e NT) | Siríaco (aramaico oriental) | idem |
| Septuaginta de Swete (1909) | Grego | `eliranwong/LXX-Swete-1930` |
| SBLGNT / MorphGNT | Grego koiné | `morphgnt/sblgnt` |
| Almeida Atualizada, ACF, NVI | Português | `thiagobodruk/biblia` |
| 69 obras deuterocanônicas e apócrifas (Enoque, Jubileus, Tobias, Macabeus, Siraque, Testamentos…) | Inglês | `scrollmapper/bible_databases_deuterocanonical` |

Para rebaixar tudo: `bash ferramentas/00_baixar_fontes.sh`

---

## Estrutura do repositório

```
dados/
  bruto/                     fontes originais (comprimidas para caber no repositório)
  processado/versiculos/     1 JSON por livro, com todos os versículos em todas as versões
ferramentas/
  00_baixar_fontes.sh        baixa hebraico, aramaico, grego, siríaco, português e apócrifos
  01_consolidar_corpus.py    alinha tudo versículo por versículo
  02_planejar_episodios.py   divide a Bíblia em 3.466 episódios de 12 frames
  03_gerar_episodio.py       monta o JSON final do episódio (curadoria + texto real)
  04_estudo_fidelidade.py    compara hebraico × Targum × Septuaginta × Peshitta × português
  05_planejar_temporada_extra.py  planeja a Temporada 9 (69 obras extra-bíblicas)
  lib_biblia.py              tabelas canônicas e utilidades de texto original
roteiro/
  curadoria/                 a parte criativa de cada episódio (narração, prompts, som)
  episodios/                 os episódios finalizados em JSON
  indice_episodios.json      o plano completo
estudo/
  01-fidelidade-textual-da-tora.md
  02-pergaminhos-transcricao-e-comparacao.md
  dados_fidelidade.json
  comparacao-tora/*.csv      a Torá inteira comparada versículo a versículo
  imagens-pergaminhos/       imagens reais de rolos e manuscritos + ampliações
```

---

## Como usar

```bash
bash ferramentas/00_baixar_fontes.sh          # 1. baixar as fontes (se necessário)
python3 ferramentas/01_consolidar_corpus.py   # 2. alinhar o corpus
python3 ferramentas/02_planejar_episodios.py  # 3. planejar os episódios
python3 ferramentas/03_gerar_episodio.py EP-0001   # 4. montar um episódio
python3 ferramentas/03_gerar_episodio.py --todos   #    ou todos os que têm curadoria
```

Para criar os episódios seguintes, basta copiar um JSON de `roteiro/curadoria/`, trocar a
passagem e escrever a curadoria — o script `03` injeta automaticamente o texto em hebraico,
aramaico, siríaco, grego e português do trecho escolhido.

---

## Situação das temporadas

| Temporada | Conteúdo | Episódios |
|---|---|---|
| **Prelúdio** | A Voz de Deus antes de Gênesis 1:1 — o vazio, o Big Bang e o primeiro traço | 1 ✅ |
| **T1 — Torá** | Gênesis a Deuteronômio | 424 |
| **T2 — Históricos** | Josué a Ester | 612 |
| **T3 — Sapienciais e Poesia** | Jó a Cantares (Salmos com 2 frames por versículo) | 1.067 |
| **T4 — Profetas** | Isaías a Malaquias | 612 |
| **T5 — Evangelhos e Atos** | Mateus a Atos | 451 |
| **T6 — Cartas de Paulo** | Romanos a Filemom | 190 |
| **T7 — Cartas Gerais** | Hebreus a Judas | 66 |
| **T8 — Apocalipse** | Apocalipse | 43 |
| **T9 — Extra** | 69 obras apócrifas/deuterocanônicas (Enoque, Jubileus, Macabeus…) | 1.865 |

---

## Nota sobre honestidade editorial

* A narração respeita o **texto massorético**, e o telespectador pode abrir a Bíblia em português e conferir versículo por versículo.
* Onde as versões antigas divergem (ex.: Gênesis 2:2, Gênesis 4:8, Deuteronômio 32:8), o episódio traz uma **nota de produção** — a variante nunca é misturada ao texto narrado.
* A Temporada 9 é sempre identificada como **extra-bíblica**: são textos que não pertencem ao cânon de 66 livros.
* As transcrições de pergaminhos foram feitas por leitura visual assistida e são **estudo**, não edição crítica certificada.
