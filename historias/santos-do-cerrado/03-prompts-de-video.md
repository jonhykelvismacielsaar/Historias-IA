# PROMPTS DE VÍDEO — formato único: **2 imagens por clipe, 6 segundos**

Este arquivo tem **um tipo de prompt só**. Todos os 15 clipes da temporada usam **duas imagens** (primeiro e último frame) e o modelo interpola o movimento entre elas.

> **Não existe mais prompt de imagem única.** A versão antiga (Prompt B, para Omni Flash) foi removida do projeto em 23/10 — o lip-sync dela era bom, mas em 6 s a diferença de qualidade não compensava o retrabalho de manter dois formatos. Tudo agora é *first & last frame*.

---

## Como identificar cada prompt

Cada bloco abaixo tem **sempre esta estrutura**:

    ## CLIPE 0X · TÍTULO

    🟢 PRIMEIRO FRAME (imagem 1): sequencia/0X-ep0Y-clipe0Z-A-inicio.jpg
    🔴 ÚLTIMO FRAME (imagem 2):   sequencia/0X-ep0Y-clipe0Z-B-fim.jpg
    ⏱️ Duração: 6,0 s

    (bloco de prompt)
    DURATION: 6 seconds.
    FIRST FRAME: ...
    LAST FRAME: ...
    MOTION: ...
    CAMERA: ...
    SPEECH: ...
    AUDIO: ...
    STYLE: ...


- **🟢 primeiro frame** (`...-A-inicio.jpg`) → é a **imagem 1** que você sobe.
- **🔴 último frame** (`...-B-fim.jpg`) → é a **imagem 2** que você sobe.
- O prompt começa com `DURATION: 6 seconds.` e tem **FIRST FRAME / LAST FRAME** no topo — se o prompt não tiver essas duas linhas, não é deste arquivo.

---

## Como gerar (4 passos)

1. Escolha o clipe na tabela abaixo.
2. Pegue as **duas imagens** na pasta `sequencia/` (nomes iguais aos da tabela).
3. Cole o prompt do bloco no Seedance 2.0 / Kling 2.x / Veo 3, no modo **first & last frame** (no Veo: "ingredients" com o primeiro e o último frame).
4. Trave a duração em **6,0 s**. Se o app só oferecer 5 s ou 8 s, gere assim mesmo e **corte na timeline** para 6,0 s.

> **Dica:** anexe também `imagens/referencias/key-visual.jpg` e, quando o Tupã estiver em cena, `imagens/ep01/c03.jpg` (estampa canônica da regata). Isso não muda o modo *first & last frame* — é referência extra de personagem.

---

## Tabela de clipes → imagens

| Ep. | Clipe | Título | Imagem 1 (primeiro frame) | Imagem 2 (último frame) | Tem fala? |
|---|---|---|---|---|---|
| 1 | 1 | A CIDADE QUE FERVE | `01-ep01-clipe01-A-inicio.jpg` | `02-ep01-clipe01-B-fim.jpg` | — |
| 1 | 2 | DOIS CARAS E UMA CAIXA | `03-ep01-clipe02-A-inicio.jpg` | `04-ep01-clipe02-B-fim.jpg` | Sim |
| 1 | 3 | O MILAGRE NÃO PEGA | `05-ep01-clipe03-A-inicio.jpg` | `06-ep01-clipe03-B-fim.jpg` | Sim |
| 1 | 4 | A CHUVA DE TUPÃ | `07-ep01-clipe04-A-inicio.jpg` | `08-ep01-clipe04-B-fim.jpg` | — |
| 1 | 5 | MOLHADOS, RINDO | `09-ep01-clipe05-A-inicio.jpg` | `10-ep01-clipe05-B-fim.jpg` | Sim |
| 2 | 1 | O CONVITE | `11-ep02-clipe01-A-inicio.jpg` | `12-ep02-clipe01-B-fim.jpg` | Sim |
| 2 | 2 | A MONTAGEM | `13-ep02-clipe02-A-inicio.jpg` | `14-ep02-clipe02-B-fim.jpg` | Sim |
| 2 | 3 | PÃO DE QUEIJO INFINITO | `15-ep02-clipe03-A-inicio.jpg` | `16-ep02-clipe03-B-fim.jpg` | Sim |
| 2 | 4 | O FOGO E O FURTO | `17-ep02-clipe04-A-inicio.jpg` | `18-ep02-clipe04-B-fim.jpg` | — |
| 2 | 5 | O TRATO COM O SACI | `19-ep02-clipe05-A-inicio.jpg` | `20-ep02-clipe05-B-fim.jpg` | Sim |
| 3 | 1 | A SÍNDICA E A MÁQUINA | `21-ep03-clipe01-A-inicio.jpg` | `22-ep03-clipe01-B-fim.jpg` | Sim |
| 3 | 2 | OS TRÊS NA CALÇADA | `23-ep03-clipe02-A-inicio.jpg` | `24-ep03-clipe02-B-fim.jpg` | Sim |
| 3 | 3 | TUPÃ ESCUTA A ÁRVORE | `25-ep03-clipe03-A-inicio.jpg` | `26-ep03-clipe03-B-fim.jpg` | — |
| 3 | 4 | ÁGUA NA RAIZ, LUZ NA TERRA | `27-ep03-clipe04-A-inicio.jpg` | `28-ep03-clipe04-B-fim.jpg` | — |
| 3 | 5 | O IPÊ FLORESCE | `29-ep03-clipe05-A-inicio.jpg` | `30-ep03-clipe05-B-fim.jpg` | Sim |

---

> **Duração de cada episódio:** 5 clipes × 6 s = **30 s**.


---

# EPISÓDIO 01 — QUARENTA GRAUS

## CLIPE 01 · A CIDADE QUE FERVE

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/01-ep01-clipe01-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/02-ep01-clipe01-B-fim.jpg`
⏱️ **Duração:** 6,0 s · **sem fala**

```text
DURATION: 6 seconds.
FIRST FRAME: aerial wide shot of Cuiabá, Brazil at noon — terracotta rooftops, low buildings, heat haze on the asphalt, river shining far away, blown-out white-blue sky.
LAST FRAME: same city from a much lower altitude, now framing the facade of an old three-story white-tiled residential building, with an old moving truck parked on the dirt sidewalk and a stack of cardboard boxes, one open with a pineapple sticking out.
MOTION: one single uninterrupted downward glide from the sky to the building facade — no cuts, no zoom, no rotation. Heat shimmer on the road the whole way. Birds cross the frame once, near the middle.
CAMERA: steady cinematic crane/drone descent, slight forward drift, settling on the facade.
SPEECH: none. No dialogue.
AUDIO: cicadas, distant traffic, low heat hum; in the last second, the truck engine dying and a handbrake.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, warm saturated Brazilian light, soft film grain, 16:9. No text, no letters, no subtitles, no watermark.
```

## CLIPE 02 · DOIS CARAS E UMA CAIXA

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/03-ep01-clipe02-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/04-ep01-clipe02-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: empty apartment living room, sunlight rectangle on the beige ceramic floor. JESUS enters from the doorway holding a cardboard box and talking; TUPÃ crosses the room carrying a floral sofa on his back.
LAST FRAME: the sofa is down on the floor, TUPÃ straightening up, and JESUS beside it stretching his lower back, laughing, the box already on the ground.
MOTION: one single movement — TUPÃ walks from left to right and lowers the sofa without stopping; JESUS follows him into the room, keeps talking, and only at the very end straightens his back with a tired laugh. Both stay on their feet, no cuts.
CAMERA: slow lateral tracking following them, chest height, gentle parallax with the window light.
SPEECH (Brazilian Portuguese, natural, warm):
- JESUS, 0.8–3.4s: "Essa caixa tem dois mil anos e um liquidificador."
- TUPÃ, 4.4–5.6s, without stopping: "Põe na sala."
AUDIO: footsteps on tile, cardboard creaking, cicadas through the window.
CHARACTERS: JESUS — Brazilian man, 30, light brown skin, CURLY dark brown hair reaching the shoulders and TIED IN A LOW BUN at the nape with loose curls framing the face, short beard, white linen shirt with rolled sleeves, light jeans, flip-flops. TUPÃ — Indigenous man, 30, brown skin, clean-shaven, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with one Guarani patterned band across the chest, dark chino pants, leather sandals, head turned three-quarters toward the camera so his face is clearly visible.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm light, 16:9. No text, no subtitles.
```

## CLIPE 03 · O MILAGRE NÃO PEGA

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/05-ep01-clipe03-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/06-ep01-clipe03-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: JESUS crouched in front of an old white table fan, palms flat on the grille, eyes closed, a thread of golden light around his fingers. TUPÃ leans on the door frame with arms crossed, head turned three-quarters toward the camera.
LAST FRAME: JESUS has stood up, shrugging with open palms, sheepish; TUPÃ is smiling with his eyes closed, still leaning on the frame, genuinely amused, face fully visible.
MOTION: the golden light pulses twice around Jesus' hands and dies; the fan blades never move. Jesus opens his eyes, sighs, stands up and shrugs. Tupã's expression changes from patient to an actual smile. One continuous shot, no cuts.
CAMERA: static medium shot, very slow push-in, then settle.
SPEECH (Brazilian Portuguese):
- JESUS, 2.2–4.6s, resigned: "Ventilador abençoado não gira."
AUDIO: hot silence, cicadas, one click of the fan trying to start, then nothing.
CHARACTERS: JESUS — CURLY dark brown hair reaching the shoulders, TIED IN A LOW BUN at the nape, loose curls framing the face, short beard, white linen shirt, barefoot. TUPÃ — clean-shaven, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with one Guarani band across the chest, barefoot.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm side light, 16:9. No text, no subtitles. No crosses, no crucifixes on the wall.
```

## CLIPE 04 · A CHUVA DE TUPÃ

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/07-ep01-clipe04-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/08-ep01-clipe04-B-fim.jpg`
⏱️ **Duração:** 6,0 s · **sem fala**

```text
DURATION: 6 seconds.
FIRST FRAME: a Cuiabá neighborhood street in heavy rain, three barefoot children jumping in puddles in the middle of the street, one with an upside-down umbrella. JESUS leans out of a blue house window on the left, arms wide, face up, laughing, his long curly hair tied in a low bun.
LAST FRAME: the children are further away, running down the street; Jesus is still at the window, drenched, arms open, laughing, water dripping from the sill.
MOTION: rain pours continuously; the children run away from camera down the street, splashing; Jesus stays at the window and shakes rain from his curls once. Puddles ripple and overflow. No cuts.
CAMERA: static low shot at sidewalk height, slight handheld sway, raindrops close to the lens.
SPEECH: none. No dialogue.
AUDIO: heavy rain, splashing, children laughing and screaming, a dog barking far away.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, blue-gray storm light with golden breaks, 16:9. No text, no subtitles.
```

## CLIPE 05 · MOLHADOS, RINDO

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/09-ep01-clipe05-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/10-ep01-clipe05-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: small wet balcony in the rain at dusk, JESUS and TUPÃ leaning on the parapet in profile but with their faces readable, drenched, laughing, Tupã holding one open hand out in the rain.
LAST FRAME: the rain has stopped, the sky is clear gold with a soft rainbow, and the two stand side by side facing the horizon but turned three-quarters toward the camera, each holding a tereré gourd, calm and content, both faces clearly visible.
MOTION: the rain thins out progressively and stops; the clouds open; warm golden light slowly washes over the balcony; the two turn from each other toward the horizon, then ease back into a slight three-quarter angle. Water keeps dripping from the plants. One continuous shot.
CAMERA: static medium shot on the two, then a slow, gentle tilt up to reveal the clearing sky and the rainbow.
SPEECH (Brazilian Portuguese):
- JESUS, 1.2–2.7s, laughing: "Você pediu chuva."
- TUPÃ, 3.6–5.4s, deadpan: "Você pediu ventilador."
AUDIO: rain fading to drips, crickets starting, a warm viola de cocho theme coming in at 4s.
CHARACTERS: JESUS — long CURLY dark brown hair TIED IN A LOW BUN at the nape, loose wet curls framing the face, short beard, soaked white linen shirt. TUPÃ — clean-shaven, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with one Guarani band across the chest, head never more than 45 degrees away from the camera.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, 16:9. No text, no subtitles.
```


---

# EPISÓDIO 02 — A FESTA DO BAIRRO

## CLIPE 01 · O CONVITE

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/11-ep02-clipe01-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/12-ep02-clipe01-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: a faded blue backyard wall covered in colorful paper pennants, with a hand-drawn junina festival poster taped to it — no letters anywhere.
LAST FRAME: Dona Nilza stands in front of the wall having just handed a folded paper to Jesus, who holds it with both hands, delighted; Tupã stands behind them with a hammer on his shoulder.
MOTION: the camera slides sideways along the wall and stops; Nilza walks in from the right and holds out the paper; Jesus takes it; Tupã settles behind them, already in work mode. Pennants flutter the whole time. One continuous shot.
CAMERA: lateral tracking that decelerates into a static medium shot of the three.
SPEECH (Brazilian Portuguese):
- DONA NILZA, 0.6–2.8s, excited: "Hoje tem festa no quintal."
- JESUS, 3.4–5.0s, delighted: "A gente vai!"
AUDIO: accordion far away, laughter, pennants snapping in the wind.
CHARACTERS: JESUS — curly dark brown hair to the shoulders TIED IN A LOW BUN, loose curls framing the face, short beard, white linen shirt. DONA NILZA — Brazilian woman, 68, gray hair, round glasses on a chain, blue floral dress, flip-flops. TUPÃ — clean-shaven, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with one Guarani band, hammer on his shoulder, face clearly visible.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, golden late afternoon light, 16:9. No text, no letters, no subtitles.
```

## CLIPE 02 · A MONTAGEM

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/13-ep02-clipe02-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/14-ep02-clipe02-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: sunset backyard with pennant strings; JESUS is high on an aluminum stepladder hanging flags and laughing; TUPÃ holds the ladder with one hand and a hammer in the other, looking up.
LAST FRAME: Jesus is down on the ground, dusting off his hands and laughing; Tupã stands beside the ladder looking up at the finished line of pennants with quiet satisfaction.
MOTION: the ladder wobbles once and Tupã steadies it with his free hand; Jesus ties the last flag and climbs down in the same movement; both end up looking at the decoration. Pennants move in the breeze throughout. No cuts.
CAMERA: static low-angle wide shot, slight vibration when the ladder wobbles.
SPEECH (Brazilian Portuguese):
- JESUS, 0.8–3.0s, shouting happily: "Tupã, eu nunca me diverti tanto!"
- TUPÃ, 4.4–5.5s, flat: "Desce daí."
AUDIO: wind, one hammer tap, distant accordion, people laughing.
CHARACTERS: JESUS — long curly dark brown hair TIED IN A LOW BUN, short beard, white linen shirt, light jeans, flip-flops. TUPÃ — clean-shaven, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with one Guarani band, dark chino pants.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm sunset palette, 16:9. No text, no subtitles.
```

## CLIPE 03 · PÃO DE QUEIJO INFINITO

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/15-ep02-clipe03-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/16-ep02-clipe03-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: community kitchen; JESUS, covered in flour, has both hands inside a bowl of dough that is rising by itself, eyes glowing faintly gold, as golden cheese bread rolls overflow a table behind him.
LAST FRAME: Jesus has stepped back from the table with both hands raised in surrender, laughing, flour floating in the air; the mountain of cheese bread is even bigger.
MOTION: the dough swells and spills and rolls keep piling up on the table, one after another; Jesus pulls his hands out and backs away with an embarrassed laugh, blowing flour off his fingers. No cuts.
CAMERA: frontal medium shot with a slow push-in, flour particles drifting in slow motion.
SPEECH (Brazilian Portuguese):
- JESUS, 2.2–4.6s, embarrassed: "Eu só queria fazer doze."
AUDIO: dough swelling, oven humming, rolls dropping onto metal trays.
CHARACTERS: JESUS — long curly dark brown hair TIED IN A LOW BUN with loose curls around the face, short beard, white linen shirt dusted with flour, no necklace, no pendant, no cross.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm kitchen light, 16:9. No text, no subtitles. No crosses, no religious symbols.
```

## CLIPE 04 · O FOGO E O FURTO

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/17-ep02-clipe04-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/18-ep02-clipe04-B-fim.jpg`
⏱️ **Duração:** 6,0 s · **sem fala**

```text
DURATION: 6 seconds.
FIRST FRAME: night junina party; TUPÃ crouched in front of a tall unlit pile of firewood, one knee on the ground, open palm over the logs, faint embers and smoke underneath, face lit from below and turned toward the camera.
LAST FRAME: the bonfire is burning high; Tupã has stood up and stepped back shielding his face; in the foreground on the dirt, two pairs of flip-flops lie abandoned — and in the blurred background a small pointed red cap slips behind a tent.
MOTION: sparks rise, the embers catch, the flames grow fast and light Tupã's face from below; he stands and steps back; in the same continuous movement the camera tilts down to the flip-flops on the ground as a small whirlwind of golden dust passes over them. No cuts.
CAMERA: low static shot that turns into one smooth tilt down to the dusty ground.
SPEECH: none. No dialogue.
AUDIO: crackling fire, one loud pop, distant accordion and laughter, then a short high-pitched giggle off-screen.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm dark firelight, 16:9. No text, no subtitles.
```

## CLIPE 05 · O TRATO COM O SACI

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/19-ep02-clipe05-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/20-ep02-clipe05-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: night, high branch of a mango tree; SACI — a skinny Black boy with a pointed red cap, torn shirt, a single bare foot and an unlit pipe — sits swinging his legs, two flip-flops dangling from his finger, grinning down at the party below.
LAST FRAME: the Saci has come down to the lowest branch, leaning toward TUPÃ and JESUS, who stand at the base of the trunk; Tupã has one hand on the trunk and Jesus holds up a cheese bread roll like an offering; the Saci's cap tilts with curiosity.
MOTION: the camera tilts up the tree to the Saci, who laughs and takes a puff from the unlit pipe, then stops laughing, tilts his cap and drops to the branch below. Below, Tupã steps forward and puts his hand on the trunk while Jesus raises the cheese bread. No cuts.
CAMERA: tilt up, brief hold, then a gentle tilt down following the Saci's descent.
SPEECH (Brazilian Portuguese):
- JESUS, 3.0–5.4s, friendly: "Desce que tem queijo."
AUDIO: high-pitched laughter, fire crackling, leaves, a branch creaking.
CHARACTERS: JESUS — long curly dark brown hair TIED IN A LOW BUN, short beard, white linen shirt, holding the bread roll up. TUPÃ — clean-shaven, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with one Guarani band, hand on the trunk, face visible.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm night palette, 16:9. No text, no subtitles.
```


---

# EPISÓDIO 03 — O IPÊ DO ESTACIONAMENTO

## CLIPE 01 · A SÍNDICA E A MÁQUINA

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/21-ep03-clipe01-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/22-ep03-clipe01-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: a dry vacant lot between low buildings in Cuiabá, cracked concrete sidewalk, wooden stakes with string, a tall bare ipê tree with a dark cracked trunk under a hot white sky. No people yet.
LAST FRAME: Dona Nilza stands on the sidewalk pointing at the dead tree, watering can in her hand; Jesus and Tupã have stopped beside her with straw market bags, both staring at the tree — Jesus worried, Tupã grave and knowing.
MOTION: the camera slides sideways along the lot; Nilza walks in from the right and points; Jesus and Tupã walk in behind her and stop. Dry grass moves in the wind. One continuous shot.
CAMERA: slow lateral tracking that settles into a static medium-wide shot of the three.
SPEECH (Brazilian Portuguese):
- DONA NILZA, 0.8–5.0s, indignant: "Setenta anos esse ipê. Semana que vem vem a máquina."
AUDIO: dry wind, a jackhammer far away, cicadas.
CHARACTERS: DONA NILZA — Brazilian woman, 68, brown skin, short styled gray hair, round glasses on a chain, blue floral dress, flip-flops, green watering can. JESUS — curly dark brown hair to the shoulders TIED IN A LOW BUN, short beard, white linen shirt, light jeans, flip-flops, straw market bag. TUPÃ — clean-shaven, no tattoos, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with one Guarani band across the chest, dark chino pants, leather sandals, straw market bag.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, dry desaturated palette with a hint of gold, 16:9. No text, no subtitles. No crosses, no religious symbols.
```

## CLIPE 02 · OS TRÊS NA CALÇADA

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/23-ep03-clipe02-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/24-ep03-clipe02-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: medium shot of three people on a sidewalk under strong morning light — Dona Nilza pointing at the dry ipê tree, Jesus and Tupã listening with their market bags.
LAST FRAME: Nilza still gesturing; Jesus thoughtful with a hand on his chin, nodding; Tupã with his head turned toward the tree, eyes narrowed — but still in a three-quarter angle, face visible to the camera.
MOTION: minimal and continuous — Nilza keeps gesturing, Jesus slowly nods and raises a hand to his chin, Tupã tilts his head slightly toward the tree and narrows his eyes. One dry leaf blows past. No cuts.
CAMERA: static medium shot with a very slow, subtle push-in.
SPEECH (Brazilian Portuguese):
- DONA NILZA, 0.4–2.9s: "Ele dá flor amarela, o bairro inteiro para."
- JESUS, 3.3–4.5s: "A gente dá um jeito."
- TUPÃ, 4.8–5.8s, low: "Ele tá com sede."
AUDIO: light traffic, cicadas, market bags rustling.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm saturated colors, 16:9. No text, no subtitles.
```

## CLIPE 03 · TUPÃ ESCUTA A ÁRVORE

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/25-ep03-clipe03-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/26-ep03-clipe03-B-fim.jpg`
⏱️ **Duração:** 6,0 s · **sem fala**

```text
DURATION: 6 seconds.
FIRST FRAME: dry vacant lot; TUPÃ stands with his open palm pressed on the cracked trunk of the bare ipê, eyes closed, a thread of emerald-green light running down the bark under his hand.
LAST FRAME: Tupã has pulled his hand away, eyes open and raised, looking up at the lower branches; the green light is fading; between the dry branches, two small glowing green eyes stare back at him.
MOTION: the green light pulses and travels down the trunk toward the roots; dust lifts off the ground and drifts away; Tupã opens his eyes, lifts his head and removes his hand; in the upper part of the frame two green eyes flick open between the branches. One continuous shot with a subtle tilt up at the end.
CAMERA: static medium shot, slow push-in, ending with a small tilt up toward the branch.
SPEECH: none. No dialogue.
AUDIO: complete silence, then a deep low pulse from underground, like a slow heartbeat, and one wooden creak.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, golden side light with a green light accent, 16:9. No text, no subtitles.
```

## CLIPE 04 · ÁGUA NA RAIZ, LUZ NA TERRA

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/27-ep03-clipe04-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/28-ep03-clipe04-B-fim.jpg`
⏱️ **Duração:** 6,0 s · **sem fala**

```text
DURATION: 6 seconds.
FIRST FRAME: night under a blue moon, at the base of the bare ipê. TUPÃ kneels in the dirt digging with his bare hands around a thick exposed root; JESUS kneels beside him with both palms open over the root, golden light spilling between his fingers into the earth, particles rising.
LAST FRAME: dawn breaking, pale pink and gold behind the low buildings. The root still glows faintly; Tupã sits back on his heels, forearms on his knees, hands covered in dirt, exhausted; Jesus sits on the ground leaning back on his hands, looking at the sky, tired but smiling.
MOTION: the golden light flows into the earth and pulses once; the night sky brightens steadily into dawn behind them; both men slowly change posture as the exhaustion lands. A time-lapse feeling inside one continuous shot.
CAMERA: static high-angle medium shot (slight plongée), no cuts.
SPEECH: none.
AUDIO: crickets, hands in the dirt, the deep underground pulse slowing down, then the first birds at dawn.
CHARACTERS: JESUS — long curly dark brown hair TIED IN A LOW BUN, short beard, white linen shirt with rolled sleeves, light jeans. TUPÃ — clean-shaven, long straight black hair in a low ponytail coming loose, dark charcoal-gray sleeveless tank top with one Guarani band across the chest, dark chino pants.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, blue night turning into golden dawn, 16:9. No text, no subtitles.
```

## CLIPE 05 · O IPÊ FLORESCE

🟢 **PRIMEIRO FRAME (imagem 1):** `sequencia/29-ep03-clipe05-A-inicio.jpg`
🔴 **ÚLTIMO FRAME (imagem 2):** `sequencia/30-ep03-clipe05-B-fim.jpg`
⏱️ **Duração:** 6,0 s · com fala em PT-BR

```text
DURATION: 6 seconds.
FIRST FRAME: sunrise street; the huge ipê in full golden-yellow bloom in the center of the frame, Jesus and Tupã standing shoulder to shoulder on the sidewalk looking up, petals on their hair and shoulders, neighbors blurred in the background.
LAST FRAME: the same street, now almost empty and quiet: the two walk away from camera side by side, small in the distance, each holding a tereré gourd, petals covering the asphalt, long morning shadows.
MOTION: petals fall continuously like golden snow; the camera orbits slowly around the trunk and settles behind the two as they start walking away; neighbors slowly disperse. One continuous shot.
CAMERA: slow orbit around the trunk, finishing as a wide shot from behind, watching them walk into the street.
SPEECH (Brazilian Portuguese):
- JESUS, 2.2–4.2s, soft: "Ele só precisava de água."
- TUPÃ, 4.6–5.8s, quiet: "E alguém que visse."
AUDIO: full viola de cocho score, petals falling, a distant collective "ohhh", soft morning wind.
CHARACTERS: JESUS — long curly dark brown hair TIED IN A LOW BUN, short beard, white linen shirt, holding a tereré gourd. TUPÃ — clean-shaven, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with one Guarani band, holding a tereré gourd.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, luminous saturated colors, 16:9. No text, no subtitles.
```


---

# Checklist antes de gerar

- [ ] Subi **as duas imagens** (primeiro e último frame)?
- [ ] Marquei **6 segundos** de duração?
- [ ] O prompt começa com `DURATION: 6 seconds.` e tem `FIRST FRAME` e `LAST FRAME`?
- [ ] Se o Tupã aparece: anexei `imagens/ep01/c03.jpg` como referência da estampa?
- [ ] Se o Tupã aparece: o rosto está legível (no máximo 45° de perfil)?
- [ ] Sem texto, letra, logo ou legenda na imagem?
