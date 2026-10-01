# A HISTÓRIA — Roteiro audiovisual da Bíblia, de Gênesis a Apocalipse

Série em **português brasileiro**, com texto traduzido **directamente do hebraico e do grego originais**
— nunca de traduções já publicadas —, com **narração de Deus (a Voz, sem face)** e prompts prontos para
gerar imagens e vídeos com fala em modelos de IA (Seedance 1.5).

---

## 🎬 COMECE POR AQUI

| # | Arquivo | O que é |
|---|---------|---------|
| 1 | **`roteiro/01_EP01_CRIACAO.md`** | ⭐ **EPISÓDIO 01 — A CRIAÇÃO.** Gênesis 1:1–2:3, com o **texto hebraico exato**, tradução literal própria verso por verso, notas de tradução, narração de Deus em pt-BR e decupagem completa |
| 2 | **`roteiro/02_EP02_EDEN.md`** | ⭐ **EPISÓDIO 02 — O ÉDEN.** Gênesis 2:4–25, com a **primeira fala humana da Bíblia** |
| 3 | **`prompts/EP01_EP02_prompts_IMAGEM.md`** | **78 prompts de imagem** (um por quadro dos dois episódios) |
| 4 | **`prompts/EP01_EP02_prompts_SEEDANCE.md`** | **78 prompts de vídeo** com as **falas em português brasileiro** |
| 5 | **`prompts/00_GUIA_DE_PROMPTS_IMAGEM_E_VIDEO.md`** | Como escrever os prompts, configurações do Seedance e fichas de personagem |
| 6 | **`roteiro/00_INDICE_GERAL_BIBLIA.md`** | **Roteiro geral: 12 Atos e 77 episódios cobrindo a Bíblia inteira** |
| 7 | **`fontes/REFERENCIAS_VISUAIS.md`** | Acervo de imagens, regras de fidelidade histórica e licenças |

**Duas imagens-modelo já geradas** (prontas para usar como *first frame* no Seedance):
`fontes/referencias_geradas/EP01_cena02_seja_luz.png` e `.../EP02_cena07_primeiro_encontro.png`

---

## 📖 O TEXTO BÍBLICO NAS LÍNGUAS ORIGINAIS — já baixado

Em `dados/` está o **corpus completo**, em domínio público / licença aberta:

| Arquivo | Conteúdo | Versículos |
|---------|----------|-----------|
| `dados/hebraico/WLC.json` | **Antigo Testamento em HEBRAICO** — Westminster Leningrad Codex, os 39 livros | **23.213** |
| `dados/grego/BYZ.json` | **Novo Testamento em GREGO** — Texto Bizantino de Robinson & Pierpont, os 27 livros | **7.953** |
| | | **31.166 versículos** |

Ou seja: **a Bíblia inteira, nos idiomas em que foi escrita, já está no seu banco de dados.**
Nenhum episódio futuro precisa de download. Para rebaixar: `python3 tools/baixar_corpus.py`

---

## 🗂 ESTRUTURA DO REPOSITÓRIO

```
Historias-IA/
├── README.md                      ← este arquivo
├── roteiro/
│   ├── 00_INDICE_GERAL_BIBLIA.md  ← os 77 episódios, Gênesis → Apocalipse
│   ├── 01_EP01_CRIACAO.md         ← roteiro completo (Gn 1:1–2:3)
│   └── 02_EP02_EDEN.md            ← roteiro completo (Gn 2:4–25)
├── prompts/
│   ├── 00_GUIA_DE_PROMPTS_IMAGEM_E_VIDEO.md
│   ├── EP01_EP02_prompts_IMAGEM.md
│   └── EP01_EP02_prompts_SEEDANCE.md
├── dados/                         ← texto bíblico original (offline)
│   ├── hebraico/WLC.json
│   └── grego/BYZ.json
├── fontes/
│   ├── REFERENCIAS_VISUAIS.md     ← regras históricas, licenças, geografia real
│   ├── dore/                      ← 62 gravuras de Gustave Doré (domínio público)
│   ├── referencias_geradas/       ← 2 quadros-modelo prontos
│   └── imagens_referencia/        ← referências de estilo
└── tools/
    ├── baixar_corpus.py           ← baixa o texto original
    └── curar_referencias.sh       ← monta o acervo de referências
```

---

## 🔑 DECISÕES DE PROJETO (leia antes de produzir)

1. **Deus nunca aparece.** A Voz é *luz, vento, fogo e eco* — **nunca** uma figura, rosto, mão ou
   silhueta. É regra absoluta em todos os 77 episódios.
2. **Um falante por clipe.** O Seedance 1.5 tem dificuldade com diálogos de vários personagens na mesma
   tomada — por isso, cada fala tem o seu próprio clipe, em close. Isso está estruturado nos roteiros.
3. **Fidelidade ao original.** Cada cena traz o hebraico/grego **exato**, a transliteração e a tradução
   literal, com **notas explicando cada escolha** — inclusive as palavras que as traduções costumam
   suavizar (*ézer kenegdô*, *tzelá*, *tóhu vavóhu*, *tanninim*, *almá*).
4. **Sem nudez explícita, sem violência explícita.** O texto é respeitado; a imagem é composta
   (contraluz, névoa, folhagem, enquadramento). Preserva o alcance nas plataformas.
5. **Tudo gerado do zero.** O texto é traduzido por este projeto a partir dos originais — se a tradução
   do hebraico/grego divergir de alguma versão publicada, **está documentado o porquê**.

---

## ▶️ COMO PEDIR OS PRÓXIMOS EPISÓDIOS

Basta dizer, por exemplo:

> *"Faça o EP 03 — A Queda (Gênesis 3)"*
> *"Faça os EPs 06 e 07 — O Dilúvio"*
> *"Faça Gênesis 3 até Gênesis 11"*
> *"Faça os Evangelhos, EPs 45 a 52"*

Cada episódio é entregue no mesmo padrão: **texto original + tradução literal + notas + narração da
Voz + decupagem + prompts de imagem + prompts de vídeo com fala.**

---

## ⚖️ LICENÇAS E ATRIBUIÇÃO

- **Texto hebraico** — Westminster Leningrad Codex (WLC), © 1998–2018 J. Alan Groves Center.
  Licença **CC BY 4.0**.
- **Texto grego** — *The New Testament in the Original Greek: Byzantine Textform*, de Maurice A. Robinson
  e William G. Pierpont. **Domínio público**.
- **Gravuras** — Gustave Doré (1832–1883), *La Grande Bible de Tours*. **Domínio público**.
  Digitalização de Felix Just, S.J.; distribuição Nainoia Inc.
- **Traduções, roteiros e prompts** — produzidos neste projeto.

Detalhes completos em `fontes/REFERENCIAS_VISUAIS.md`.
