# STATUS DO PROJETO — SANTOS DO CERRADO

Atualizado em: 23/10/2026 · **Formato final: 5 clipes de 6 s por episódio (30 s)**

---

## 🆕 Mudança de padrão (23/10) — 6 s e o novo cabelo do Jesus

### 1. Todo clipe agora tem **6 segundos** (não 8)

- Episódio = **5 clipes × 6 s = 30 s**.
- O motivo é técnico: acima de 6 s os modelos de vídeo começam a inventar movimento e a boca descola da fala.
- O que mudou nos arquivos: roteiros, guia de produção e `03-prompts-de-video.md` foram **retimados** — marcações `00:00–00:06 … 00:24–00:30`, falas remarcadas dentro dos 6 s e o clipe 04 do Ep. 02 deixou de ter corte interno.
- Onde **não** cabe mais de uma ação em 6 s, a segunda ação passou a ser movimento de câmera contínuo (tilt down), não corte.

### 2. Jesus agora usa o **cabelo amarrado**

| | Antes | Agora |
|---|---|---|
| Cabelo | cacheado solto, na altura da nuca | **cacheado, mais comprido (até os ombros), preso num coque baixo despojado na nuca**, com cachos soltos emoldurando o rosto |

- A referência canônica é o novo **key visual**: `imagens/referencias/key-visual.jpg`.
- O bloco de personagem do `02-guia-de-producao.md` já foi atualizado — copie de lá, não invente variação.

### 3. Estampa canônica da regata do Tupã (corrigida em 23/10)

As imagens geradas **do zero** (fora do fluxo de edição) voltaram com a estampa **errada**: zigue-zague fino e pálido em vez dos triângulos terracota. Corrigi `ep02/c05-fim` e `ep03/c01-fim`, e daí em diante passei a **anexar `imagens/ep01/c03.jpg` como referência** em todo prompt com o Tupã.

**Estampa oficial:** faixa larga no peito em fundo creme, com **triângulos e losangos terracota grandes e saturados**, contornada por duas linhas finas terracota; motivo menor na barra; corpo da regata cinza-escuro.

### 4. Tupã — rosto sempre legível

A imagem de fim do Ep. 01 (`ep01/c05-fim.jpg`) tinha o Tupã com a cabeça **virada demais, quase de costas**. Foi regerada: agora ele aparece **em três quartos, rosto visível**. Virou regra: o Tupã nunca passa de **45° de perfil**.

---

## 📊 Onde estamos

| Item | Situação |
|---|---|
| Pesquisa do anime original (Saint Onii-san) | ✅ |
| Bíblia da história (cabelo novo do Jesus) | ✅ |
| Guia de produção (Seedance/Veo + CapCut, 6 s) | ✅ |
| Roteiros dos 3 episódios em 5 clipes de 6 s | ✅ |
| `03-prompts-de-video.md` retimado para 6 s | ✅ |
| Key visual dos dois personagens | ✅ `imagens/referencias/key-visual.jpg` |
| Pacote de produção (`sequencia/`) | ✅ 30 frames numerados + 3 pranchas |

### Frames

| Episódio | Início | Fim |
|---|---|---|
| 01 — Quarenta Graus | ✅ c01–c05 | ✅ c01–c05 |
| 02 — A Festa do Bairro | ✅ c01–c05 | ✅ c01–c05 |
| 03 — O Ipê do Estacionamento | ✅ c01–c05 | ✅ c01–c05 |

**Temporada 1 completa: 30 de 30 frames.**

> **Regra usada para decidir quais frames refazer:** só os frames em que o **Jesus aparece**. Frames sem ele (cidade, parede, Saci no galho, Tupã sozinho na árvore) foram mantidos — o figurino e o rosto do Tupã não mudaram.

## ✅ PRONTO — temporada 1 completa

| Item | Situação |
|---|---|
| Pesquisa do anime original (Saint Onii-san) | ✅ |
| Bíblia da história | ✅ |
| Guia de produção (Seedance/Veo + CapCut) | ✅ |
| Roteiro dos 3 episódios reformatado em 5 clipes de 6 s | ✅ |
| Prompts de imagem e de vídeo (15 + 15) | ✅ retimados para 6 s |
| **Frames de início** | **15 de 15** ✅ |
| **Frames de fim** | **15 de 15** ✅ |
| **Pacote de produção** | ✅ `sequencia/` — 30 arquivos numerados + pranchas |

> Os frames antigos do Ep. 01 (12 planos) ficaram em `imagens/ep01/alternativas/` e servem como banco extra.

---

## ✅ Uniformização do figurino do Tupã (23/10)

A camiseta do Tupã aparecia com **4 estampas diferentes** entre as imagens. Padronizei todas para o **figurino canônico**: regata cinza-escura com **uma faixa horizontal de grafismo guarani no peito** (losangos e zigue-zagues terracota e preto) + o mesmo motivo pequeno na barra.

Frames refeitos: `ep01/c02`, `ep01/c03`, `ep01/c05` (também trocou o short por calça), `ep02/c02`, `ep02/c04`, `ep03/c02`, `ep03/c03`.

**Referência canônica do figurino:** `imagens/ep01/c02.jpg`. Use-a como imagem de referência ao gerar qualquer cena nova.

## ✅ Correções aplicadas (23/10)

- `ep02/c03` — tinha um **pingente de cruz** no peito do Jesus → removido, decote limpo.
- `ep03/c02` — Tupã estava **com barba** → regerado **sem barba**.
- `ep03/c05` — Tupã **duplicado** → regerado com **exatamente dois personagens** e sem barba.
- `ep01/c03` — tinha **cruz na parede** e **tatuagens** no Tupã → regerado, quadro limpo.
- `ep03` — numeração dos frames estava **deslocada** em relação aos clipes → reordenada (`c01` terreno, `c02` os três na calçada, `c03` Tupã escutando a árvore, `c04` água na raiz/luz na terra, `c05` o ipê florido). Os frames fora de ordem viraram **extras** em `imagens/ep03/alternativas/`.

## 🎬 Formato ÚNICO de prompt de vídeo: 2 imagens (23/10)

O `03-prompts-de-video.md` foi reescrito e agora tem **só um tipo de prompt**, 15 no total:

- **Primeiro + último frame:** você entrega `...-A-inicio.jpg` e `...-B-fim.jpg`; o modelo interpola o movimento. Seedance 2.0 / Kling / Veo no modo *first & last frame*, **6 s**, com falas marcadas no tempo.
- **O formato de imagem única (Prompt B / Omni Flash) foi removido** — manter dois formatos duplicava o trabalho sem ganho real em 6 s.
- Cada bloco do arquivo traz os **dois nomes de arquivo** logo acima do prompt (🟢 imagem 1, 🔴 imagem 2), então não há como confundir qual prompt usa quantas imagens.

### Frames de fim

| Episódio | Fim | Falta |
|---|---|---|
| 01 | `c01-fim` a `c05-fim` ✅ | nada |
| 02 | `c01-fim` a `c04-fim` ✅ | `c05-fim` |
| 03 | — | `c01-fim` a `c05-fim` |

Os 6 prompts que faltam estão no **Anexo** do `03-prompts-de-video.md`.

## ⚠️ PRÓXIMA CONVERSA — só isto:

1. **Gerar os 15 vídeos** de 6 s a partir de `sequencia/` (2 imagens por clipe) — nada de imagem nova é necessário.
2. *(Opcional)* Gerar as **falas em áudio** para dublagem.
3. *(Temporada 2)* A figura de terno claro e chapéu de palha, plantada no fim do Ep. 03.

---

## 🔧 Regras de continuidade

Copiar **literalmente** o bloco de personagem e o de estilo do `02-guia-de-producao.md`. Não parafrasear. Se o gerador permitir, usar **seed fixo** e anexar o key visual como referência.

**Tupã é sempre barbeado** (sem barba, sem bigode, sem cavanhaque) e **sem tatuagens nos braços**. **Jesus é o único com barba.** Sempre que a imagem for de interior, evitar cruz/crucifixo na parede — não é o tom da série.

**Cabelo do Jesus (padrão 23/10):** cacheado, **comprido até os ombros**, preso num **coque baixo** na nuca, com cachos soltos emoldurando o rosto. Nunca solto, nunca curto.

**Rosto do Tupã:** no máximo **45° de perfil**. Ele fala pouco, então a emoção tem que estar visível — nada de cabeça virada para o fundo.

**Figurino fixo do Tupã:** regata cinza-escura com uma faixa horizontal de grafismo guarani no peito + motivo pequeno na barra; calça de sarja escura; sandália de couro; pulseira de sementes. Nunca variar a estampa.
