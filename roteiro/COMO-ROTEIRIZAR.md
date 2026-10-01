# Como roteirizar os próximos episódios

Este guia é para você (ou para outra IA) continuar a série sem perder o padrão. O sistema foi
feito para que a **única parte escrita à mão** seja a curadoria criativa — o texto bíblico em
hebraico, aramaico, siríaco, grego e português é injetado automaticamente pelo script.

---

## 1. A regra que nunca muda

**1 episódio = 12 frames × 5 segundos = 60 segundos.**

* Cada frame = 1 prompt de imagem + 1 prompt de vídeo.
* A narração de cada frame precisa caber em 5 s → **máximo ~20 palavras** (o validador avisa se passar).
* A narração é sempre a **voz de Deus em primeira pessoa**, em PT-BR, fiel ao versículo.

---

## 2. Passo a passo

### Passo 1 — Descubra o episódio no plano

```bash
python3 -c "
import json
d=json.load(open('roteiro/indice_episodios.json',encoding='utf-8'))
for ep in d['episodios'][:5]: print(ep['id'], ep['referencia'], '|', ep['titulo'], '|', ep['genero'])
"
```

Ou abra `roteiro/plano_episodios.csv` (abre no Excel/Planilhas Google). Ele já diz, para cada
episódio: livro, capítulo, faixa de versículos, título e gênero literário.

### Passo 2 — Veja o texto original do trecho

```bash
python3 -c "
import json
d=json.load(open('dados/processado/versiculos/genesis.json',encoding='utf-8'))
for v in ['3','4','5']:
    r=d['capitulos']['1'][v]
    print('HE :', r.get('he',''))
    print('TAR:', r.get('targum_onkelos',''))
    print('LXX:', r.get('lxx_grego',''))
    print('PT :', r.get('pt_aa',''))
    print()
"
```

### Passo 3 — Copie um modelo e escreva a curadoria

```bash
cp roteiro/curadoria/EP-0002.json roteiro/curadoria/EP-0005.json
```

Abra `EP-0005.json` e troque:

* `id`, `titulo`, `referencia`, `slug`, `capitulo`, `versiculo_inicial`, `versiculo_final`;
* nos 12 frames: `titulo`, `referencia`, `versiculos`, `acao_cena_pt`, `imagem_scene_en`,
  `video_movimento_en`, `narracao`, `texto_passagem_pt`, `sfx`, `trilha`.

**O que NÃO precisa escrever:** o hebraico, o aramaico, o siríaco, o grego e o português.
O script busca no corpus pelo capítulo e faixa de versículos que você indicou.

### Passo 4 — Gere o episódio final

```bash
python3 ferramentas/03_gerar_episodio.py EP-0005
```

Saída: `roteiro/episodios/EP-0005.json` — o episódio completo, validado.

---

## 3. O molde dos prompts

### Prompt de imagem (inglês)

```
[cena específica do frame]. [ESTILO_BASE: pintura a óleo hiper-realista em linhas de linho,
empasto, chiaroscuro, 8k, masterpiece]. [PINCEL: pincel de madeira flutuando com tinta fresca].
[luz]. Aspect ratio 16:9.
```

* **Sempre** em inglês (Midjourney, Flux, SDXL rendem melhor).
* **Sempre** com a frase do pincel — é a assinatura visual da série.
* **Nunca** descrever Deus, nenhum rosto divino, nenhuma figura celeste humana.
  O pincel faz o papel da presença de Deus.
* Proporção: **sempre 16:9 (3840×2160)**, horizontal. Não gerar versão vertical.

### Prompt de vídeo (inglês)

```
A câmera ENTRA na superfície da pintura e as pinceladas ganham vida tridimensional.
[ESTILO_VIDEO_BASE]. Movement: [movimento específico da cena]. Camera: [movimento de câmera].
Duration 5 seconds.
```

* Use verbos de transformação: *bloom, dissolve, erupt, unfold, bloom into real matter*.
* Uma única ação clara por frame — vídeos de 5 s não comportam duas ações.

### Onde ir buscar os movimentos de câmera

| Intenção | Frase para o prompt |
|---|---|
| Revelar a escala | `extreme slow pull-back to the widest possible shot` |
| Entrar na cena | `the camera flies INTO the surface of the painting` |
| Mostrar detalhe | `macro shot on the bristles, then slow pull-back` |
| Momento sagrado | `extremely slow drift backward, then hold perfectly still` |
| Passagem do tempo | `time-lapse style lateral sweep` |
| Clímax | `fast follow of the brush stroke, then settle as the light floods` |

---

## 4. Regras de fidelidade (não negociáveis)

1. **A narração segue o texto massorético** — o mesmo da Bíblia em português. O telespectador
   deve poder abrir a Bíblia e conferir versículo por versículo.
2. **Nunca misture variantes no texto narrado.** Se houver divergência (ex.: Gênesis 2:2 —
   "sétimo dia" no hebraico × "sexto dia" na Septuaginta e na Peshitta), use o campo
   `nota_producao` do frame e siga o hebraico na voz.
3. **Nunca invente fala de personagem humano.** As falas de pessoas são as do texto bíblico,
   literais, no campo `falas_personagens`.
4. **Nunca coloque legendas nem texto na tela.** O vídeo não tem nenhuma palavra escrita:
   nem legenda, nem título, nem crédito de cena. A voz do narrador carrega o texto bíblico.
5. **Não misture os cânones.** A Temporada 9 (69 obras apócrifas) tem prelúdio próprio e é
   sempre identificada como extra-bíblica.
6. **Nunca represente Deus visualmente.** Só o pincel, o rastro de tinta e a luz.

---

## 5. Ritmo por gênero literário (já aplicado no plano)

| Gênero | Versículos por frame | Versículos por episódio | Exemplo |
|---|---|---|---|
| Narrativo | 1 | 12 | Gênesis, Êxodo, Evangelhos |
| Profético | 1 | 12 | Isaías, Jeremias |
| Apocalíptico | 1 | 12 | Daniel 7-12, Apocalipse |
| Cartas | 1,2 | 14 | Romanos, 1 Coríntios |
| Legislativo | 2,5 | 30 | Levítico, Deuteronômio, Êxodo 20-40 |
| Poético | 0,5 | 6 (2 frames por versículo) | Salmos, Jó, Cantares |
| Listas / censos | 4 | 48 | Gênesis 5 e 10, Números 1 |

---

## 6. Motivos visuais que dão unidade à série

| Motivo | Onde aparece | O que significa |
|---|---|---|
| **Pincel flutuante** | em todos os frames, exceto os marcados `pincel: false` | a presença de Deus agindo |
| **Tinta fresca e brilhante** | em volta do pincel | a criação é recente, viva |
| **Linhas douradas no rodapé da tela** | uma por dia da criação (7 em Gênesis 1) | a contagem dos dias |
| **A câmera entra na pintura** | em todos os vídeos | o quadro vira realidade |
| **Deus nunca aparece** | sempre | o espectador é quem "vê" Deus na obra |

---

## 7. Checklist antes de publicar um episódio

- [ ] 12 frames, 5 s cada (60 s no total)
- [ ] cada narração com no máximo ~20 palavras
- [ ] `texto_passagem_pt` de cada frame = versículo literal da Bíblia
- [ ] `nota_producao` preenchida onde houver variante textual
- [ ] prompt de imagem em inglês, com a cláusula do pincel
- [ ] prompt de vídeo com **uma** ação clara e o movimento de câmera
- [ ] formato 16:9 horizontal (sem versão vertical)
- [ ] **nenhuma legenda e nenhum texto na tela** — a voz e a imagem contam a história
- [ ] continuidade de paleta com o frame anterior

Rode `python3 ferramentas/03_gerar_episodio.py --todos` — o validador aponta automaticamente
qualquer frame fora do padrão.
