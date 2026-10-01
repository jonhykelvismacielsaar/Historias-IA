# REFERÊNCIAS VISUAIS — acervo do projeto

## 1. O QUE É "IMAGEM ORIGINAL" NESTE PROJETO — e a resposta honesta

Você pediu **"imagens originais"**. Isso precisa ser dito com clareza, porque muda a entrega:

| Tipo de imagem | Existe? | O que fazer |
|---|---|---|
| **Foto real** de Adão, do Éden, de Moisés, de Jesus | ❌ **Não existe.** Nenhuma câmera existia antes de 1826. Nada do que está em Gênesis 1–2 foi fotografado, porque **não havia ninguém lá para fotografar.** | Não é possível "baixar a foto certa". Quem mostrar "a foto do Éden" está mostrando uma ilustração, uma pintura ou uma imagem de IA. |
| **Fotografia real** de tudo que existe hoje: o Nilo, o Monte Sinai, o Mar Morto, o deserto do Negueve, Jerusalém, o Mar da Galileia, Roma, a ilha de Patmos | ✅ **Existe, e é de domínio público.** | É aqui que as imagens **originais** entram: usar **a geografia real** como base dos quadros. Foi o que fiz ao montar as referências abaixo. |
| **Gravura histórica** de Doré (século XIX) — a ilustração bíblica mais famosa que existe | ✅ **Domínio público** (Doré morreu em 1883) | **62 estampas baixadas e otimizadas** em `fontes/dore/` — cobrindo Gênesis → Apocalipse, em ordem narrativa. |
| **Imagem gerada por IA** com aspecto ultrarrealista | ✅ Fabricável | É o que você vai gerar. Os **prompts** estão prontos; as diretrizes de fidelidade histórica estão neste documento. |

**Conclusão prática:** o caminho correto não é "achar a foto do Éden" (não existe), é **reconstruir com fidelidade
histórica + geográfica + arqueológica**. Para isso:
1. Use **locação e geografia reais** (fotografadas).
2. Use **figurino, utensílio e arquitetura comprovados** pela arqueologia do período.
3. Use **traços étnicos corretos** para cada povo (não europeus genéricos).

---

## 2. O ACERVO BAIXADO NESTA ENTREGA

### `fontes/dore/` — 62 gravuras de Gustave Doré *(dominínio público)*
Fonte: *La Grande Bible de Tours*, 241 gravuras, digitalizadas por Felix Just, S.J. e distribuídas pelo
projeto Aionian Bible. Numeração e curadoria feitas por este projeto para cobrir a Bíblia inteira.
Cada arquivo é nomeado com o **episódio correspondente do roteiro geral**.

| Exemplos do acervo | |
|---|---|
| `EP01_A-Criacao-a-Luz.jpg` | Gn 1:3 — "Seja luz" |
| `EP02_A-Criacao-de-Eva.jpg` | Gn 2:21-22 — a formação da mulher |
| `EP03_Adao-e-Eva-expulsos-do-Eden.jpg` | Gn 3:24 |
| `EP06_O-mundo-destruido-pelas-aguas.jpg` | Gn 7 |
| `EP19_A-entrega-da-Lei-no-Monte-Sinai.jpg` | Êx 19–20 |
| `EP29_Davi-mata-Golias.jpg` | 1Sm 17 |
| `EP42_A-visao-do-vale-de-ossos-secos.jpg` | Ez 37 |
| `EP46_A-Anunciacao.jpg` / `EP46_O-nascimento-de-Jesus.jpg` | Lc 1–2 |
| `EP55_A-Ultima-Ceia.jpg` | Jo 13 |
| `EP77_A-Nova-Jerusalem.jpg` | Ap 21 |

Reproduzir: `bash tools/curar_referencias.sh`

### `fontes/referencias_geradas/` — 2 quadros-modelo prontos
Gerados a partir dos prompts deste projeto, já no estilo final da série (podem ir direto como
*first frame* no Seedance):

| Arquivo | Quadro do roteiro | Uso |
|---|---|---|
| `EP01_cena02_seja_luz.png` | **IMG-2.2** — a fenda de luz | abertura do EP 01, Cena 2 |
| `EP02_cena07_primeiro_encontro.png` | **IMG-16.6** — Adão e Eva frente a frente | clímax do EP 02 |

> ⚠️ **Aviso de uso:** são imagens geradas por IA para servirem de referência/modelo. Elas não são
> "os atores oficiais" — são **testes de direção de arte** para você validar o estilo antes de gerar
> os 78 quadros do EP 01 e 02.

### `fontes/imagens_referencia/` — referências de estilo
Reproduções de obras de **domínio público** (Doré, Michelangelo, Schnorr von Carolsfeld), usadas apenas
como **referência de composição e atmosfera** — não devem entrar no vídeo final.

---

## 3. REGRAS DE FIDELIDADE HISTÓRICA (para os prompts não errarem)

### PROIBIDO em qualquer imagem dos episódios 01 a 15 (era patriarcal, ~2000–1500 a.C.)
```
❌ qualquer metal trabalhado (ferro, bronze, aço)
❌ tecido tingido industrialmente, algodão, seda, botão, zíper, costura reta de máquina
❌ tijolo cozido, vidro, papel, pergaminho, escrita alfabética
❌ sandália com tiras modernas, óculos, relógio, tatuagem
❌ tons pastel de "desenho de igreja"; pele europeia clara
✅ linho e lã crus, sem tingimento, fiados à mão
✅ couro curtido cru, corda de fibra, madeira lascada, pedra lascada
✅ cerâmica feita à mão, sem torno
✅ pele morena-oliva (Levante), cabelo escuro ondulado, olhos escuros
```

### Por era (para os episódios seguintes)
| Era | Episódios | Pode aparecer | Não pode |
|-----|-----------|---------------|----------|
| **Pré-diluviana** (Gn 1–8) | 01–07 | barro, pedra, planta, pele, água | tudo fabricado |
| **Patriarcal** (Gn 12–50) | 09–15 | linho cru, couro, tenda de pelo de cabra, cerâmica à mão | metal, tijolo, cidades muradas de pedra grande |
| **Êxodo / deserto** | 16–23 | bronze, linho branco, tendas, ouro trabalhado (no Tabernáculo) | ferro em uso comum, templos de pedra |
| **Reino / Templo** (1Sm–2Rs) | 28–36 | ferro, pedra talhada, cedro, púrpura, ouro | vidro, arcos romanos |
| **Exílio e retorno** | 40–45 | cerâmica pintada babilônica, papiro, tijolo esmaltado | greco-romano tardio |
| **Evangelhos e Atos** | 46–63 | túnica de linho com costura, sandália de couro, sinagoga de pedra, moeda romana, denário | anacronismo bizantino, cruz como ornamento |
| **Apocalipse** | 70–77 | simbólico — não seguir regra realista; seguir o texto (Animais, Tronos, Taças, Cidade) |

### ⚠️ Regras de decência e de plataforma
1. **Deus nunca tem corpo.** Regra absoluta, em todos os episódios.
2. **Adão e Eva nus (Gn 2:25)** — enquadrar dos ombros para cima, contraluz, névoa, folhagem. Nunca
   mostrar nudez explícita: além de ser desnecessário para o texto, derruba o alcance em todas as
   plataformas.
3. **Cenas de violência** (dilúvio, pragas, crucifixão): mostrar **a consequência** e o **rosto de quem
   vê**, não o ato. É mais forte e passa em qualquer classificação.
4. **Nenhuma das estampas de Doré é de conteúdo explícito** — a seleção feita em `fontes/dore/` foi
   curada justamente para isso.

---

## 4. GEOGRAFIA REAL — usar como base fotográfica

Onde for possível, gere as imagens usando **a paisagem real** como referência. Isso é o que dá
"cara de verdade" à reconstrução:

| Passagem | Região real | O que serve |
|---|---|---|
| Gn 2 (Éden) | Mesopotâmia · confluência Tigre/Eufrates · Vale do Rift | rios largos, planícies aluviais, tamareiras, pântanos de junco |
| Gn 6–8 (Dilúvio) | Monte Ararate (Turquia) | cume vulcânico coberto de neve |
| Gn 12–50 (Patriarcas) | Negueve, Hebron, Beersheba, Siquém, Vale do Jordão | deserto pedregoso, tendas de beduínos, poços de pedra, acácias |
| Êx 1–15 | Delta do Nilo · Mar Vermelho (Golfo de Suez) | palmeiras, papiro, dunas, paredões |
| Êx 19–20 | Monte Sinai / Jebel Musa | granito vermelho, picos áridos, neblina de altitude |
| Js 1–12 | Jordão · Jericó (Tell es-Sultan) | rio turvo, oásis, tel arqueológico |
| 1–2 Sm | Vale de Elá · Jerusalém (Cidade de Davi) | colinas de calcário, cisternas |
| 1Rs 6–8 | Jerusalém (Monte do Templo) | pedra calcária dourada, cedro, talha |
| Mt–Jo | Mar da Galileia · Cafarnaum · Jardim do Getsêmani | basalto negro, sinagoga, oliveiras milenares |
| At–Ap | Roma · Éfeso · Patmos | ruínas clássicas, pedreiras, grutas |

---

## 5. FLUXO RECOMENDADO

```
1. Escolha o episódio no roteiro geral (roteiro/00_INDICE_GERAL_BIBLIA.md)
2. Leia o roteiro do episódio → pegue os IDs dos quadros (IMG-x.y)
3. Abra fontes/dore/EPxx_*.jpg  → referência de composição e atmosfera
4. Gere a imagem com o prompt do bloco de PROMPTS DE IMAGEM
5. Confira contra as REGRAS DE FIDELIDADE HISTÓRICA deste documento
6. Suba a imagem no Seedance 1.5 como first frame → use o prompt de vídeo correspondente
7. A narração da Voz entra na edição, por cima
```

---

## 6. O QUE NÃO FOI POSSÍVEL BAIXAR NESTE AMBIENTE — e o que fazer

A rede deste ambiente libera **apenas GitHub**; Wikimedia Commons, Gutenberg, Rijksmuseum e
Metropolitan Museum ficam bloqueados. Por isso, os acervos abaixo **não puderam ser baixados aqui**,
mas ficam registrados com o link para você baixar em 2 minutos, se quiser ampliar o acervo:

| Acervo | O que tem | Link |
|---|---|---|
| **Rijksmuseum** | Rembrandt bíblico em altíssima resolução, domínio público, download direto | `rijksmuseum.nl/en/rijksstudio` |
| **Metropolitan Museum (Open Access)** | Arte bíblica egípcia, assíria, grega e do Oriente Próximo, com dados abertos | `metmuseum.org/art/collection` |
| **Wikimedia Commons** | Categoria "Gustave Doré Bible illustrations" completa (241 estampas) | `commons.wikimedia.org` |
| **Prelinger / Internet Archive** | Filmagens reais de Israel, Egito, Jordânia, Turquia, em domínio público | `archive.org` |
| **NASA / ESA** | Imagens reais do planeta, do Sol e da Via Láctea, domínio público — **essenciais para as Cenas 1, 5 e 9 do EP 01** | `images.nasa.gov` |

> 💡 **Dica importante:** as cenas de espaço do EP 01 (IMG-5.1, 9.3 e 9.4) ficam **muito melhores**
> usando imagens reais da NASA como base (Via Láctea, curvatura da Terra, nascer do Sol orbital) do que
> deixando o gerador de IA inventar. São de domínio público e livres para uso comercial.

---

## 7. ATRIBUIÇÃO E LICENÇAS

### Acervo Doré (`fontes/dore/`)
> Ilustrações por **Gustave Doré** (1832–1883), da *La Grande Bible de Tours*.
> Obra em **domínio público** por falecimento do autor há mais de 70 anos.
> Digitalização compilada por **Felix Just, S.J.** — `catholic-resources.org/Art/Dore.htm`
> Distribuída por **Nainoia Inc** — `resources.aionianbible.org`
> Repositório: `github.com/Nainoia-Inc/AionianBible_GustaveDore_LaGrandeBibledeTours`

### Texto bíblico em hebraico (`dados/hebraico/WLC.json`)
> **Westminster Leningrad Codex**, via repositório `github.com/openscriptures/morphhb`
> Licença: **CC BY 4.0** — atribuição obrigatória.
> "Westminster Leningrad Codex (WLC) © 1998–2018 J. Alan Groves Center for Advanced Biblical Research.
> Licenciado sob Creative Commons Attribution 4.0 (CC BY 4.0)."

### Texto bíblico em grego (`dados/grego/BYZ.json`)
> **The New Testament in the Original Greek — Byzantine Textform**, editado por
> **Maurice A. Robinson e William G. Pierpont**. Repositório `github.com/byztxt/byzantine-majority-text`.
> **Domínio público** (byztxt está inativo; obra disponível para uso livre).

### Imagens de IA (`fontes/referencias_geradas/`)
> Geradas neste projeto por modelo de geração de imagem. Sem direitos de terceiros.

---

## 8. SOBRE "A TORÁ" E "O PRIMEIRO LIVRO"

Um esclarecimento que vale para todo o projeto:

- **Torá (תּוֹרָה)** = os **cinco** primeiros livros da Bíblia: **Gênesis, Êxodo, Levítico, Números e
  Deuteronômio**. É o "Pentateuco". A Torá **não é** só o primeiro livro.
- **O "primeiro livro da Bíblia"** = **Gênesis**, que tem **50 capítulos** e termina com **José no Egito**
  (Gn 50:26) — **não** com a criação nem com o Éden.
- **Nesta entrega:** os **dois primeiros capítulos de Gênesis** estão completos em hebraico original
  e traduzidos por mim, verso por verso. **Gênesis 3 até Gênesis 50** segue no roteiro geral (EP 03 a EP 15)
  e **Êxodo a Deuteronômio** nos EP 16 a 23 — basta pedir os episódios em sequência.
- **Todo o corpus necessário já está baixado no seu repositório** (`dados/`): os **39 livros do
  Antigo Testamento em hebraico (23.213 versículos)** e os **27 livros do Novo Testamento em grego
  (7.953 versículos)**. Nada mais precisa ser baixado para escrever qualquer episódio.
