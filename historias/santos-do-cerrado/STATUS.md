# STATUS DO PROJETO — SANTOS DO CERRADO

Atualizado em: 23/10/2026 · **Formato final: 5 clipes de 8 s por episódio (40 s)**

---

## ✅ PRONTO — temporada 1 completa

| Item | Situação |
|---|---|
| Pesquisa do anime original (Saint Onii-san) | ✅ |
| Bíblia da história | ✅ |
| Guia de produção (Seedance/Veo + CapCut) | ✅ |
| Roteiro dos 3 episódios reformatado em 5 clipes de 8 s | ✅ |
| Prompts de imagem e de vídeo (15 + 15) | ✅ |
| **Frames gerados** | **15 de 15 possíveis** ✅ |

### Frames prontos

| Episódio | Frames | Observação |
|---|---|---|
| 01 — Quarenta Graus | `c01` a `c05` ✅ + 5 alternativas | ok |
| 02 — A Festa do Bairro | `c01` a `c05` ✅ | ok |
| 03 — O Ipê do Estacionamento | `c01` a `c05` ✅ | corrigido (Tupã duplicado e barba) |

> Os frames antigos do Ep. 01 (12 planos) ficaram em `imagens/ep01/alternativas/` e servem como banco extra.

---

## ✅ Uniformização do figurino do Tupã (23/10)

A camiseta do Tupã aparecia com **4 estampas diferentes** entre as imagens. Padronizei todas para o **figurino canônico**: regata cinza-escura com **uma faixa horizontal de grafismo guarani no peito** (losangos e zigue-zagues terracota e preto) + o mesmo motivo pequeno na barra.

Frames refeitos: `ep01/c02`, `ep01/c03`, `ep01/c05` (também trocou o short por calça), `ep02/c02`, `ep02/c04`, `ep03/c02`, `ep03/c03`.

**Referência canônica do figurino:** `imagens/ep01/c02.jpg`. Use-a como imagem de referência ao gerar qualquer cena nova.

## ✅ Correções aplicadas (23/10)

- `ep03/c02` — Tupã estava **com barba** → regerado **sem barba**.
- `ep03/c05` — Tupã **duplicado** → regerado com **exatamente dois personagens** e sem barba.
- `ep01/c03` — tinha **cruz na parede** e **tatuagens** no Tupã → regerado, quadro limpo.
- `ep03` — numeração dos frames estava **deslocada** em relação aos clipes → reordenada (`c01` terreno, `c02` os três na calçada, `c03` Tupã escutando a árvore, `c04` água na raiz/luz na terra, `c05` o ipê florido). Os frames fora de ordem viraram **extras** em `imagens/ep03/alternativas/`.

## 🎬 Dois formatos de prompt de vídeo (23/10)

Criado o **`03-prompts-de-video.md`** com 30 prompts prontos para os 15 clipes:

- **Prompt A — primeiro + último frame:** você entrega `cXX.jpg` e `cXX-fim.jpg`; o modelo interpola o movimento. Usa Seedance 2.0 / Kling / Veo no modo *first & last frame*. Diálogos com marca de tempo inclusos.
- **Prompt B — imagem única com fala:** uma imagem só, para **Google Omni Flash** e **Seedance 1.5 Pro**. Movimento, câmera, fala em PT-BR e som descritos no texto.

### Frames de fim

| Episódio | Fim | Falta |
|---|---|---|
| 01 | `c01-fim` a `c05-fim` ✅ | nada |
| 02 | `c01-fim` a `c04-fim` ✅ | `c05-fim` |
| 03 | — | `c01-fim` a `c05-fim` |

Os 6 prompts que faltam estão no **Anexo** do `03-prompts-de-video.md`.

## ⚠️ PRÓXIMA CONVERSA — só isto:

1. Gerar os **6 frames de fim que faltam** (`ep02/c05-fim` + `ep03/c01-fim` a `c05-fim`) — prompts no Anexo do `03-prompts-de-video.md`.
2. *(Opcional)* Gerar o **key visual** dos dois personagens em `imagens/referencias/key-visual.jpg` — pose neutra, fundo claro, corpo inteiro — para usar como imagem de referência e travar a consistência nos geradores de vídeo.
3. *(Opcional)* Gerar as **falas em áudio** para dublagem.
4. *(Temporada 2)* A figura de terno claro e chapéu de palha, plantada no fim do Ep. 03.

---

## 🔧 Regras de continuidade

Copiar **literalmente** o bloco de personagem e o de estilo do `02-guia-de-producao.md`. Não parafrasear. Se o gerador permitir, usar **seed fixo** e anexar o key visual como referência.

**Tupã é sempre barbeado** (sem barba, sem bigode, sem cavanhaque) e **sem tatuagens nos braços**. **Jesus é o único com barba.** Sempre que a imagem for de interior, evitar cruz/crucifixo na parede — não é o tom da série.

**Figurino fixo do Tupã:** regata cinza-escura com uma faixa horizontal de grafismo guarani no peito + motivo pequeno na barra; calça de sarja escura; sandália de couro; pulseira de sementes. Nunca variar a estampa.
