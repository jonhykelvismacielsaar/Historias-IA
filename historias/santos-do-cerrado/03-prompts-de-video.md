# PROMPTS DE VÍDEO — os dois formatos

Este é o arquivo de **copiar e colar**. Cada clipe tem **dois prompts independentes**:

| | Tipo | Ferramenta | Para que serve |
|---|---|---|---|
| **A** | **Primeiro + último frame** | Seedance 2.0 / Kling 2.x / Veo 3 (modo *first & last frame*) | Você entrega **duas imagens** (`cXX.jpg` e `cXX-fim.jpg`) e o modelo interpola o movimento entre elas. **Mais controle** — a cena termina exatamente onde você desenhou. |
| **B** | **Imagem única com fala** | **Google Omni Flash** / **Seedance 1.5 Pro** (com áudio/diálogo) | Você entrega **só a imagem inicial** e o prompt descreve movimento, fala e som. **Mais rápido** e é o único que faz o diálogo com lip-sync decente. |

> **Regra de ouro:** as falas estão sempre em **português brasileiro**, curtas e com **marca de tempo** (ex.: `0.0–3.0s`). Isso ajuda o modelo a não atropelar a boca nem inventar texto.

---

## STATUS DOS FRAMES DE FIM

| Episódio | Início | Fim |
|---|---|---|
| 01 | ✅ c01–c05 | ✅ **todos os 5 prontos** (`c01-fim` a `c05-fim`) |
| 02 | ✅ c01–c05 | ✅ c01–c04 · ⏳ **falta `c05-fim`** |
| 03 | ✅ c01–c05 | ⏳ **faltam os 5** |

Os prompts dos frames de fim que faltam estão no **Anexo** no final do arquivo.

---

# EPISÓDIO 01 — QUARENTA GRAUS

## CLIPE 01 · A CIDADE QUE FERVE
`imagens/ep01/c01.jpg` → `imagens/ep01/c01-fim.jpg` · **sem fala**

### PROMPT A — primeiro/último frame

```text
FIRST FRAME: aerial wide shot of Cuiabá, Brazil at noon — terracotta rooftops, low buildings, heat haze on the asphalt, river shining far away, blown-out white-blue sky.
LAST FRAME: same city from a much lower altitude, now framing the facade of an old three-story white-tiled residential building, with an old moving truck parked on the dirt sidewalk and a stack of cardboard boxes, one open with a pineapple sticking out.
MOTION: the camera descends slowly and continuously from the sky to the building facade — one single uninterrupted downward glide, no cuts, no zoom, no rotation. Heat shimmer on the road all the way down. Birds cross the frame once in the middle of the move.
CAMERA: steady cinematic crane/drone descent, slight forward drift, ending on a static medium shot of the facade.
AUDIO: cicadas, distant traffic, low heat hum; at the end, an old truck engine dying and a handbrake.
STYLE: cinematic 2D anime, clean cel shading, thin linework, hand-painted background in Ghibli x A-1 Pictures style, warm saturated Brazilian light, soft film grain, 16:9. No text, no letters, no subtitles, no watermark.
```

### PROMPT B — imagem única com fala (Omni Flash / Seedance 1.5 Pro)

```text
Animate this still as a cinematic 2D anime shot of Cuiabá at noon. Slow drone descent over terracotta rooftops toward an old three-story building with a moving truck and cardboard boxes on the sidewalk. Heat shimmer distorts the asphalt, leaves roll across the ground, a few birds cross the sky.
CAMERA: one continuous slow descent, no cuts, slight forward drift.
SPEECH: none. Ambient sound only — cicadas, distant traffic, an old truck engine shutting off.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures look, warm Brazilian light, 16:9. No text, no subtitles, no watermark.
```

---

## CLIPE 02 · DOIS CARAS E UMA CAIXA
`imagens/ep01/c02.jpg` → `imagens/ep01/c02-fim.jpg`

### PROMPT A

```text
FIRST FRAME: empty apartment living room, sunlight rectangle on the beige ceramic floor. JESUS enters from the doorway holding a cardboard box and talking; TUPÃ walks across the room carrying a floral sofa on his back.
LAST FRAME: the sofa is being set down on the floor by TUPÃ, and JESUS stands next to it stretching his lower back, laughing, the box already on the ground.
MOTION: TUPÃ walks steadily from left to right and lowers the sofa to the floor in one continuous movement; JESUS follows him into the room, keeps talking, and only at the end straightens his back with a tired laugh. Both stay on their feet, no cuts.
CAMERA: slow lateral tracking shot following them, chest height, gentle parallax with the window light.
SPEECH (Brazilian Portuguese, natural, warm):
- JESUS, 1.0–4.5s: "Essa caixa tem dois mil anos e um liquidificador."
- TUPÃ, 5.5–7.0s, without stopping: "Põe na sala."
AUDIO: footsteps on tile, cardboard creaking, cicadas through the window.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm light, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot inside an empty Brazilian apartment. JESUS, in a white linen shirt, walks in from the left carrying a cardboard box and talks cheerfully; TUPÃ, in a dark charcoal sleeveless tank top with a Guarani patterned band across the chest, crosses the frame carrying a floral sofa and lowers it to the floor.
CAMERA: slow lateral tracking, chest height.
SPEECH (Brazilian Portuguese, lip-synced):
- JESUS at 1.0s: "Essa caixa tem dois mil anos e um liquidificador."
- TUPÃ at 5.5s, calm and flat: "Põe na sala."
AUDIO: footsteps, cardboard creak, cicadas outside.
STYLE: 2D anime, clean cel shading, hand-painted background, warm afternoon light, 16:9. No subtitles, no text.
```

---

## CLIPE 03 · O MILAGRE NÃO PEGA
`imagens/ep01/c03.jpg` → `imagens/ep01/c03-fim.jpg`

### PROMPT A

```text
FIRST FRAME: JESUS crouched in front of an old white table fan, palms flat on the grille, eyes closed, a thread of golden light around his fingers. TUPÃ leans on the door frame with arms crossed.
LAST FRAME: JESUS has stood up, shrugging with open palms, sheepish; TUPÃ is smiling with his eyes closed, still leaning on the frame, genuinely amused.
MOTION: the golden light pulses twice around Jesus' hands and dies; the fan blades never move. Jesus opens his eyes, sighs, stands up and shrugs. Tupã's expression changes from patient to an actual smile. One continuous shot.
CAMERA: static medium shot, very slow push-in, then settle.
SPEECH (Brazilian Portuguese):
- JESUS, 3.0–6.0s, resigned: "Ventilador abençoado não gira."
AUDIO: hot silence, cicadas, one click of the fan trying to start, then nothing.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm side light, 16:9. No text, no subtitles. No crosses, no crucifixes on the wall.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot in a small Brazilian living room. JESUS, crouched in front of an old white table fan with his palms on the grille, tries to bless it: golden light pulses twice around his hands and fades, the fan stays dead. He opens his eyes, stands up and shrugs. TUPÃ, leaning on the door frame with arms crossed, breaks into a quiet smile.
CAMERA: static medium shot with a very slow push-in.
SPEECH (Brazilian Portuguese, lip-synced):
- JESUS at 3.0s, resigned: "Ventilador abençoado não gira."
AUDIO: hot silence, distant cicadas, one mechanical click from the fan.
STYLE: 2D anime, clean cel shading, hand-painted look, warm afternoon light, 16:9. No text, no subtitles, no crosses on the wall.
```

---

## CLIPE 04 · A CHUVA DE TUPÃ
`imagens/ep01/c04.jpg` → `imagens/ep01/c04-fim.jpg` · **sem fala**

### PROMPT A

```text
FIRST FRAME: a Cuiabá neighborhood street in heavy rain, three barefoot children jumping in puddles in the middle of the street, one with an upside-down umbrella. JESUS leans out of a blue house window on the left, arms wide, face up, laughing.
LAST FRAME: the children are further away, running down the street; Jesus is still at the window, drenched, arms open, laughing, water dripping from the sill.
MOTION: rain pours continuously; the children run away from camera down the street, splashing; Jesus stays at the window, shaking rain from his hair once. Puddles ripple and overflow. No cuts.
CAMERA: static low shot at sidewalk height, slight handheld sway, raindrops close to the lens.
AUDIO: heavy rain, splashing, children laughing and screaming, a dog barking far away.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, blue-gray storm light with golden breaks, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot of a Brazilian street under heavy rain. Three barefoot children jump and run away down the flooded street, splashing water; JESUS leans out of a blue house window with his arms wide open and his face turned up, laughing and getting soaked.
CAMERA: static low angle at sidewalk height, subtle handheld movement, rain drops close to the lens.
SPEECH: none. Ambient sound only — heavy rain, splashes, children laughing, a distant dog barking.
STYLE: 2D anime, clean cel shading, hand-painted background, cool blue-gray storm light, 16:9. No text, no subtitles.
```

---

## CLIPE 05 · MOLHADOS, RINDO
`imagens/ep01/c05.jpg` → `imagens/ep01/c05-fim.jpg`

### PROMPT A

```text
FIRST FRAME: small wet balcony in the rain at dusk, JESUS and TUPÃ leaning on the parapet in profile, drenched, laughing, Tupã holding one open hand out in the rain.
LAST FRAME: the rain has stopped, the sky is clear gold with a soft rainbow, and the two stand side by side facing the horizon, each holding a tereré gourd, calm and content.
MOTION: the rain thins out progressively and stops; the clouds open; warm golden light slowly washes over the balcony; the two turn from each other toward the horizon and relax. Water keeps dripping from the plants. One continuous shot.
CAMERA: static medium shot on the two, then a slow, gentle tilt up to reveal the clearing sky and the rainbow.
SPEECH (Brazilian Portuguese):
- JESUS, 1.5–3.5s, laughing: "Você pediu chuva."
- TUPÃ, 4.5–6.5s, deadpan: "Você pediu ventilador."
AUDIO: rain fading to drips, crickets starting, a warm viola de cocho theme coming in at the end.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot on a small rainy balcony at dusk. JESUS and TUPÃ lean on the wet parapet, soaked and laughing; Tupã holds one palm open under the rain. The rain gradually stops, the sky clears into warm gold with a faint rainbow, and the two settle into a calm silence looking at the horizon.
CAMERA: static medium shot, ending with a slow tilt up to the sky.
SPEECH (Brazilian Portuguese, lip-synced):
- JESUS at 1.5s, laughing: "Você pediu chuva."
- TUPÃ at 4.5s, deadpan: "Você pediu ventilador."
AUDIO: rain fading into drips, crickets, soft viola de cocho music entering at the end.
STYLE: 2D anime, clean cel shading, hand-painted look, golden dusk light, 16:9. No text, no subtitles.
```

---

# EPISÓDIO 02 — A FESTA DO BAIRRO

## CLIPE 01 · O CONVITE
`imagens/ep02/c01.jpg` → `imagens/ep02/c01-fim.jpg`

### PROMPT A

```text
FIRST FRAME: a faded blue backyard wall covered in colorful paper pennants, with a hand-drawn junina festival poster taped to it — no letters anywhere.
LAST FRAME: Dona Nilza stands in front of the wall handing a folded paper to Jesus, who takes it with both hands, delighted; Tupã stands behind them with a hammer on his shoulder.
MOTION: the camera slides sideways along the wall, then stops. Nilza walks in from the right and holds out the paper; Jesus reaches for it; Tupã follows and settles behind them, already in work mode. Pennants flutter the whole time. One continuous shot.
CAMERA: lateral tracking that decelerates into a static medium shot of the three.
SPEECH (Brazilian Portuguese):
- DONA NILZA, 1.0–4.0s, excited: "Hoje tem festa no quintal."
- JESUS, 5.0–6.5s, delighted: "A gente vai!"
AUDIO: accordion far away, laughter, pennants snapping in the wind.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, golden late afternoon light, 16:9. No text, no letters, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot of a Brazilian backyard wall decorated with colorful pennants. DONA NILZA, an elderly woman in a blue floral dress with a green watering can, walks in and hands a folded paper to JESUS, who takes it smiling; TUPÃ appears behind them with a hammer resting on his shoulder.
CAMERA: lateral slide that settles into a static medium shot.
SPEECH (Brazilian Portuguese, lip-synced):
- DONA NILZA at 1.0s: "Hoje tem festa no quintal."
- JESUS at 5.0s: "A gente vai!"
AUDIO: distant accordion, laughter, fluttering paper flags.
STYLE: 2D anime, clean cel shading, hand-painted background, warm golden light, 16:9. No text, no letters, no subtitles.
```

---

## CLIPE 02 · A MONTAGEM
`imagens/ep02/c02.jpg` → `imagens/ep02/c02-fim.jpg`

### PROMPT A

```text
FIRST FRAME: sunset backyard with pennant strings; JESUS is high on an aluminum stepladder hanging flags and laughing; TUPÃ holds the ladder with one hand and a hammer in the other, looking up.
LAST FRAME: Jesus is back on the ground, dusting off his hands and laughing; Tupã holds the ladder and looks up at the finished line of pennants with quiet satisfaction.
MOTION: the ladder wobbles once, Tupã steadies it with his free hand; Jesus finishes tying the flag and climbs down carefully; both end up on the ground looking at the decoration. Pennants move in the breeze throughout. No cuts.
CAMERA: static low angle (low-angle wide), slight vibration when the ladder wobbles.
SPEECH (Brazilian Portuguese):
- JESUS, 1.0–4.0s, shouting happily: "Tupã, eu nunca me diverti tanto!"
- TUPÃ, 6.0–7.0s, flat: "Desce daí."
AUDIO: wind, one hammer tap, distant accordion, people laughing.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm sunset palette, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot in a decorated Brazilian backyard at sunset. JESUS, up on an aluminum stepladder, ties a paper flag and laughs; the ladder wobbles, and TUPÃ, below, steadies it with one hand while holding a hammer in the other. Jesus climbs down and they both look up at the finished pennants.
CAMERA: static low-angle wide shot, small shake when the ladder moves.
SPEECH (Brazilian Portuguese, lip-synced):
- JESUS at 1.0s, shouting: "Tupã, eu nunca me diverti tanto!"
- TUPÃ at 6.0s, flat and calm: "Desce daí."
AUDIO: wind, one hammer tap, distant accordion.
STYLE: 2D anime, clean cel shading, hand-painted background, golden sunset, 16:9. No text, no subtitles.
```

---

## CLIPE 03 · PÃO DE QUEIJO INFINITO
`imagens/ep02/c03.jpg` → `imagens/ep02/c03-fim.jpg`

### PROMPT A

```text
FIRST FRAME: community kitchen; JESUS, covered in flour, has both hands inside a bowl of dough that is rising by itself, eyes glowing faintly gold, as golden cheese bread rolls overflow a table behind him.
LAST FRAME: Jesus has stepped back from the table with both hands raised in surrender, laughing, flour floating in the air; the mountain of cheese bread is even bigger.
MOTION: the dough swells and spills; bread rolls keep piling up on the table one after another; Jesus pulls his hands out and backs away with an embarrassed laugh, blowing flour off his fingers. Continuous shot, no cuts.
CAMERA: frontal medium shot with a slow push-in, flour particles drifting in slow motion.
SPEECH (Brazilian Portuguese):
- JESUS, 3.0–6.0s, embarrassed: "Eu só queria fazer doze."
AUDIO: dough swelling, oven humming, bread rolls dropping onto metal trays.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm kitchen light, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot in a simple community kitchen. The dough in the bowl rises and spills over on its own; golden cheese bread rolls keep piling up on the table behind him. JESUS, with flour on his face, pulls his hands back, raises them in surrender and laughs, blowing flour off his fingers.
CAMERA: frontal medium shot, slow push-in, flour floating in the air.
SPEECH (Brazilian Portuguese, lip-synced):
- JESUS at 3.0s, embarrassed: "Eu só queria fazer doze."
AUDIO: dough swelling, oven hum, rolls landing on trays.
STYLE: 2D anime, clean cel shading, hand-painted look, warm light, 16:9. No text, no subtitles.
```

---

## CLIPE 04 · O FOGO E O FURTO
`imagens/ep02/c04.jpg` → `imagens/ep02/c04-fim.jpg` · **sem fala**

### PROMPT A

```text
FIRST FRAME: night junina party; TUPÃ crouched in front of a tall unlit pile of firewood, one knee on the ground, open palm over the logs, faint embers and smoke underneath.
LAST FRAME: the bonfire is burning high; Tupã has stood up and stepped back, shielding his face with one hand. In the foreground on the dirt, two pairs of flip-flops lie abandoned; in the blurred background behind the tents, a small pointed red cap disappears.
MOTION: sparks rise, the embers catch, flames grow fast and light Tupã's face from below. He stands up and steps back. The camera then drifts down to the flip-flops on the ground, where a small whirlwind of golden dust passes and takes them. In the background the red cap slips out of sight. No cuts — one continuous move from the fire down to the ground.
CAMERA: static low shot at first, then a slow tilt/pan down to the dusty ground.
AUDIO: crackling fire, a loud pop, laughter and accordion in the background, then a short high-pitched giggle off-screen.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm dark firelight, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot at a night junina festival. TUPÃ, crouched in front of the firewood with his open palm over the logs, makes the fire catch: sparks rise, embers glow and flames grow tall, lighting his face from below. He stands up and steps back. In the foreground, a small whirlwind of golden dust passes over two pairs of flip-flops on the ground, and behind the tents a small pointed red cap slips out of sight.
CAMERA: static low shot, slow tilt down to the ground at the end.
SPEECH: none. Ambient sound only — cracking fire, a loud pop, distant accordion and laughter, then a short high-pitched giggle off-screen.
STYLE: 2D anime, clean cel shading, hand-painted look, warm firelight on a dark night, 16:9. No text, no subtitles.
```

---

## CLIPE 05 · O TRATO COM O SACI
`imagens/ep02/c05.jpg` → `imagens/ep02/c05-fim.jpg` ⏳ *(frame de fim a gerar — prompt no Anexo)*

### PROMPT A

```text
FIRST FRAME: night, high branch of a mango tree; SACI — a skinny Black boy with a pointed red cap, torn shirt, a single bare foot and an unlit pipe — sits swinging his legs, two flip-flops dangling from his finger, grinning down at the party below.
LAST FRAME: the Saci has come down to the lowest branch, leaning toward TUPÃ and JESUS, who stand at the base of the trunk; Tupã has one hand on the trunk and Jesus holds up a cheese bread roll like an offering; the Saci's cap tilts with curiosity.
MOTION: the camera tilts up the tree to the Saci, who laughs and takes a puff from the unlit pipe, then stops laughing, tilts his cap, and climbs down branch by branch. Below, Tupã steps forward and puts his hand on the trunk while Jesus raises the cheese bread.
CAMERA: tilt up, hold, then tilt down following the Saci's descent.
SPEECH (Brazilian Portuguese):
- JESUS, 4.0–7.0s, friendly: "Desce que tem queijo."
AUDIO: high-pitched laughter, fire crackling, leaves, a branch creaking.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm night palette, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot at night. SACI, a skinny Black boy with a pointed red cap and a single bare foot, sits on a high tree branch swinging his legs and laughing, two flip-flops dangling from his finger. He takes a puff from his unlit pipe, stops laughing, tilts his cap with curiosity and starts climbing down toward the two men at the base of the trunk — TUPÃ with a hand on the trunk and JESUS holding up a cheese bread roll.
CAMERA: slow tilt up to the Saci, then a gentle tilt down following his descent.
SPEECH (Brazilian Portuguese, lip-synced):
- JESUS at 4.0s, friendly: "Desce que tem queijo."
AUDIO: high-pitched laughter, fire crackling, leaves rustling, a branch creaking.
STYLE: 2D anime, clean cel shading, hand-painted background, warm night light, 16:9. No text, no subtitles.
```

---

# EPISÓDIO 03 — O IPÊ DO ESTACIONAMENTO

## CLIPE 01 · A SÍNDICA E A MÁQUINA
`imagens/ep03/c01.jpg` → `imagens/ep03/c01-fim.jpg` ⏳

### PROMPT A

```text
FIRST FRAME: a dry vacant lot between low buildings in Cuiabá, cracked concrete sidewalk, wooden stakes with string, a tall bare ipê tree with a dark cracked trunk under a hot white sky. No people yet.
LAST FRAME: Dona Nilza stands on the sidewalk pointing at the dead tree, watering can in her hand; Jesus and Tupã have stopped beside her with straw market bags, both staring at the tree — Jesus worried, Tupã grave and knowing.
MOTION: the camera slides sideways along the lot; Nilza walks in from the right and points; Jesus and Tupã walk in behind her and stop. Dry grass moves in the wind. One continuous shot.
CAMERA: slow lateral tracking that settles into a static medium-wide shot of the three.
SPEECH (Brazilian Portuguese):
- DONA NILZA, 1.0–6.0s, indignant: "Setenta anos esse ipê. Semana que vem vem a máquina."
AUDIO: dry wind, a jackhammer far away, cicadas.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, dry desaturated palette with a hint of gold, 16:9. No text, no subtitles. No crosses, no religious symbols.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot of a vacant lot in Cuiabá. DONA NILZA, an elderly woman in a blue floral dress holding a green watering can, points at the dead bare tree while talking angrily; JESUS and TUPÃ stop beside her with straw market bags and stare at the tree. Dry grass bends in the hot wind.
CAMERA: slow lateral slide settling into a static medium-wide shot.
SPEECH (Brazilian Portuguese, lip-synced):
- DONA NILZA at 1.0s, indignant: "Setenta anos esse ipê. Semana que vem vem a máquina."
AUDIO: dry wind, distant jackhammer, cicadas.
STYLE: 2D anime, clean cel shading, hand-painted background, dry hot palette, 16:9. No text, no subtitles, no religious symbols.
```

---

## CLIPE 02 · OS TRÊS NA CALÇADA
`imagens/ep03/c02.jpg` → `imagens/ep03/c02-fim.jpg` ⏳

### PROMPT A

```text
FIRST FRAME: medium shot of three people on a sidewalk under strong morning light — Dona Nilza pointing at the dry ipê tree, Jesus and Tupã listening with their market bags.
LAST FRAME: Nilza still gesturing; Jesus thoughtful with a hand on his chin, nodding; Tupã with his head turned toward the tree, eyes narrowed, as if listening to something far away.
MOTION: minimal — Nilza keeps gesturing and talking, Jesus slowly nods and raises a hand to his chin, Tupã tilts his head slightly toward the tree and narrows his eyes. A dry leaf blows past. No cuts.
CAMERA: static medium shot with a very slow, subtle push-in.
SPEECH (Brazilian Portuguese):
- DONA NILZA, 0.5–4.0s: "Ele dá flor amarela, o bairro inteiro para."
- JESUS, 4.8–6.3s: "A gente dá um jeito."
- TUPÃ, 6.6–8.0s, low: "Ele tá com sede."
AUDIO: light traffic, cicadas, market bags rustling.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, warm saturated colors, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot on a sunny sidewalk in Cuiabá. DONA NILZA gestures toward the dry tree while she talks; JESUS nods slowly and brings a hand to his chin; TUPÃ turns his head toward the tree, narrows his eyes and speaks quietly. A dry leaf blows past.
CAMERA: static medium shot, very slow push-in.
SPEECH (Brazilian Portuguese, lip-synced):
- DONA NILZA at 0.5s: "Ele dá flor amarela, o bairro inteiro para."
- JESUS at 4.8s: "A gente dá um jeito."
- TUPÃ at 6.6s, low and quiet: "Ele tá com sede."
AUDIO: light traffic, cicadas.
STYLE: 2D anime, clean cel shading, hand-painted background, warm morning light, 16:9. No text, no subtitles.
```

---

## CLIPE 03 · TUPÃ ESCUTA A ÁRVORE
`imagens/ep03/c03.jpg` → `imagens/ep03/c03-fim.jpg` ⏳ · **sem fala**

### PROMPT A

```text
FIRST FRAME: dry vacant lot; TUPÃ stands with his open palm pressed on the cracked trunk of the bare ipê, eyes closed, a thread of emerald-green light running down the bark under his hand.
LAST FRAME: Tupã has pulled his hand away, eyes open and raised, looking up at the lower branches; the green light is fading; between the dry branches, two small glowing green eyes stare back at him.
MOTION: the green light pulses and travels down the trunk toward the roots; dust lifts off the ground and drifts away from the tree; Tupã opens his eyes, lifts his head and removes his hand. In the upper part of the frame, two green eyes flick open in the dark between the branches. One continuous shot.
CAMERA: static medium shot, a slow push-in, ending with a subtle tilt up toward the branch.
AUDIO: complete silence, then a deep low pulse from underground, like a slow heartbeat — and one wooden creak.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, golden side light with a green light accent, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot in a dry vacant lot. TUPÃ holds his palm on the cracked trunk of a bare tree with his eyes closed; a thread of emerald-green light pulses and runs down the bark toward the roots, and the dust around him drifts away. He opens his eyes, lifts his head and pulls his hand back — and in the shadows between the upper branches, two small glowing green eyes slowly open.
CAMERA: static medium shot, slow push-in, subtle tilt up at the end.
SPEECH: none. Complete silence, then a deep low pulse from underground and one wooden creak.
STYLE: 2D anime, clean cel shading, hand-painted look, golden light with a green accent, 16:9. No text, no subtitles.
```

---

## CLIPE 04 · ÁGUA NA RAIZ, LUZ NA TERRA
`imagens/ep03/c04.jpg` → `imagens/ep03/c04-fim.jpg` ⏳ · **sem fala**

### PROMPT A

```text
FIRST FRAME: night under a blue moon, at the base of the bare ipê. TUPÃ kneels in the dirt digging with his bare hands around a thick exposed root; JESUS kneels beside him with both palms open over the root, golden light spilling between his fingers into the earth, particles rising.
LAST FRAME: dawn breaking, pale pink and gold behind the low buildings. The root still glows faintly; Tupã sits back on his heels, forearms on his knees, hands covered in dirt, exhausted; Jesus sits on the ground leaning back on his hands, looking at the sky, tired but smiling.
MOTION: the golden light flows into the earth and pulses with the heartbeat rhythm; the camera holds while the night sky gradually brightens into dawn behind them; the two slowly change posture as exhaustion sets in. A time-lapse feeling inside one continuous shot.
CAMERA: static high-angle medium shot (slight plongée), no cuts.
SPEECH: none.
AUDIO: crickets, hands in the dirt, the deep underground pulse gradually slowing down, then the first birds at dawn.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, blue night turning into golden dawn, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot at night in a vacant lot. TUPÃ digs the dirt with his bare hands around an exposed root of the bare tree while JESUS, kneeling beside him, holds both palms over the root and lets golden light spill into the earth, with small light particles rising. The sky behind them slowly turns from deep blue night into pale golden dawn, and both men sag with exhaustion.
CAMERA: static high-angle medium shot, no cuts.
SPEECH: none. Crickets, hands in the dirt, a deep slow pulse underground, then the first birds of dawn.
STYLE: 2D anime, clean cel shading, hand-painted background, blue night turning to golden dawn, 16:9. No text, no subtitles.
```

---

## CLIPE 05 · O IPÊ FLORESCE
`imagens/ep03/c05.jpg` → `imagens/ep03/c05-fim.jpg` ⏳

### PROMPT A

```text
FIRST FRAME: sunrise street; the huge ipê in full golden-yellow bloom in the center of the frame, Jesus and Tupã standing shoulder to shoulder on the sidewalk looking up, petals on their hair and shoulders, neighbors blurred in the background.
LAST FRAME: the same street, now almost empty and quiet: the two walk away from camera side by side, small in the distance, each holding a tereré gourd, petals covering the asphalt, long morning shadows.
MOTION: petals fall continuously like golden snow; the camera orbits slowly around the trunk and then settles behind the two as they start walking away. Neighbors slowly disperse. One continuous shot.
CAMERA: slow orbit around the trunk, finishing as a wide shot from behind, watching them walk into the street.
SPEECH (Brazilian Portuguese):
- JESUS, 3.0–5.5s, soft: "Ele só precisava de água."
- TUPÃ, 6.0–8.0s, quiet: "E alguém que visse."
AUDIO: full viola de cocho score, petals falling, a distant collective "ohhh", soft morning wind.
STYLE: 2D anime, clean cel shading, hand-painted Ghibli x A-1 Pictures, luminous saturated colors, 16:9. No text, no subtitles.
```

### PROMPT B

```text
Animate this still as a cinematic 2D anime shot at sunrise. The huge ipê tree blooms in golden yellow and petals fall like snow over the street; JESUS and TUPÃ stand shoulder to shoulder, covered in petals, then turn and slowly walk away from the camera side by side down the petal-covered asphalt, each holding a tereré gourd.
CAMERA: slow orbit around the trunk that ends as a wide shot from behind, following the two as they walk away.
SPEECH (Brazilian Portuguese, lip-synced):
- JESUS at 3.0s, soft: "Ele só precisava de água."
- TUPÃ at 6.0s, quiet: "E alguém que visse."
AUDIO: full viola de cocho score, petals falling, a distant collective "ohhh", soft wind.
STYLE: 2D anime, clean cel shading, hand-painted look, luminous golden light, 16:9. No text, no subtitles.
```

---

# ANEXO — prompts dos frames de fim que faltam gerar

Use estes prompts no gerador de imagem para criar `ep02/c05-fim` e `ep03/c01-fim` a `c05-fim`. Salve como `.jpg` na pasta do episódio.

## `ep02/c05-fim.jpg`

```text
Anime cinematic 2D: base of a mango tree at night during a junina festival, warm lantern light, bonfire glow. JESUS: Brazilian man, 30, curly dark brown hair to the nape, short beard, white linen shirt, light jeans, flip-flops — holding up a cheese bread roll in his open hand like an offering. TUPÃ: Indigenous man, 30, brown skin, COMPLETELY CLEAN-SHAVEN BARE FACE, no tattoos on his arms, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with ONE horizontal band of Guarani geometric art across the chest, dark chino pants, leather sandals, seed bracelet — standing beside him with one hand resting on the tree trunk, looking up. On the lowest branch, SACI: skinny Black boy about 12, pointed red cap, torn red shirt, short torn pants, a single bare foot, an unlit pipe in his mouth, leaning down toward them, curious and grinning, the two stolen flip-flops in his hand. Pennants and lanterns blurred in the background. Hand-painted Ghibli x A-1 Pictures style, clean cel shading, thin linework, warm night palette, soft film grain, 16:9, no text, no letters, no watermark, no logo.
```

## `ep03/c01-fim.jpg`

```text
Anime cinematic 2D: cracked concrete sidewalk in front of a dry vacant lot in Cuiabá, a tall bare ipê tree with a dark cracked trunk, wooden stakes with string, low houses, hot white sky. Exactly THREE characters. DONA NILZA: Brazilian woman, 68, brown skin, short styled gray hair, round glasses on a chain, blue floral dress, flip-flops — pointing emphatically at the dry tree, a green plastic watering can in her other hand. JESUS: Brazilian man, 30, light brown skin, curly dark brown hair to the nape, short beard, white linen shirt, light jeans, flip-flops, straw market bag — stopped beside her, looking at the tree with concern. TUPÃ: Indigenous man, 30, brown skin, COMPLETELY CLEAN-SHAVEN BARE FACE, no tattoos, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with ONE horizontal band of Guarani geometric art across the chest, dark chino pants, leather sandals, seed bracelet, straw market bag — stopped beside them, staring at the tree with a grave, knowing expression. Hand-painted Ghibli x A-1 Pictures style, clean cel shading, thin linework, dry desaturated palette with warm gold, soft film grain, 16:9, no text, no letters, no watermark, no logo.
```

## `ep03/c02-fim.jpg`

```text
Anime cinematic 2D: cracked concrete sidewalk in front of a dry vacant lot in Cuiabá, a tall bare ipê tree behind a low fence, low houses and palm trees, strong late-morning light. Exactly THREE characters, medium shot. DONA NILZA: Brazilian woman, 68, brown skin, short styled gray hair, round glasses on a chain, blue floral dress, flip-flops, green watering can — still gesturing toward the tree. JESUS: Brazilian man, 30, light brown skin, curly dark brown hair to the nape, short beard, white linen shirt, light jeans, flip-flops, straw bag — nodding slowly, thoughtful, hand on his chin. TUPÃ: Indigenous man, 30, brown skin, COMPLETELY CLEAN-SHAVEN BARE FACE, no tattoos, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with ONE horizontal band of Guarani geometric art across the chest, dark chino pants, leather sandals, seed bracelet, straw bag — his head turned toward the tree, eyes narrowed, as if listening to something far away. Hand-painted Ghibli x A-1 Pictures style, clean cel shading, thin linework, warm saturated colors, soft film grain, 16:9, no text, no letters, no watermark, no logo.
```

## `ep03/c03-fim.jpg`

```text
Anime cinematic 2D: dry vacant lot in Cuiabá with yellowed grass and rubble, a tall bare ipê tree with a cracked dark gray trunk. TUPÃ: Indigenous man, 30, brown skin, COMPLETELY CLEAN-SHAVEN BARE FACE, no tattoos, long straight black hair in a low ponytail, dark charcoal-gray sleeveless tank top with ONE horizontal band of Guarani geometric art across the chest, dark chino pants, leather sandals, seed bracelet — pulling his open palm away from the trunk, eyes open and raised, looking UP at the lower branches, alert. The green light on the bark is fading away. In the upper part of the frame, between the dry branches, TWO SMALL GLOWING GREEN EYES stare back, barely visible. Warm golden side light, dusty air, long shadows. Hand-painted Ghibli x A-1 Pictures style, clean cel shading, thin linework, soft film grain, 16:9, no text, no letters, no watermark, no logo.
```

## `ep03/c04-fim.jpg`

```text
Anime cinematic 2D: dawn in a vacant lot in Cuiabá, pale pink and gold sky behind low buildings. Near the base of a bare ipê tree, freshly dug ground with a thick root exposed, covered by a faint fading golden glow. TUPÃ: Indigenous man, 30, brown skin, COMPLETELY CLEAN-SHAVEN BARE FACE, no tattoos, long straight black hair in a low ponytail coming loose, dark charcoal-gray sleeveless tank top with ONE horizontal band of Guarani geometric art across the chest, dark chino pants, leather sandals — sitting back on his heels, forearms on his knees, hands covered in dirt, exhausted and calm. Beside him JESUS: Brazilian man, 30, light brown skin, curly dark brown hair to the nape, short beard, white linen shirt now dirty, sleeves rolled — sitting on the ground, leaning back on his hands, looking at the sky, tired but smiling. Tiny golden particles still floating. Hand-painted Ghibli x A-1 Pictures style, clean cel shading, thin linework, soft film grain, 16:9, no text, no letters, no watermark, no logo.
```

## `ep03/c05-fim.jpg`

```text
Anime cinematic 2D: wide shot of a neighborhood street in Cuiabá early in the morning, a huge ipê tree in full golden-yellow bloom in the middle of the frame, petals covering the asphalt like yellow snow. EXACTLY TWO people walking away from the camera down the empty street, seen from behind, small in the frame, side by side: JESUS (Brazilian man, white linen shirt, light jeans, flip-flops, curly dark hair, holding a tereré gourd) and TUPÃ (Indigenous man, long black hair in a low ponytail, dark charcoal-gray sleeveless tank top with one horizontal band of Guarani geometric art across the chest, dark chino pants, leather sandals, holding a tereré gourd). Petals drifting in the air, long morning shadows, soft golden sunrise light, low houses on both sides. Hand-painted Ghibli x A-1 Pictures style, clean cel shading, thin linework, luminous saturated colors, soft film grain, 16:9, no text, no letters, no watermark, no logo.
```
