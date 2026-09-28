# Historias-IA

## 🎭 Troca de personagem em vídeo

Você envia um **vídeo** e uma **foto**, e a pessoa da foto passa a estar no vídeo fazendo os mesmos movimentos. Dá para trocar **o corpo inteiro** (roupa, cabelo, corpo) ou **só o rosto**. O áudio original é mantido.

### Três modos

| Modo | O que troca | Qualidade | Onde roda | Custo |
|---|---|---|---|---|
| **🧠 Corpo inteiro · IA na nuvem** | pessoa inteira: corpo, roupa, cabelo, expressões, luz da cena | ⭐⭐⭐⭐⭐ (Wan 2.2 Animate, a mesma IA dos sites de "character swap") | GPU na nuvem: **deAPI** ou **fal.ai** | deAPI: US$ 5 grátis no cadastro · depois ~US$ 0,04–0,08 por segundo de vídeo |
| **🕺 Corpo inteiro · local** | pessoa inteira, como uma marionete 2D | ⭐⭐ (fica com cara de "recorte", sem 3D) | seu PC, só CPU | grátis |
| **🙂 Só o rosto** | só o rosto | ⭐⭐⭐ (clássico) · ⭐⭐⭐⭐ (IA inswapper) | seu PC, só CPU | grátis |

#### Por que o melhor modo é na nuvem?
A IA que troca o corpo inteiro de verdade (**Wan 2.2 Animate-14B**, da Alibaba, código aberto) tem 14 bilhões de parâmetros, uns 70 GB de arquivos, e precisa de **uma placa de vídeo com 24–80 GB**. Não tem como ela rodar em CPU. Por isso o projeto chama a IA por uma API:

* **deAPI**: crie a conta em https://app.deapi.ai (US$ 5 grátis, sem cartão, dá umas 45 trocas de 4 s). Limite de 8 s por vídeo.
* **fal.ai**: https://fal.ai/dashboard/keys. US$ 0,04/s (480p) a US$ 0,08/s (720p).

Cole a chave na interface, ou copie `.env.exemplo` para `.env` e preencha `DEAPI_API_KEY` / `FAL_KEY`.

Se você tiver uma placa de vídeo de 24 GB ou mais, também dá para rodar o Wan 2.2 Animate no seu PC pelo ComfyUI (existe um template oficial "Wan2.2 Animate").

#### Como funciona o motor local (corpo inteiro)
1. Detecta o esqueleto (33 pontos) e a silhueta da pessoa em cada quadro (MediaPipe).
2. **Apaga a pessoa original**: preenche o fundo com pedaços de outros quadros, alinhados pelo movimento da câmera (homografia), e usa inpainting no que nunca aparece.
3. Recorta o personagem da foto (GrabCut, usando o esqueleto como semente) e cobre ele com uma malha de ~5 000 triângulos ligada a 15 ossos (tronco, cabeça, pescoço, braços, antebraços, mãos, coxas, canelas, pés).
4. Em cada quadro, move os ossos para a pose do vídeo, deforma a malha e ajusta a luz do personagem à cena.

Limitações: é 2D, então o personagem não "vira" de costas nem de lado de verdade. Não há expressões faciais. Funciona melhor com **pessoa real, de frente, câmera parada e foto de corpo inteiro com os braços um pouco afastados do corpo**. Em desenho animado, o detector de pose erra mais.

### Modo "só o rosto"

![antes / foto / depois](amostras/exemplo_antes_depois.jpg)
*Esquerda: vídeo original · Meio: foto enviada · Direita: resultado*

#### Dois motores para o rosto

| Motor | Qualidade | Precisa baixar? | Velocidade (CPU, 720p) |
|---|---|---|---|
| **Clássico** (padrão) | boa: deforma a foto sobre uma malha de 468 pontos do rosto, com ajuste de cor e mistura *seamless* | **não**, funciona direto | ~25 quadros/s |
| **IA – inswapper** | muito realista (o mesmo modelo de Roop / FaceFusion / ReActor) | sim, ~700 MB (`python baixar_modelos.py`) | mais lento em CPU (estimativa: poucos q/s), bem mais rápido com GPU |

Com o modo **Automático**, o programa usa a IA quando os modelos estão instalados e, se não estiverem, usa o motor clássico.

### Instalação

```bash
./instalar.sh            # cria o .venv, instala as dependências e tenta baixar os modelos de IA
```
Para instalar manualmente: `pip install -r requirements.txt` e depois `python baixar_modelos.py`.
Se o download falhar, baixe os arquivos pelos links que o script mostra e coloque em `models/`:
- `models/inswapper_128.onnx`
- `models/w600k_r50.onnx` (fica dentro do `buffalo_l.zip`)

### Uso

**Interface web**
```bash
.venv/bin/python app.py          # abre em http://localhost:7860
```
1. Envie o vídeo e a foto. 2. Escolha o modo. 3. Clique em **Gerar vídeo**.

**Linha de comando**
```bash
# corpo inteiro
.venv/bin/python trocar_corpo.py video.mp4 personagem.png                         # local
.venv/bin/python trocar_corpo.py video.mp4 personagem.png --nuvem deapi --chave XXX  # IA na nuvem
# só o rosto
.venv/bin/python trocar_rosto.py video.mp4 foto.jpg -o resultado.mp4
```

**Exemplos para testar:** `./baixar_exemplos.sh` baixa os vídeos e fotos oficiais do Wan 2.2 Animate para `amostras/wan/`.

### Dicas para um bom resultado
- Use uma foto **de frente**, nítida, bem iluminada e sem óculos escuros.
- Funciona melhor quando o rosto aparece bem no vídeo. Rostos muito de perfil ficam piores.
- O modo `seamless` puxa a iluminação do vídeo. O modo `suave` fica mais fiel às cores da foto.

### Uso responsável
Só use a imagem de pessoas que autorizaram. Não use para enganar, difamar, cometer fraude ou criar conteúdo íntimo de ninguém. Em muitos países, incluindo o Brasil, isso é crime. Os modelos InsightFace são liberados **apenas para uso não comercial**.

### Estrutura
```
faceswap/landmarks.py   detecção de rostos + 478 pontos (MediaPipe)
faceswap/classic.py     motor clássico (malha + cor + seamless)
faceswap/ai_swapper.py  motor de IA (inswapper + ArcFace via onnxruntime)
faceswap/video.py       leitura/escrita do vídeo, suavização e áudio (ffmpeg)
bodyswap/pose.py        esqueleto + silhueta (MediaPipe Pose), com reinício automático
bodyswap/background.py  apaga a pessoa original (preenchimento temporal + homografia)
bodyswap/puppet.py      recorte, malha e "rig" do personagem (marionete 2D)
bodyswap/video.py       pipeline do corpo inteiro local
bodyswap/cloud.py       Wan 2.2 Animate Replace via deAPI / fal.ai
trocar_corpo.py         linha de comando (corpo inteiro)
app.py + templates/     interface web (Flask)
trocar_rosto.py         linha de comando
baixar_modelos.py       download dos modelos de IA
```
