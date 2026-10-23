# GUIA DE PRODUÇÃO — do frame ao vídeo final

Este guia explica **exatamente** como usar o material dos 3 episódios:
cada plano tem **1 imagem (frame)** + **1 prompt de imagem** + **1 prompt de vídeo de 6 s**.
Você gera a imagem → joga a imagem no gerador de vídeo → junta os 5 clipes → pronto.

---

## 1. FLUXO DE TRABALHO

```
PROMPT DA IMAGEM  →  [gerador de imagem]  →  frame .png
                                              ↓
                       [Seedance / Veo, modo image-to-video]
                                              ↓
                                    clipe de 6 s com áudio
                                              ↓
                         5 clipes = 30 s = 1 episódio
                                              ↓
                              [CapCut / Premiere] montagem
```

## 2. CONFIGURAÇÃO RECOMENDADA NO GERADOR DE VÍDEO

| Parâmetro | Valor |
|---|---|
| Modelo | **Seedance 2.5** (imagem→vídeo) ou **Veo 3.x** |
| Duração | **6 segundos** por clipe (nunca mais, nunca menos) |
| Proporção | **16:9** (horizontal, YouTube) — se for Shorts/Reels, gere 9:16 e reenquadre |
| Resolução | 1080p |
| Áudio | **Ligado** (o prompt já traz som ambiente e diálogo) |
| Modo | *image-to-video* (NÃO text-to-video: a imagem é o que garante a continuidade dos personagens) |
| Movimento de câmera | sempre descrito no prompt — não deixe "automático" |

> **Dica de ouro:** gere o clipe de 6 s **duas vezes** com o mesmo frame e escolha o melhor. A segunda geração corrige mãos, olhos e boca.

> ⚠️ **Por que 6 s e não 8 s?** Seis segundos são o ponto em que os modelos de vídeo ainda obedecem ao prompt até o último quadro. Acima disso eles começam a inventar movimento. O episódio fica em **30 s** — o tamanho ideal de Reels/Shorts — e a montagem fica com corte mais nervoso, que segura a atenção.

## 3. COMO MANTER O JESUS E O TUPÃ IGUAIS DO EP. 1 AO 3

O maior problema de IA é a inconsistência de personagem. Três travas resolvem:

1. **Repetição literal do bloco de personagem** — ele está em TODOS os prompts, palavra por palavra. Não traduza, não resuma, não "melhore".
2. **Nunca** deixe o Tupã sair com barba ou bigode. Ele é **sempre barbeado**. Se o modelo insistir, acrescente "clean-shaven, bare face, no facial hair" e "no tattoos on arms" no prompt, e "barba, bigode, cavanhaque, tatuagem" no negative prompt.
3. **Frame de referência** — quando o gerador permitir (Veo 3 "ingredients", Seedance "referência"), anexe o **key visual** em `imagens/referencias/key-visual.jpg` junto com o prompt.
4. **Ordem no prompt** — sempre coloque **estilo → personagens → ação** nessa ordem. Modelos dão mais peso ao que vem primeiro.
5. **O cabelo do Jesus é o mesmo em todo frame (novo padrão, 23/10):** cacheado, **comprido até os ombros**, preso num **coque baixo despojado na nuca**, com dois ou três cachos soltos emoldurando o rosto. Se o modelo devolver o cabelo solto ou curto, repita: `hair tied in a low bun, longer curly hair, loose curls framing the face`.
6. **O rosto do Tupã precisa ser legível.** Ele é o personagem calado; a emoção dele vive no rosto. Nunca deixe a cabeça dele virada de costas ou de perfil puro: **no máximo 45° de perfil**, olhos visíveis. No prompt de imagem, escreva `head turned three-quarters toward the camera, face clearly visible`.

### BLOCO DE PERSONAGEM (copie igual em tudo)

```
JESUS: homem brasileiro de 30 anos, pele morena clara, cabelo castanho-escuro cacheado e comprido, na altura dos ombros, preso num coque baixo despojado na nuca, com cachos soltos emoldurando o rosto, barba curta, camisa de linho branca de botão com mangas dobradas, calça jeans clara, chinelo de dedo, pulseira de couro no pulso.
TUPÃ: homem indígena de 30 anos, pele morena, rosto COMPLETAMENTE BARBEADO (sem barba, sem bigode, sem cavanhaque), sem tatuagens nos braços, cabelo preto liso na altura dos ombros preso em rabo de cavalo baixo, camiseta regata cinza-escura com UMA faixa horizontal de grafismo geométrico guarani atravessada no peito (losangos e zigue-zagues em terracota e preto) e o mesmo motivo pequeno repetido na barra inferior, calça de sarja, sandália de couro, pulseira de sementes no pulso.
```

## 4. BLOCO DE ESTILO (copie igual em tudo)

```
ESTILO: anime cinematográfico 2D, cel shading limpo, traço fino, fundos pintados à mão no estilo Ghibli x A-1 Pictures, luz brasileira quente, cores saturadas, grão de filme suave, 16:9, sem texto, sem letreiro, sem logo, sem legenda.
```

## 5. NEGATIVE PROMPT UNIVERSAL

Cole isto no campo "negative prompt" (ou no fim do prompt, se a ferramenta não tiver campo):

```
texto, letras, legendas, marca d'água, logo, moldura, colagem, várias cenas no mesmo quadro, 3D, CGI, fotorrealismo, pele plástica, personagens duplicados, mãos deformadas, seis dedos, olhos assimétricos, rosto borrado, derretido, estátua, cruz, crucifixo, igreja, templo, barba no Tupã, bigode, cavanhaque, tatuagem tribal nos braços, estereótipo de índio de cinema, cocar de fantasia, pintura corporal genérica, violência, tristeza
```

> Por que "sem cruz, sem igreja, sem templo"? Porque o modelo tende a transformar "Jesus" em estátua, crucifixo ou pintura barroca. A gente quer **um cara de chinelo**.

## 6. REGRAS DE PROMPT DE VÍDEO (6 s)

Um prompt de 6 segundos precisa das mesmas **5 informações, nesta ordem**:

1. **QUEM + ONDE** (personagem + ambiente)
2. **AÇÃO ÚNICA** (uma só! 6 s não cabe duas)
3. **CÂMERA** (plano fixo / travelling / aproximação lenta / handheld)
4. **AUDIÊNCIA** (som ambiente + diálogo entre aspas + trilha)
5. **ESTILO** (repita o bloco)

**Como distribuir os 6 segundos** (a marcação de tempo no prompt):

| Tempo | O que acontece |
|---|---|
| 0,0 – 1,0 s | o quadro "assenta": a câmera já se move, o personagem respira |
| 1,0 – 4,8 s | a **ação única** e a **fala principal** |
| 4,8 – 6,0 s | reação (um sorriso, um olhar) e o som ambiente fechando |

> Fala mais longa que 4 s **não cabe** em 6 s. Se a frase for grande, divida entre os dois personagens ou corte a última palavra — no roteiro ela aparece inteira, no prompt não.

Erros que estragam o clipe:
- ❌ duas ações simultâneas ("ele abre a porta e depois senta") → o modelo faz as duas ao mesmo tempo. Em 6 s, escolha **uma** ação. Nem tente "primeira metade / segunda metade": não cabe
- ⚠️ 6 s permite **um** micro-evento só (ex.: a chama acender). Dois eventos no mesmo clipe saem embaralhados
- ❌ "câmera cinematográfica" sozinho → câmera voa sem controle
- ❌ diálogo longo → a boca não acompanha. Máximo **7 palavras por fala** e **14 palavras por clipe**
- ❌ pedir choro, grito, corrida → deforma o rosto

## 7. MONTAGEM (CapCut, gratuito)

1. Crie um projeto **1920×1080, 30 fps**.
2. Importe os **5 clipes** na ordem e **trave cada um em exatamente 6,0 s** (30 s no total). Se algum clipe vier com 5 s ou 8 s, **corte/reduza na timeline** em vez de gerar de novo.
3. Coloque uma **trilha única por episódio** por baixo (não música diferente em cada clipe — o corte fica "colado").
4. **Transições:** só corte seco. Use *fade* apenas no 1º e no último plano.
5. **Color grading:** temperatura +8, saturação +5, contraste +5. Mantém o look dourado.
6. **Título:** entra aos 0,5 s do plano 1, sai aos 5 s. Fonte grossa, branca, com sombra.
7. **Legendas queimadas** só nas falas (o público assiste sem som).
8. **Áudio:** música em −18 dB, voz do clipe em −6 dB.
9. Exporte **1080p, 30 fps, H.264**.

## 8. CRONOGRAMA SUGERIDO (1 episódio por dia)

| Etapa | Tempo |
|---|---|
| Gerar 5 frames | 10 min |
| Gerar 5 clipes de 6 s (2 tentativas cada) | 25 min |
| Montagem + trilha | 40 min |
| Revisão | 15 min |

## 9. PUBLICAÇÃO

- **YouTube:** 3 vídeos de 30 s + 1 compilado de 1 min 30 s com os três juntos (o compilado performa melhor no algoritmo).
- **TikTok/Reels:** reenquadre em 9:16 e publique cada episódio inteiro (30 s cabe).
- **Título:** `E se Jesus e Tupã dividissem um apê em Cuiabá? | SANTOS DO CERRADO — Ep. 1`
- **Descrição:** use as 3 primeiras linhas do roteiro como gancho.
- **Thumbnail:** o key visual + texto grande "JESUS E TUPÃ DE FÉRIAS".

---

## 10. AVISO LEGAL / DE BOAS PRÁTICAS

Esta é uma **obra original de ficção e comédia**, inspirada no *gênero* inaugurado por *Saint Young Men* (Hikaru Nakamura / Kodansha). Não reproduz personagens, diálogos, designs ou quadros da obra japonesa. Trata-se de sátira afetuosa e ficção especulativa sobre figuras históricas/religiosas, sem intenção de ofender nenhuma crença. Tupã é tratado com respeito à cosmologia guarani. Se for monetizar, mantenha a nota de "obra de ficção" na descrição.
