# HANDOFF — texto para copiar e colar numa nova conversa

> Copie **todo o bloco abaixo** (do "---INÍCIO---" ao "---FIM---") e cole na primeira mensagem da nova conversa, com o repositório `Historias-IA` aberto. Ele dá contexto suficiente para o agente continuar sem precisar reler tudo.

---INÍCIO---

Continuando o projeto **SANTOS DO CERRADO**, que já está no repositório em `historias/santos-do-cerrado/`. Leia primeiro o `README.md`, o `STATUS.md` e o `02-guia-de-producao.md` dessa pasta antes de gerar qualquer coisa.

**O projeto:** série de animação curta (anime 2D), 3 episódios de **30 s cada = 5 clipes de 6 s** (o projeto saiu de 8 s para 6 s por clipe em 23/10). É uma versão brasileira, ambientada em Cuiabá (MT), da premissa do anime japonês *Saint Onii-san / Saint Young Men*: duas divindades dividindo apartamento. Aqui os protagonistas são **Jesus** (brasileiro, cabelo cacheado **comprido e preso num coque baixo**, barba curta, camisa de linho branca, chinelo) e **Tupã** (indígena, cabelo preto liso em rabo de cavalo, camiseta cinza sem manga com grafismo guarani).

**Regras que não podem ser quebradas:**
1. Jesus e Tupã **nunca discordam** — são amigos, a piada é sempre a situação, nunca a religião.
2. Nenhuma imagem deve ter texto, letra, logo ou legenda.
3. Copiar **literalmente** o bloco de personagem e o bloco de estilo do `02-guia-de-producao.md` em todo prompt. Não parafrasear.
4. Estilo: anime cinematográfico 2D, cel shading limpo, traço fino, fundo pintado à mão estilo Ghibli x A-1 Pictures, luz brasileira quente, 16:9, grão de filme suave.

**O que já está pronto:** roteiro completo dos 3 episódios em `episodio-01`, `episodio-02` e `episodio-03`, cada um com 5 clipes de 6 s, o `03-prompts-de-video.md` retimado, o key visual em `imagens/referencias/key-visual.jpg` e **19 frames já gerados** (`imagens/ep01` a `imagens/ep03`, arquivos `c01.jpg` a `c05.jpg`).

**O que eu preciso agora:**

TAREFA 1 (já resolvida — pule; o Tupã agora aparece em três quartos) — Regerar **apenas** o frame `imagens/ep03/c05.jpg`. O que existe hoje saiu com o personagem **Tupã duplicado** (aparecem dois homens indígenas na imagem). Use o prompt abaixo:

```text
Plano geral de uma rua de Cuiabá ao amanhecer: um ipê amarelo enorme e florido no centro do quadro, cercado de prédios baixos e cinzentos, calçada e asfalto cobertos de pétalas amarelas. Em primeiro plano, na calçada, exatamente DUAS figuras: JESUS (homem brasileiro de 30 anos, pele morena clara, cabelo castanho-escuro cacheado e comprido, na altura dos ombros, preso num coque baixo despojado na nuca, com cachos soltos emoldurando o rosto, barba curta, camisa de linho branca de botão com mangas dobradas, calça jeans clara, chinelo de dedo) e TUPÃ (homem indígena de 30 anos, pele morena, cabelo preto liso na altura dos ombros preso em rabo de cavalo baixo, camiseta cinza-escura sem manga com grafismo geométrico guarani no peito, calça de sarja, sandália de couro, pulseira de sementes) — apenas esses dois personagens, de ombros encostados, olhando para cima, com pétalas no cabelo e nos ombros. Pessoas desfocadas ao fundo também olhando para cima. Luz de sol nascente atravessando as flores. ESTILO: anime cinematográfico 2D, cel shading limpo, traço fino, fundo pintado à mão no estilo Ghibli x A-1 Pictures, cores luminosas e saturadas, grão de filme suave, 16:9, sem texto, sem letreiro, sem logo, sem legenda.
```

TAREFA 2 (prioridade) — Gerar o **key visual** dos dois personagens em `imagens/referencias/key-visual.jpg`: os dois em pé, lado a lado, pose neutra, fundo claro liso, corpo inteiro, mesmo estilo. Esse arquivo será usado como imagem de referência para travar a consistência dos personagens nos geradores de vídeo.

TAREFA 3 — Gerar **imagens extras para a temporada 2**, seguindo a lógica dos mesmos 5 clipes de 6 s: a figura alta de terno claro e chapéu de palha que aparece no fim do Ep. 03 (um "cobrador cósmico" que vem auditar as férias dos dois), o Saci e o Curupira como aliados, e o apartamento 302 em desordem. Antes de gerar, escreva o roteiro dos 5 clipes de cada novo episódio no mesmo formato dos arquivos existentes (cena, câmera, áudio, imagem, prompt de imagem, prompt de vídeo de 6 s, ficha do episódio).

**Como gerar:** use o gerador de imagem da plataforma, salve os arquivos `.png` e depois converta para `.jpg` (`convert arquivo.png -quality 92 -strip arquivo.jpg`) para não inflar o repositório. Mantenha os links nas marcações `![CLIPE 0X](imagens/epXX/cXX.jpg)` funcionando. Ao final, atualize o `STATUS.md` e faça commit.

---FIM---

---

## Versão curta (se a conversa nova travar)

> "No repo Historias-IA, pasta `historias/santos-do-cerrado/`: leia STATUS.md e o HANDOFF.md. Os 15 frames da temporada 1 já estão prontos. Gere o key visual em `imagens/referencias/key-visual.jpg` (os dois personagens, corpo inteiro, fundo liso, Tupã SEM barba) e depois siga a temporada 2 conforme o HANDOFF.md."
