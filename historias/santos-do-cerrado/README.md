# SANTOS DO CERRADO — índice do projeto

Série de animação curta em 3 episódios de **40 segundos** (5 clipes de 8 s cada), inspirada na premissa do anime japonês **Saint Onii-san (Saint Young Men)** — Jesus e Buda dividindo um apartamento — transposta para o Brasil, com **Jesus e Tupã** morando juntos em **Cuiabá (MT)**.

---

## Comece por aqui

| # | Arquivo | O que tem |
|---|---|---|
| 1 | **[00-pesquisa-saint-onii-san.md](00-pesquisa-saint-onii-san.md)** | A pesquisa: qual é o anime, ficha técnica, por que "3 episódios", por que a nossa versão é original |
| 2 | **[01-biblia-da-historia.md](01-biblia-da-historia.md)** | Personagens, tom, ambiente, paleta, estrutura da temporada, regras invioláveis |
| 3 | **[02-guia-de-producao.md](02-guia-de-producao.md)** | Como gerar imagem → gerar vídeo de 5 s → montar os 60 s. Configurações do Seedance/Veo, negative prompt, CapCut |
| 4 | **[episodio-01-quarenta-graus.md](episodio-01-quarenta-graus.md)** | Roteiro do Ep. 1 + 5 frames prontos + 5 prompts de imagem + 5 prompts de vídeo |
| 5 | **[episodio-02-festa-do-bairro.md](episodio-02-festa-do-bairro.md)** | Roteiro do Ep. 2 + 5 frames prontos + 5 prompts de imagem + 5 prompts de vídeo |
| 6 | **[episodio-03-o-ipe-do-estacionamento.md](episodio-03-o-ipe-do-estacionamento.md)** | Roteiro do Ep. 3 + 5 frames prontos + 5 prompts de imagem + 5 prompts de vídeo |
| 7 | **[03-prompts-de-video.md](03-prompts-de-video.md)** | **Arquivo de copiar e colar:** os 2 tipos de prompt de vídeo (primeiro/último frame e imagem única com fala) para os 15 clipes |
| 8 | **[STATUS.md](STATUS.md)** | O que já está pronto e o que falta gerar na próxima conversa |

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
├── STATUS.md
└── imagens/
    ├── ep01/  c01.jpg … c05.jpg + c01-fim.jpg … c05-fim.jpg
    ├── ep02/  c01.jpg … c05.jpg
    ├── ep03/  c01.jpg … c05.jpg
    └── referencias/  (key visual dos personagens)
```

---

## Como usar em 4 passos

1. Abra o arquivo do episódio.
2. Cada plano tem **imagem pronta → prompt de imagem → prompt de vídeo de 5 s**.
3. Escolha o caminho em **[03-prompts-de-video.md](03-prompts-de-video.md)**:
   - **Prompt A** → duas imagens (início + fim) no Seedance 2.0 / Kling / Veo, modo *first & last frame*. Mais controle do movimento.
   - **Prompt B** → uma imagem só, no **Omni Flash** ou **Seedance 1.5 Pro**, com fala e lip-sync.
4. Junte os 5 clipes no CapCut, trave cada um em 8,0 s, coloque a trilha e exporte em 1080p.

---

## Convenções do projeto

- **Idioma dos prompts:** inglês (melhor aderência nos modelos de imagem/vídeo). Os roteiros e falas ficam em português.
- **Falas:** máximo 8 palavras por fala, 2 falas por plano. Dublagem/legenda é feita na edição.
- **Nunca** colocar texto dentro da imagem — títulos entram na edição.
- **Regra de ouro:** Jesus e Tupã **nunca discordam**. A piada é sempre a situação, nunca a religião.
