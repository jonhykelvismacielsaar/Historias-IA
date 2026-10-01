# GUIA DE PROMPTS — IMAGEM E VÍDEO (Seedance 1.5)

Como transformar os roteiros deste repositório em imagens e em vídeo com fala, em português brasileiro,
com aparência **ultrarrealista**.

---

## PARTE 1 — O FLUXO DE TRABALHO (3 PASSOS)

```
[1] PROMPT DE IMAGEM  →  gera o QUADRO (still)
        ↓
[2] O QUADRO VIRA A IMAGEM INICIAL (image-to-video)
        ↓
[3] PROMPT DE VÍDEO (Seedance 1.5) → anima + gera a FALA em pt-BR + som ambiente
```

**Por que fazer assim:** no Seedance 1.5, o modo **image-to-video (I2V)** é o que mantém
o **mesmo rosto** do personagem de um clipe para o outro. Se você gerar tudo por texto
(text-to-video), cada vídeo vai inventar um rosto novo e a série fica sem continuidade.
**Gere primeiro a imagem, aprove, e só então anime.**

---

## PARTE 2 — COMO ESCREVER PROMPT DE IMAGEM

Todo prompt de imagem deste projeto segue **6 blocos, nesta ordem**:

```
[1] SUJEITO      quem/o que, idade, etnia, cabelo, olhos, expressão
[2] AÇÃO/POSE    o que ele está fazendo exatamente
[3] AMBIENTE     lugar, época, clima, hora do dia
[4] LUZ/ATMOSFERA direção da luz, cor dominante, partículas no ar
[5] CÂMERA       lente, altura, ângulo, profundidade de campo
[6] ESTILO       "ultra-realistic, photorealistic, 8k, cinematic, shot on ARRI Alexa 65"
```

### Bloco de estilo padrão da série (cole no fim de TODO prompt)
```
ultra-realistic, photorealistic, cinematic, dramatic natural lighting, shallow depth of field,
film grain, shot on ARRI Alexa 65 with Zeiss Prime lenses, 8k detail, skin pores and micro-texture
visible, cinematic color grading, aspect ratio 16:9, no text, no watermark, no logo
```

### Negative prompt padrão (cole no campo negativo)
```
cartoon, anime, 3d render, cgi, plastic skin, waxy, oversaturated, blurry, deformed hands,
extra fingers, extra limbs, text, watermark, signature, modern clothing, wristwatch,
glasses, tattoos, logos, cartoonish clouds
```

### Regras de ouro
1. **Nunca peça rosto de Deus.** Escreva: *"no visible divine figure, only light and atmosphere"*.
2. **Uma ação por imagem.** "Adão regando" — não "Adão regando e olhando para árvore enquanto fala".
3. **Repita a ficha do personagem** sempre (ver bloco `PERSONAGENS` no fim deste arquivo).
4. **Sem objetos anacrônicos:** nada de metal trabalhado, tecido industrial, vidro, papel, tijolo
   na era do Éden. Só pedra, madeira, pele, fibra, folha.
5. **Rostos limpos de oclusão** quando houver fala: boca visível, cabelo fora do rosto,
   três-quartos ou frontal. Isso é obrigatório para o lip-sync funcionar depois.

---

## PARTE 3 — COMO ESCREVER PROMPT DE VÍDEO NO SEEDANCE 1.5

### Especificação técnica da ferramenta (para você configurar)
| Parâmetro | Valor recomendado |
|-----------|-------------------|
| Modelo | **Seedance 1.5 Pro** (é o que gera **áudio + vídeo juntos**, com lip-sync) |
| Modo | **Image-to-Video** (suba a imagem do quadro como *first frame*) |
| `duration` | **5 s** para fala curta · **8–10 s** para fala longa · **4–6 s** para paisagem |
| `resolution` | **720p** para testar · **1080p** para o material final |
| `aspect_ratio` | `16:9` (série) · `9:16` (corte para Reels/TikTok/Shorts) |
| `generate_audio` | **true** (é o recurso principal — sem isso não sai a fala) |
| `camera_fixed` | `true` em close de fala (estabiliza o rosto) · `false` nas paisagens |
| `seed` | Fixe um número por personagem (ex.: Adão = `1144`) para repetir o rosto |

### A ESTRUTURA DE PROMPT QUE FUNCIONA (4 CAMADAS)
O Seedance 1.5 responde a um prompt estruturado em **quatro camadas**, nesta ordem.
E lembre-se: **a fala vai SEMPRE entre aspas duplas.**

```
CAMADA 1 — SUJEITO + AÇÃO
"Adão, homem de 26 anos, pele oliva, cabelo preto ondulado, olhos escuros, agachado junto ao rio,
levantando água com as duas mãos, gotas caindo em câmera lenta"

CAMADA 2 — DIÁLOGO (entre aspas, com idioma e emoção)
Ele diz em português brasileiro, com voz grave e emocionada:
"Esta, desta vez, é osso dos meus ossos e carne da minha carne."

CAMADA 3 — ÁUDIO DO AMBIENTE
"som de rio correndo, pássaros tropicais, vento nas folhas, respiração"

CAMADA 4 — CÂMERA + ESTILO
"câmera fixa em tripé, plano médio, close lento aproximando, luz dourada de amanhecer,
ultrarrealista, cinematográfico, 24fps"
```

### 🔁 O FLUXO COM VÁRIOS FRAMES POR VÍDEO (o mais recomendado)

Cada clipe pode receber **2 ou 3 imagens** (frames), não só uma. Isso dá muito mais controle:
a câmera sabe exatamente onde começar, como se mover e onde terminar.

```
FRAME A (0s)  ──►  FRAME B (meio)  ──►  FRAME C (fim)
     ↑                   ↑                  ↑
  imagem inicial    keyframe intermediário  imagem final
```

**Como pedir isso no prompt de vídeo:** escreva a **linha do tempo com os segundos**, nomeando o frame,
a ação e a fala de cada trecho. Exemplo real deste projeto:

```
CLIPE DE 10 SEGUNDOS · três frames fornecidos: FRAME A (0s), FRAME B (5s), FRAME C (10s).

0s a 5s — FRAME A: [o que acontece neste trecho, incluindo o movimento de câmera]
5s a 10s — FRAME B e depois FRAME C: [o que acontece, como a câmera se move, como termina]

[fala entre aspas, com idioma e emoção]
[som ambiente]
[estilo]
```

**Por que funciona melhor:**
- O modelo **não inventa** o meio da cena: ele interpola entre imagens que você aprovou.
- O **rosto se mantém** porque os keyframes já têm o rosto certo.
- Falas com tempo definido encaixam melhor no lip-sync: você sabe em que segundo ela começa.

**Se a ferramenta só aceitar 2 imagens:** use **FRAME A + FRAME C** e mantenha as descrições do
FRAME B na linha do tempo — o modelo vai gerar aquele trecho por texto.

**Se a ferramenta aceitar apenas 1 imagem:** use o FRAME A como *first frame*.

> 📁 **Os arquivos já montados neste formato:**
> - `prompts/EP01_PRONTO_PARA_COPIAR.md` — 20 blocos / 48 imagens
> - `prompts/EP02_PRONTO_PARA_COPIAR.md` — 18 blocos / 46 imagens
>
> Cada bloco já traz os prompts de imagem e, **logo abaixo**, o prompt de vídeo com os segundos,
> as ações e as falas. É copiar, colar e gerar.

### FÓRMULA DE DIÁLOGO (a mais confiável)
```
[quem fala] + [fala exata entre aspas] + [idioma] + [emoção/tom] + [câmera] + [som] + [restrições]
```

Exemplo pronto:
> Adão, em close médio, diz em português brasileiro, com voz grave, lenta e emocionada:
> **"Esta, desta vez, é osso dos meus ossos, e carne da minha carne."**
> Câmera fixa em tripé, aproximação muito lenta. Som ambiente: vento suave no jardim, água ao longe.
> Ultrarrealista, cinematográfico, 24fps, sem música.

### ⚠️ LIMITAÇÕES CONHECIDAS DO SEEDANCE 1.5 — e como resolvo neste projeto
| Limitação | Solução adotada nos roteiros |
|-----------|------------------------------|
| **Diálogo com 2+ personagens na mesma cena se atrapalha** (o modelo confunde quem fala) | **Nunca coloco dois personagens falando no mesmo clipe.** Cada fala tem o seu próprio clipe, com um personagem só, em close. |
| Fala longa desalinha a boca | Quebro falas longas em **frases de até ~15 palavras** por clipe, no mesmo plano. |
| Falas muito rápidas/emotivas desalinham | Escrevo a instrução de **ritmo**: "fala devagar, pausada, sem pressa". |
| Cantar não funciona bem | Nenhuma cena cantada. Salmos são **recitados**, não cantados. |
| O rosto muda ao longo do clipe | Clipes de **5–8 s**, close médio, movimento contido, `camera_fixed: true`. |
| Imagem de referência contradiz o prompt | O prompt de vídeo descreve **só o movimento e o som** — nunca redescobri a aparência, que já está na imagem. |

### A VOZ (Narrador = Deus, sem face) — como fazer
O Seedance gera vídeo; **a Voz não tem imagem**. Portanto:
1. Grave/sintetize a narração **separadamente** (ElevenLabs, Speechify, sua própria voz com
   processamento). O texto exato está em cada cena dos roteiros, marcado como **NARRAÇÃO DA VOZ**.
2. Aplique: `reverb de catedral curto`, EQ com corte de agudos, camada dupla grave -12 semitons
   a -30 dB para efeito "voz que move o chão".
3. No Seedance, use **`generate_audio: true` com som ambiente só**, e monte a Voz por cima na edição.
   Isso dá **muito mais controle** do que pedir para o modelo gerar a voz de Deus — que sai genérica.
4. **Jamais** gere uma imagem do narrador. A Voz é sempre *silêncio, luz, vento e eco*.

---

## PARTE 4 — FICHAS DE PERSONAGEM (copiar/colar dentro dos prompts)

### `ADAM` — Adão
```
Adam, a 26-year-old Middle-Eastern man, olive-tan skin with visible pores, shoulder-length
dark wavy hair, thick dark eyebrows, deep brown eyes, lean athletic build, short trimmed beard
in later episodes (clean-shaven when newly created), calm intense expression
```

### `EVA` — Eva / a mulher
```
Eve, a 24-year-old Middle-Eastern woman, olive-tan skin with visible pores, long dark
wavy hair parted in the middle, deep brown eyes, oval face, serene curious expression,
soft natural features
```

### `NOAH` — Noé (EP 06–08)
```
Noah, a 480-year-old-looking weathered man (appears 60), deeply tanned leathery skin,
long grey-white braided beard, bushy white eyebrows, bald crown with grey hair on the sides,
broad calloused hands, woolen undyed tunic
```

### `ABRAHAM` — Abrão/Abraão (EP 09–12)
```
Abram, a 75-year-old Semitic man, weathered sun-darkened skin, long white beard streaked
with grey, deep-set dark eyes, tall lean frame, undyed wool tunic with a leather belt,
carries a wooden staff
```

### `MOSES` — Moisés (EP 16–23)
```
Moses, an 80-year-old Hebrew man, dark bronze skin, long white beard, white hair,
strong angular jaw, deep-set eyes with heavy brows, plain linen tunic, wooden staff,
sandal leather
```

### `DAVID` — Davi (EP 28–32)
```
David, a young Israelite man: 17 years old in the Goliath episode (smooth face, sun-bleached
brown hair, tanned skin), 30s as king (short dark beard, long wavy dark hair, deep brown eyes,
scar on left forearm from a lion)
```

### `JESUS` — Yeshua (EP 46–59)
```
Yeshua, a 30-year-old Galilean Jewish man, olive skin weathered by sun, shoulder-length
dark brown hair parted in the middle, full dark beard, dark brown eyes, strong carpenter's
hands, plain undyed linen tunic with a woven seam, leather sandals
```

### `VOZ` — A Voz (nunca visível)
```
NO FIGURE. No face. No silhouette. No hands. No robe. Only: volumetric golden-white light,
moving air, glowing dust particles, water rippling with no wind source
```

---

## PARTE 5 — NOMENCLATURA DOS ARQUIVOS

```
imagens/EP01/cena01_IMG-1.1.png ... cena09_IMG-9.4.png
videos/EP01/cena01_VID-1.1.mp4  ... cena09_VID-9.4.mp4
audio/EP01/narracao_cena01.mp3
```
Manter o mesmo ID nos três lugares permite reeditar qualquer quadro sem quebrar a sequência.
