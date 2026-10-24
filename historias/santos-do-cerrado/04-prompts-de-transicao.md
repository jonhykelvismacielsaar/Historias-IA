# PROMPTS DE TRANSIÇÃO — do **último frame de um clipe** para o **primeiro frame do próximo**

São **14 prompts de ponte**, todos de **5 segundos**, no mesmo formato de 2 imagens: você entrega a **imagem B** de um clipe e a **imagem A** do clipe seguinte, e o modelo cria o movimento que liga um no outro.

| | |
|---|---|
| **Quando usar** | quando você quiser que o corte "respire" — a passagem de um lugar para outro, ou de um horário para outro |
| **Quando NÃO usar** | se o episódio estiver longo demais. O corte seco também funciona: as duas imagens já foram desenhadas para casar |
| **Duração** | **5 s cada**. Se usar as 4 transições internas de um episódio, ele passa de 25 s para 45 s |

> **Atenção:** transição **não substitui** o clipe. Ela entra **entre** dois clipes. Se você usar as 12 internas + as 2 viradas de episódio, a temporada vai de 75 s para 145 s.

---

## Como identificar um prompt de transição

Todo bloco aqui usa **duas imagens que já existem** e traz no cabeçalho de onde elas vêm:

    ## T03 · SALA → RUA NA CHUVA
    
    🟢 PRIMEIRO FRAME (imagem 1, o B do clipe anterior): sequencia/06-ep01-clipe03-B-fim.jpg
    🔴 ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):   sequencia/07-ep01-clipe04-A-inicio.jpg
    ⏱️ Duração: 5,0 s · Ep. 01 · clipe 03 → clipe 04

- Prefixo **`T`** = transição interna do episódio.
- Prefixo **`X`** = virada de um episódio para o outro.
- O prompt traz `FIRST FRAME` e `LAST FRAME` descritos como **"exatamente o frame X, sem mudar nada"** — é isso que garante o encaixe perfeito no corte.

> **Regra de ouro da transição:** o primeiro e o último frame **não podem ser redesenhados**. Não peça "mais ou menos assim": é a imagem exata. Se o modelo tentar reenquadrar, gere de novo.

---

## Vozes

Transição **não tem fala** — é passagem de câmera, e boca falando em cima de travelling descola. Por isso o bloco `VOICES` aparece igual em todos, como reserva: se em alguma transição você quiser uma frase curta, é só acrescentar em `SPEECH` respeitando as mesmas vozes.

```text
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
```

---

## Lista das 14 transições

| Imagem 1 (B do clipe) | Imagem 2 (A do clipe) | Ligação | Nome |
|---|---|---|---|
| `02-ep01-clipe01-B-fim.jpg` | `03-ep01-clipe02-A-inicio.jpg` | Ep. 01 · clipe 01 → clipe 02 | FACHADA → SALA VAZIA |
| `04-ep01-clipe02-B-fim.jpg` | `05-ep01-clipe03-A-inicio.jpg` | Ep. 01 · clipe 02 → clipe 03 | SALA → O VENTILADOR |
| `06-ep01-clipe03-B-fim.jpg` | `07-ep01-clipe04-A-inicio.jpg` | Ep. 01 · clipe 03 → clipe 04 | SALA → RUA NA CHUVA |
| `08-ep01-clipe04-B-fim.jpg` | `09-ep01-clipe05-A-inicio.jpg` | Ep. 01 · clipe 04 → clipe 05 | RUA → VARANDA |
| `12-ep02-clipe01-B-fim.jpg` | `13-ep02-clipe02-A-inicio.jpg` | Ep. 02 · clipe 01 → clipe 02 | MURO → QUINTAL |
| `14-ep02-clipe02-B-fim.jpg` | `15-ep02-clipe03-A-inicio.jpg` | Ep. 02 · clipe 02 → clipe 03 | QUINTAL → COZINHA |
| `16-ep02-clipe03-B-fim.jpg` | `17-ep02-clipe04-A-inicio.jpg` | Ep. 02 · clipe 03 → clipe 04 | COZINHA → NOITE NA FOGUEIRA |
| `18-ep02-clipe04-B-fim.jpg` | `19-ep02-clipe05-A-inicio.jpg` | Ep. 02 · clipe 04 → clipe 05 | CHÃO → SACI NO GALHO |
| `22-ep03-clipe01-B-fim.jpg` | `23-ep03-clipe02-A-inicio.jpg` | Ep. 03 · clipe 01 → clipe 02 | TERENO → OS TRÊS |
| `24-ep03-clipe02-B-fim.jpg` | `25-ep03-clipe03-A-inicio.jpg` | Ep. 03 · clipe 02 → clipe 03 | CALÇADA → TUPÃ NO TRONCO |
| `26-ep03-clipe03-B-fim.jpg` | `27-ep03-clipe04-A-inicio.jpg` | Ep. 03 · clipe 03 → clipe 04 | ENTARDECER → NOITE NA RAIZ |
| `28-ep03-clipe04-B-fim.jpg` | `29-ep03-clipe05-A-inicio.jpg` | Ep. 03 · clipe 04 → clipe 05 | AMANHECER → O IPÊ FLORIDO |
| `10-ep01-clipe05-B-fim.jpg` | `11-ep02-clipe01-A-inicio.jpg` | Ep. 01 (fim) → Ep. 02 (início) | VIRADA DO EP. 01 PARA O EP. 02 |
| `20-ep02-clipe05-B-fim.jpg` | `21-ep03-clipe01-A-inicio.jpg` | Ep. 02 (fim) → Ep. 03 (início) | VIRADA DO EP. 02 PARA O EP. 03 |

---

## Como gerar

1. Localize a transição pelo nome (ex.: `T03 · SALA → RUA NA CHUVA`).
2. Suba as **duas imagens** indicadas, no modo *first & last frame*.
3. Cole o prompt e trave **5,0 s**.
4. Se o movimento sair com "pulo" de enquadramento, gere de novo — o problema é o modelo tentando reenquadrar, não o prompt.

> **Dica de montagem:** as transições internas combinam com som contínuo por cima (a trilha não corta). As duas viradas de episódio (`X01` e `X02`) são o lugar natural para entrar a **cartela de título** na edição.

---

# AS 12 TRANSIÇÕES INTERNAS


## T01 · FACHADA → SALA VAZIA

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/02-ep01-clipe01-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/03-ep01-clipe02-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 01 · clipe 01 → clipe 02

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: the camera pushes in from the street toward the old building, slips through the open ground-floor door, crosses a dim stairwell and emerges into the empty living room, where the rectangle of sunlight is already lying on the beige tile. The sidewalk boxes and the truck slide out of frame behind the camera.
CAMERA: one continuous forward push-in, no cuts, no zoom, steady and slow.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: street noise fading out, door creak, footsteps on stairs, then the hot hush of the empty apartment.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T02 · SALA → O VENTILADOR

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/04-ep01-clipe02-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/05-ep01-clipe03-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 01 · clipe 02 → clipe 03

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: the afternoon light slides down the wall and turns amber; Jesus walks from the sofa to the old table fan, drops to a crouch in front of it and puts his palms on the grille; Tupã drifts to the door frame and leans there. The sofa stays where it was.
CAMERA: slow lateral drift to the right that settles into the static framing of the fan.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: room tone, flip-flops on tile, the click of the fan switch, cicadas getting louder.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T03 · SALA → RUA NA CHUVA

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/06-ep01-clipe03-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/07-ep01-clipe04-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 01 · clipe 03 → clipe 04

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: Jesus turns toward the window; in two seconds the sky goes dark and the light in the room turns blue-gray. The camera follows him to the window and pushes through the frame, becoming the rainy street outside, where the first drops hit the puddles and the children run in from the right.
CAMERA: follow move to the window that turns into a push-through, ending on the wide street shot.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: cicadas cut off, wind rising, first heavy drop on the zinc roof, then the downpour starting.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T04 · RUA → VARANDA

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/08-ep01-clipe04-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/09-ep01-clipe05-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 01 · clipe 04 → clipe 05

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: the camera pulls back out of the rain and into the building, glides along the corridor wall and out onto the small balcony, where Tupã is already leaning on the wet parapet; Jesus steps out beside him, soaked, and shakes his curls. Rain keeps falling the whole way.
CAMERA: smooth pull-back and lateral dolly that settles on the two men at the parapet.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: rain heavy on the roof, water dripping from gutters, distant thunder, the children's laughter fading.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T05 · MURO → QUINTAL

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/12-ep02-clipe01-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/13-ep02-clipe02-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 02 · clipe 01 → clipe 02

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: Dona Nilza walks off to the right and the two men follow her around the corner of the house; the camera trails them into the backyard, past the strings of pennants, until Jesus is already up on the aluminum ladder, tying a flag and laughing. Tupã plants himself at the base of the ladder.
CAMERA: tracking shot from behind the three that opens into the wide backyard framing.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: pennants snapping, flip-flops on dirt, accordion getting closer, people chatting.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T06 · QUINTAL → COZINHA

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/14-ep02-clipe02-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/15-ep02-clipe03-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 02 · clipe 02 → clipe 03

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: the camera slips away from the ladder, crosses the party and goes through the kitchen door; the noise of the yard drops behind the wall and the smell of hot cheese bread takes over, with Jesus already at the table, flour on his face, hands in the dough.
CAMERA: one continuous dolly through the party into the kitchen, decelerating into a frontal medium shot.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: party muffled behind the wall, oven humming, dough squelching, trays clinking.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T07 · COZINHA → NOITE NA FOGUEIRA

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/16-ep02-clipe03-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/17-ep02-clipe04-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 02 · clipe 03 → clipe 04

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: a time-lapse: the daylight drains out of the kitchen window, the lamps and lanterns come on one by one, and the camera travels from the table of cheese bread out to the yard, where Tupã is already crouched in front of the tall pile of firewood at night.
CAMERA: continuous forward dolly with a time-lapse light change, ending on the static low shot of the firewood.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: afternoon birds turning into crickets, lanterns buzzing, the party band tuning up in the distance.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T08 · CHÃO → SACI NO GALHO

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/18-ep02-clipe04-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/19-ep02-clipe05-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 02 · clipe 04 → clipe 05

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: from the abandoned flip-flops on the dirt, the camera rises along the mango trunk, through the dark leaves, and finds the Saci sitting high on the branch with the stolen flip-flops dangling from his finger.
CAMERA: one continuous tilt up along the trunk, ending on the medium shot of the Saci in the branch.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: fire crackling below, leaves rustling, a short high-pitched giggle getting closer.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T09 · TERENO → OS TRÊS

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/22-ep03-clipe01-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/23-ep03-clipe02-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 03 · clipe 01 → clipe 02

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: the camera pushes in slowly on the three people on the sidewalk until the framing closes from wide to medium; Dona Nilza keeps pointing at the dead tree, Jesus and Tupã settle beside her with their market bags.
CAMERA: slow push-in that settles into a static medium shot.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: dry wind, a jackhammer far away, cicadas, market bags rustling.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T10 · CALÇADA → TUPÃ NO TRONCO

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/24-ep03-clipe02-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/25-ep03-clipe03-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 03 · clipe 02 → clipe 03

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: Tupã steps off the sidewalk and crosses the dry lot toward the bare ipê; the camera follows him and lets Dona Nilza and Jesus slide out of frame behind. He stops, lifts his open palm and presses it against the cracked trunk.
CAMERA: following dolly from behind that arcs around and settles on a medium shot of Tupã at the trunk.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: dry grass under his sandals, the jackhammer fading, then a sudden drop into silence.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T11 · ENTARDECER → NOITE NA RAIZ

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/26-ep03-clipe03-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/27-ep03-clipe04-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 03 · clipe 03 → clipe 04

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: a time-lapse into night: the golden light drains from the lot, long shadows sweep across the dirt, the blue hour comes, the moon rises above the buildings, and the two men come back into frame and kneel at the base of the trunk.
CAMERA: static wide shot with the time-lapse, then a small settle into the high-angle medium shot of the two kneeling.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: cicadas handing over to crickets, a low underground pulse starting, sandals on dry earth.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## T12 · AMANHECER → O IPÊ FLORIDO

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/28-ep03-clipe04-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/29-ep03-clipe05-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 03 · clipe 04 → clipe 05

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: a time-lapse at dawn: the pink sky warms to gold, the bare branches above the two men suddenly fill with yellow blossom, petals start to fall, and the camera rises and pulls back to reveal the street covered in yellow. The two get to their feet.
CAMERA: continuous pull-back and rise from the medium shot at the trunk to the street-wide shot.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: the underground pulse stopping, birds waking up, petals rustling, a viola de cocho entering.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```



---

# AS 2 VIRADAS DE EPISÓDIO

## X01 · VIRADA DO EP. 01 PARA O EP. 02

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/10-ep01-clipe05-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/11-ep02-clipe01-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 01 (fim) → Ep. 02 (início)

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: from the balcony with the rainbow, the camera tilts up into the clearing sky; the clouds drift fast as time passes, the light changes from morning to late afternoon, and the camera comes down onto the faded blue backyard wall covered in pennants, with the junina poster taped to it.
CAMERA: tilt up, cloud time-lapse, tilt down onto the wall.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: crickets turning into accordion and laughter, wind in the pennants.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```


## X02 · VIRADA DO EP. 02 PARA O EP. 03

🟢 **PRIMEIRO FRAME (imagem 1, o B do clipe anterior):** `sequencia/20-ep02-clipe05-B-fim.jpg`
🔴 **ÚLTIMO FRAME (imagem 2, o A do clipe seguinte):** `sequencia/21-ep03-clipe01-A-inicio.jpg`
⏱️ **Duração:** 5,0 s · Ep. 02 (fim) → Ep. 03 (início)

```text
DURATION: 5 seconds.
FIRST FRAME: exactly the still of the previous clip's last frame, unchanged — same framing, same characters, same light.
LAST FRAME: exactly the still of the next clip's first frame, unchanged — same framing, same characters, same light.
MOTION: the camera tilts up from the Saci into the dark mango canopy; the leaves fill the frame and dissolve, through the gap, into a hard white-hot sky, which pulls back to reveal the dry vacant lot and the bare ipê between the low buildings.
CAMERA: tilt up into the leaves, then a slow pull-back revealing the dry lot.
SPEECH (Brazilian Portuguese, PT-BR): none. No dialogue in this bridge — nobody speaks, so no lip-sync is needed.
VOICES — FIXED CAST VOICES, IDENTICAL IN EVERY SHOT (never swap them):
- JESUS (Brazilian Portuguese, adult male, 30s): SOFT, CALM, VELVETY voice — warm, gentle, smooth and airy timbre, low energy, a smile inside the voice. Never loud, never shouting, never deep or gravelly.
- TUPÃ (Brazilian Portuguese, adult male, 30s): DEEP, THICK, THUNDEROUS voice — very low bass, gravelly and resonant, like distant thunder. Slow measured cadence, few words, almost flat delivery. Never soft, never high, never chatty.
AUDIO: night crickets fading into hot cicadas and a distant jackhammer.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, soft film grain, 16:9. Motion blur only on the camera move, never on the faces. No text, no letters, no subtitles, no watermark.
```

