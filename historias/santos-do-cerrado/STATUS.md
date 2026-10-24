# STATUS DO PROJETO — SANTOS DO CERRADO

Atualizado em 23/10/2026.

## Padrão de produção atual

- **3 episódios × 5 clipes × 5 s = 25 s por episódio** (75 s para os 15 clipes principais, sem transições).
- Cada clipe principal usa **2 imagens**: primeiro frame A + último frame B. Não há formato de imagem única.
- As falas são em **português brasileiro (PT-BR)**, com marcação de tempo e lip-sync; máximo **7 palavras por fala** e **14 por clipe**.
- Vozes fixas incluídas em todos os prompts de clipe: **Jesus** = voz masculina mansa, calma e aveludada; **Tupã** = voz masculina grossa, grave e ressonante como trovão. Manter os blocos sem variação para reforçar consistência entre gerações.
- Existem **14 prompts de transição**, também de 5 s: 12 entre clipes do mesmo episódio e 2 entre episódios. Cada ponte usa o **B do clipe anterior → A do clipe seguinte** e é opcional; acrescenta 5 s à montagem.

## Arquivos prontos

| Entrega | Situação |
|---|---|
| 30 frames da temporada 1 | ✅ 15 imagens A + 15 imagens B |
| Pacote `sequencia/` + índice e pranchas | ✅ 30 arquivos numerados + 3 pranchas |
| `03-prompts-de-video.md` | ✅ 15 prompts separados, 2 imagens, 5 s, falas PT-BR e vozes fixas |
| `04-prompts-de-transicao.md` | ✅ 14 pontes B→A, 5 s cada |
| Roteiros, README, guia, índice e handoff | ✅ atualizados para o padrão novo |
| Estampa canônica do Tupã | ✅ faixa creme larga com formas terracota grandes; anexar `imagens/ep01/c03.jpg` quando ele aparecer |

## Regras de continuidade

- Jesus e Tupã nunca discordam; a piada é a situação, nunca a religião.
- Jesus: cabelo cacheado comprido até os ombros, preso em coque baixo despojado; ele é o único com barba.
- Tupã sempre barbeado, sem tatuagens nos braços e no máximo 45° de perfil.
- Nenhum texto, letra, logo, legenda ou marca d'água nas imagens.
- Copiar literalmente os blocos de personagem e estilo de `02-guia-de-producao.md`; anexar `imagens/ep01/c03.jpg` em todo prompt com Tupã.
- Evitar cruzes/crucifixos em interiores.

## Próximo passo

Gerar os 15 clipes principais com os prompts de `03-prompts-de-video.md`. Depois, decidir na montagem quais das 14 transições opcionais usar. Não é necessário gerar novas imagens.
