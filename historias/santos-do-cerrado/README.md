# SANTOS DO CERRADO — índice do projeto

Série de animação curta em 3 episódios de **25 segundos** (5 clipes de 5 s cada), inspirada na premissa do anime japonês **Saint Onii-san (Saint Young Men)** — Jesus e Buda dividindo um apartamento — transposta para o Brasil, com **Jesus e Tupã** morando juntos em **Cuiabá (MT)**.

---

## Comece por aqui

| # | Arquivo | O que tem |
|---|---|---|
| 1 | **[00-pesquisa-saint-onii-san.md](00-pesquisa-saint-onii-san.md)** | A pesquisa: qual é o anime, ficha técnica, por que "3 episódios", por que a nossa versão é original |
| 2 | **[01-biblia-da-historia.md](01-biblia-da-historia.md)** | Personagens, tom, ambiente, paleta, estrutura da temporada, regras invioláveis |
| 3 | **[02-guia-de-producao.md](02-guia-de-producao.md)** | Como gerar imagem → gerar vídeo de 5 s → montar os 25 s. Configurações do Seedance/Veo, negative prompt, CapCut |
| 4 | **[episodio-01-quarenta-graus.md](episodio-01-quarenta-graus.md)** | Roteiro do Ep. 1 + 5 frames prontos + 5 prompts de imagem + 5 prompts de vídeo |
| 5 | **[episodio-02-festa-do-bairro.md](episodio-02-festa-do-bairro.md)** | Roteiro do Ep. 2 + 5 frames prontos + 5 prompts de imagem + 5 prompts de vídeo |
| 6 | **[episodio-03-o-ipe-do-estacionamento.md](episodio-03-o-ipe-do-estacionamento.md)** | Roteiro do Ep. 3 + 5 frames prontos + 5 prompts de imagem + 5 prompts de vídeo |
| 7 | **[03-prompts-de-video.md](03-prompts-de-video.md)** | **Arquivo de copiar e colar:** os 15 prompts de vídeo, **todos no formato de 2 imagens** (primeiro + último frame, 5 s) |
| 8 | **[04-prompts-de-transicao.md](04-prompts-de-transicao.md)** | 14 prompts (5 s) para ligar o frame B de um clipe ao frame A do próximo |
| 9 | **[sequencia/INDICE.md](sequencia/INDICE.md)** | **Pacote de uso direto:** os 30 frames renomeados na ordem de montagem + pranchas de conferência |
| 10 | **[STATUS.md](STATUS.md)** | O que já está pronto e o que falta gerar na próxima conversa |

---

## Estrutura de pastas

```
historias/santos-do-cerrado/
├── 00-pesquisa-saint-onii-san.md
├── 01-biblia-da-historia.md
├── 02-guia-de-producao.md
├── episodio-01-quarenta-graus.md
├── episodio-02-festa-do-bairro.md
├── episodio-03-o-ipe-do-estacionamento.md
├── 03-prompts-de-video.md
├── 04-prompts-de-transicao.md
├── STATUS.md
└── imagens/
    ├── ep01/  c01.jpg … c05.jpg + c01-fim.jpg … c05-fim.jpg
    ├── ep02/  c01.jpg … c05.jpg
    ├── ep03/  c01.jpg … c05.jpg + c01-fim … c05-fim
    └── referencias/  key-visual.jpg (referência dos personagens)
sequencia/  30 frames numerados 01–30 + 3 pranchas (ver INDICE.md)
```

---

## Como usar em 4 passos

1. Abra o arquivo do episódio.
2. Cada plano tem **imagem pronta → prompt de imagem → prompt de vídeo de 5 s**.
3. Pegue o prompt do clipe em **[03-prompts-de-video.md](03-prompts-de-video.md)**. **Formato único:** duas imagens (início + fim) no Seedance 2.0 / Kling / Veo, modo *first & last frame*, **5 segundos**.
   - Os dois arquivos de cada clipe estão em **[sequencia/](sequencia/INDICE.md)**, numerados de 01 a 30. As transições B→A opcionais estão em **[04-prompts-de-transicao.md](04-prompts-de-transicao.md)**.
4. Junte os 5 clipes no CapCut, trave cada um em 5,0 s, coloque a trilha e exporte em 1080p. Transições de 5 s são opcionais e aumentam a duração final.

---

## Convenções do projeto

- **Idioma dos prompts:** inglês (melhor aderência nos modelos de imagem/vídeo). Os roteiros e falas ficam em português.
- **Falas:** máximo 7 palavras por fala e 14 por clipe. As falas são geradas no prompt em PT-BR, com legendas adicionadas apenas na edição se desejado.
- **Nunca** colocar texto dentro da imagem — títulos entram na edição.
- **Regra de ouro:** Jesus e Tupã **nunca discordam**. A piada é sempre a situação, nunca a religião.
