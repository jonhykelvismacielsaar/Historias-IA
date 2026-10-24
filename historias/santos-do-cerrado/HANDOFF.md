# HANDOFF — SANTOS DO CERRADO

Leia o `README.md`, `STATUS.md` e `02-guia-de-producao.md` nesta pasta antes de continuar.

## Estado atual

Temporada 1 fechada em imagens: **30/30 frames**. O pacote `sequencia/` contém 30 imagens numeradas (A-inicio/B-fim), três pranchas e `INDICE.md`.

Os prompts estão separados em dois arquivos:

- `03-prompts-de-video.md`: 15 clipes principais, cada um com **2 imagens e 5 segundos**, falas em **português brasileiro**, marcação de tempo e instruções de lip-sync.
- `04-prompts-de-transicao.md`: 14 pontes opcionais, cada uma usa **imagem B do clipe anterior → imagem A do próximo**, com 5 segundos.

## Regras inegociáveis

- Jesus: voz masculina mansa, tranquila e aveludada; cabelo cacheado comprido até os ombros preso em coque baixo despojado; ele é o único com barba.
- Tupã: voz masculina grossa e grave como trovão; sempre barbeado, sem tatuagens nos braços, rosto no máximo 45° de perfil.
- Repetir literalmente o bloco `VOICES` em cada prompt; não variar timbre ou identidade vocal entre clipes.
- Falas em PT-BR: máximo 7 palavras por fala e 14 palavras por clipe.
- Estampa canônica do Tupã: faixa larga creme com triângulos/losangos terracota grandes e saturados, além do motivo menor na barra. Anexar `imagens/ep01/c03.jpg` quando Tupã estiver em cena.
- Nenhum texto, letra, logo, legenda ou marca d'água nas imagens. Jesus e Tupã nunca discordam; a piada é a situação, nunca a religião.

## Próximo passo

Gerar os 15 clipes principais usando `03-prompts-de-video.md`. As pontes são opcionais e prolongam o corte em 5 s cada. Não gerar imagens novas, salvo se algum frame falhar na produção.
