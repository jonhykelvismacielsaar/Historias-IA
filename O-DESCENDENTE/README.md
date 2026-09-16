# 🦁 O DESCENDENTE — pacote de produção (Episódios 1–3)

Série em **7 frames × 8 segundos por episódio** para **Seedance 1.5**, com prompts de imagem,
prompts de vídeo com falas cronometradas em português e fichas travadas de personagem/voz.

## COMO USAR (ordem de leitura)

1. **`00-BIBLIA-DA-SERIE.md`** — regras de formato, cronograma do frame de 8 s, os dois mundos,
   as 12 tribos e bestas, poderes, amuleto, arco geral.
2. **`01-PERSONAGENS-E-VOZES.md`** — BLOCOS TRAVADOS de aparência (copiar e colar em todo prompt)
   + fichas de voz por personagem + prompt negativo global. **É isso que impede o rosto/timbre
   de mudar entre frames.**
3. **`EP01-A-Estrela-que-Nao-Se-Apagou.md`**, **`EP02-O-Vazio-de-Cimento.md`**,
   **`EP03-A-Cela-e-a-Harpa.md`** — cada episódio com 7 frames, e cada frame com:
   - 🖼️ **PROMPT DE IMAGEM** (copie e cole no seu gerador de imagem; use a imagem como primeiro
     frame no Seedance 1.5, modo imagem→vídeo);
   - 🎬 **PROMPT PARA SEEDANCE 1.5** com câmera, ação segundo a segundo, **falas em PT-BR com
     janela de tempo exata (1.0s–6.5s)** e descrição da voz travada por personagem.
4. **`frames/`** — imagens de referência de cada frame (21 arquivos: `EPxx-F0y.png`).

## STATUS DAS IMAGENS
- ✅ EP01 F01–F07 (7/7)
- ✅ EP02 F01 (1/7) — **F02–F07 continuam na próxima leva**
- ⏳ EP03 F01–F07 — **próxima leva**

## REGRAS RÁPIDAS (leia antes de gerar qualquer coisa)
- Frame de 8 s = fala só entre **1.0s e 6.5s**. Nunca fora disso.
- Mundo REAL = paleta fria/cinza, som seco, sem reverb.
- Mundo dos SONHOS = paleta âmbar/esmeralda, reverb de salão longo nas vozes de lá.
- Cole o **BLOCO TRAVADO** do personagem em todo prompt de vídeo. Sem resumir.
- Cole o **prompt negativo global** (fim de `01-PERSONAGENS-E-VOZES.md`) em todo prompt.
