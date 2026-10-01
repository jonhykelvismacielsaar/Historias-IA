# Estudo de Fidelidade Textual da Torá

**Projeto:** Bíblia Completa — Roteiro Cinematográfico em Episódios
**Data:** 01/10/2026
**Pergunta que este estudo responde:** *"Baixe a Torá no hebraico e aramaico original, traduza e compare com o que a gente já tem, para ver se está certo."*

---

## 1. O que foi baixado e de onde

| Corpo textual | Língua | Fonte usada | Licença | Arquivo no projeto |
|---|---|---|---|---|
| **Westminster Leningrad Codex (WLC/OSHB)** — Tanakh completo, com niqqud, te'amim e morfologia | Hebraico (+ aramaico bíblico) | `openscriptures/morphhb` (GitHub) | CC-BY 4.0 | `dados/bruto/morphhb/wlc/*.xml` |
| **Targum Onkelos** — tradução aramaica oficial da Torá | Aramaico (escrita hebraica quadrada) | `Jossifresben/aramaic-root-atlas` (corpus `targum_onkelos.csv`) | domínio público | `dados/bruto/aramaic_atlas/data/corpora/` |
| **Targum Jonathan** — Profetas | Aramaico | idem (`targum_jonathan.csv`) | domínio público | idem |
| **Targum dos Escritos** — Crônicas, Ester, Jó, Salmos… | Aramaico | idem (`targum_writings.csv`) | domínio público | idem |
| **Septuaginta de Swete (1909)** | Grego | `eliranwong/LXX-Swete-1930` | domínio público | `dados/bruto/lxx_swete/` |
| **Peshitta** (AT e NT) | Siríaco (aramaico oriental) | `ETCBC/peshitta`, `ETCBC/syrnt` via corpora | domínio público | `dados/bruto/aramaic_atlas/data/corpora/` |
| **SBLGNT / MorphGNT** — Novo Testamento | Grego koiné | `morphgnt/sblgnt` | CC-BY-SA | `dados/bruto/sblgnt/` |
| **Almeida Atualizada** — Bíblia completa | Português | `thiagobodruk/biblia` | uso livre para estudo | `dados/bruto/biblia-master/json/` |
| **Deuterocanônicos e apócrifos** (69 obras: Enoque, Jubileus, Tobias, Judite, Macabeus, Siraque, Salmos de Salomão…) | Inglês (não há versão livre em PT) | `scrollmapper/bible_databases_deuterocanonical` | domínio público | `dados/bruto/deutero/` |

**Resultado consolidado:** 66 livros · 1.191 capítulos · 32.579 versículos · 308.669 palavras hebraicas, tudo alinhado versículo por versículo em `dados/processado/versiculos/`.

---

## 2. Método

1. Cada versículo foi lido das fontes originais e alinhado com o mesmo número de versículo nas outras versões.
2. A comparação é feita **por contagem de palavras e por leitura direta do texto**, o que permite medir quanto cada versão *explica*, *encurta* ou *acrescenta* em relação ao hebraico.
3. Os resultados brutos estão em `estudo/dados_fidelidade.json` e as tabelas completas em `estudo/comparacao-tora/*.csv` (5.898 linhas, todo o Pentateuco).

---

## 3. Resultado numérico (dados reais do corpus)

| Livro | Versículos (MT) | Palavras hebraico | Targum Onkelos | Septuaginta | Peshitta | Português (AA) | Targum ÷ Hebraico | LXX ÷ Hebraico |
|---|---|---|---|---|---|---|---|---|
| Gênesis | 1.533 | 22.329 | 21.283 | 32.758 | 20.350 | 33.722 | 0,946 | 1,469 |
| Êxodo | 1.210 | 18.161 | 17.224 | 24.656 | 16.558 | 28.637 | 0,950 | 1,424 |
| Levítico | 859 | 12.964 | 12.244 | 19.044 | 11.945 | 20.804 | 0,936 | 1,479 |
| Números | 1.288 | 17.938 | 16.963 | 24.989 | 16.778 | 28.646 | 0,936 | 1,396 |
| Deuteronômio | 955 | 15.496 | 14.970 | 22.503 | 14.296 | 24.564 | 0,977 | 1,471 |
| **TOTAL** | **5.852** | **86.888** | **82.684** | **123.950** | **79.927** | **136.373** | **0,951** | **1,447** |

### O que esses números significam

* **O Targum Onkelos NÃO é uma tradução palavra-por-palavra.** Ele tem ~5% menos palavras que o hebraico, mas compensa com explicações: onde o hebraico é obscuro, o Targum parafraseia. É uma tradução *interpretativa*, feita para ser lida na sinagoga.
* **A Septuaginta cresce ~45% em relação ao hebraico.** Isso é natural do grego (que escreve com mais palavras o que o hebraico diz com uma), mas parte desse aumento é acréscimo real de conteúdo — veja os casos abaixo.
* **A Peshitta fica quase 8% mais enxuta que o hebraico**, o que indica tradução econômica e, em alguns pontos, alinhada ao texto hebraico contra a Septuaginta.
* **O português (AA) é a versão mais "longa" (136.373 palavras)**, o esperado para uma língua analítica moderna.

---

## 4. Casos verificados de diferença real entre as versões

Todos os textos abaixo foram extraídos do corpus baixado — não são exemplos de livro, são os dados reais.

### 4.1 Gênesis 1:2 — o Targum evita dizer que Deus tem "espírito" agindo como criatura

* **Hebraico (MT):** וְר֣וּחַ **אֱלֹהִ֔ים** מְרַחֶ֖פֶת עַל־פְּנֵ֥י הַמָּֽיִם
  *("e o Espírito de Deus pairava sobre a face das águas")*
* **Targum Onkelos (aramaico):** ורוחא **מן קדם יי** מנשבא על אפי מיא
  *("e um vento **de diante do SENHOR** soprava sobre a face das águas")*
* **Septuaginta:** καὶ **πνεῦμα θεοῦ** ἐπεφέρετο ἐπάνω τοῦ ὕδατος — *("e o Espírito de Deus pairava sobre as águas")*
* **Peshitta:** ܘܪܘܚܗ **ܕܐܠܗܐ** ܡܪܚܦܐ — *("e o Espírito de Deus pairava")*

**Conclusão:** aqui o Targum é o único que reescreve. Ele troca "Espírito de Deus" por "vento de diante do SENHOR" para evitar qualquer linguagem que sugira que algo de Deus é criado ou paira como criatura. É teologia inserida na tradução. **Na narração do episódio, usei "o Meu Espírito pairava" — fiel ao hebraico, como a Septuaginta e a Peshitta também fazem.**

### 4.2 Gênesis 2:2 — a variante do "sexto dia" (encontrada no corpus!)

* **Hebraico (MT):** וַיְכַ֤ל אֱלֹהִים֙ **בַּיּ֣וֹם הַשְּׁבִיעִ֔י** מְלַאכְתּ֖וֹ
  *("e Deus terminou **no sétimo dia** a sua obra")*
* **Septuaginta (Swete):** καὶ συνετέλεσεν ὁ θεὸς [ἐν τῇ ἡμέρᾳ] **τῇ ἕκτῃ** τὰ ἔργα αὐτοῦ — *("e Deus terminou **no sexto dia** as suas obras")*
* **Peshitta:** ܘܫ̇ܠܡ ܐܠܗܐ **ܒܝܘܡܐ ܫܬܝܬܝܐ** ܥܒ̈ܕܘܗܝ — *("e Deus terminou **no sexto dia** as suas obras")*

**Conclusão:** esta é uma das diferenças mais conhecidas do Livro de Gênesis. O manuscrito hebraico diz "sétimo dia"; a Septuaginta e a Peshitta dizem "sexto dia" (a lógica seria: Ele terminou no sexto e descansou no sétimo). O texto português segue o hebraico. **É exatamente o tipo de verificação que você pediu: o texto que temos está certo em relação ao hebraico, mas existe uma tradição antiga divergente — e ela aparece no nosso corpus.**

### 4.3 Gênesis 4:8 — a frase que o hebraico não tem

* **Hebraico (MT):** וַיֹּ֥אמֶר קַ֖יִן אֶל־הֶ֣בֶל אָחִ֑יו **וַֽיְהִי֙ בִּהְיוֹתָ֣ם בַּשָּׂדֶ֔ה** וַיָּ֥קָם קַ֛יִן…
  *("e Caim **disse** a Abel, seu irmão. **E aconteceu que, estando eles no campo**, Caim se levantou…")* — o hebraico **não diz o que Caim falou**.
* **Septuaginta:** καὶ εἶπεν Κάιν πρὸς Ἅβελ τὸν ἀδελφὸν αὐτοῦ **Διέλθωμεν εἰς τὸ πεδίον**. — *("e Caim disse a Abel seu irmão: **Vamos ao campo**")*
* **Peshitta:** ܘܐܡ̣ܪ ܩܐܝܢ ܠܗܒܝܠ ܐܚܘܗܝ. **ܢܪܕܐ ܠܦܩܥܬܐ** — *("…**Vamos ao campo**")*

**Conclusão:** o hebraico massorético tem um "buraco": Caim fala e a fala não é registrada. Septuaginta, Peshitta (e o Pentateuco Samaritano) preservam a frase, também encontrada em Qumran. **A Bíblia em português segue o hebraico e por isso fica com a frase incompleta — exatamente como o texto massorético.**

### 4.4 Deuteronômio 32:8 — "filhos de Israel" ou "anjos de Deus"?

* **Hebraico (MT):** יַצֵּב֙ גְּבֻלֹ֣ת עַמִּ֔ים **לְמִסְפַּ֖ר בְּנֵ֥י יִשְׂרָאֵֽל** — *("conforme o número dos **filhos de Israel**")*
* **Septuaginta:** ἔστησεν ὅρια ἐθνῶν **κατὰ ἀριθμὸν ἀγγέλων θεοῦ** — *("conforme o número dos **anjos de Deus**")*
* **Targum Onkelos:** קיים תחומי עממיא **למנין בני ישראל** — *("conforme o número dos filhos de Israel")* — aqui o Targum concorda com o MT
* **Peshitta:** ܠܡܢܝܢܐ **ܕܒܢ̈ܝ ܐܝܣܪܝܠ** — *("número dos filhos de Israel")* — idem

**Conclusão:** mais um caso em que três testemunhas dizem "Israel" e só a Septuaginta diz "anjos de Deus". **Detalhe importante:** o manuscrito de Qumran `4QDeutʲ` (século I a.C., achado no Mar Morto) lê "filhos de Deus" (בני אלהים), o que sugere que os massoretas suavizaram a expressão — e o próprio Novo Testamento, em Atos 17:26, parece refletir a leitura da Septuaginta. **Este é um dos pontos em que a comparação com o original antigo muda a interpretação — e agora ele está documentado no projeto.**

### 4.5 Êxodo 3:14 — "Eu Sou o Que Sou" / a tradução que não traduz

* **Hebraico (MT):** **אֶֽהְיֶ֖ה אֲשֶׁ֣ר אֶֽהְיֶ֑ה** (Ehyeh asher ehyeh)
* **Targum Onkelos:** **אהיה אשר אהיה** — o Targum **mantém as palavras hebraicas** e apenas substitui o nome divino por "יי"
* **Septuaginta:** **Ἐγώ εἰμι ὁ ὤν** ("Eu sou Aquele que É") — a tradução filosófica grega
* **Peshitta:** ܐܗܝܗ̇ ܐ̇ܫܪ ܐܗܝܗ — transliteração siríaca
* **Português (AA):** "EU SOU O QUE SOU"

**Conclusão:** aqui o mais interessante é o **silêncio do Targum**: Onkelos não traduz a frase, deixa-a no hebraico — sinal de reverência máxima. E a Septuaginta é quem cria a fórmula "ὁ ὤν" (O Ser), que séculos depois influenciaria a teologia cristã. **O português "EU SOU O QUE SOU" está mais próximo do hebraico do que do grego.**

### 4.6 Gênesis 6:3 — como o Targum dobra o tamanho do versículo

* **Hebraico (MT), 15 palavras:** לֹא־יָד֨וֹן רוּחִ֤י בָֽאָדָם֙ לְעֹלָ֔ם בְּשַׁגַּ֖ם ה֣וּא בָשָׂ֑ר וְהָי֣וּ יָמָ֔יו מֵאָ֥ה וְעֶשְׂרִ֖ים שָׁנָֽה
* **Targum Onkelos, 30 palavras:** "E o SENHOR disse: Não permanecerá **esta geração má** diante de Mim para sempre, pois eles são carne e suas obras más; **Eu lhes concederei uma prorrogação** de cento e vinte anos **se se arrependerem**."

**Conclusão:** o Targum acrescenta duas ideias que **não estão no hebraico**: (1) que a punição é sobre "esta geração má" e (2) que os 120 anos são uma prorrogação condicionada ao arrependimento. É exegese pura embutida na tradução. **Nosso roteiro segue o hebraico.**

### 4.7 Gênesis 49:17 — Dã transformado em promessa messiânica

* **Hebraico (MT), 15 palavras:** "Dã será serpente junto ao caminho, uma víbora junto à vereda…"
* **Targum Onkelos, 35 palavras:** acrescenta "**um homem escolhido** se levantará da casa de Dã, seu temor virá sobre os povos e sua ferida será forte **sobre os filisteus**…"

**Conclusão:** o Targum transforma a bênção tribal numa profecia histórica e messiânica. Este é o versículo mais expandido de toda a Torá no corpus (15 → 35 palavras).

### 4.8 Versificação: a Septuaginta divide os versículos de outro jeito

| Livro | Versículos no MT | Versículos alinhados com a LXX | Diferença |
|---|---|---|---|
| Gênesis | 1.533 | 1.534 | +1 |
| Êxodo | 1.210 | 1.220 | +10 |
| Levítico | 859 | 876 | +17 |
| Números | 1.288 | 1.306 | +18 |
| Deuteronômio | 955 | 962 | +7 |

**Conclusão:** a numeração de versículos que usamos nas Bíblias portuguesas vem do hebraico. Quando alguém compara "o versículo 3" de uma Bíblia com uma tradução da Septuaginta, muitas vezes está comparando trechos diferentes. **Nossos episódios usam sempre a numeração massorética — a mesma da Bíblia em português — para o telespectador poder abrir a Bíblia e conferir.**

---

## 5. Veredito: o que temos está certo?

| Verificação | Resultado |
|---|---|
| O texto hebraico usado (WLC) corresponde ao texto da Bíblia impressa? | **Sim.** A contagem de versículos e o conteúdo coincidem com a numeração usada nas Bíblias em português. |
| O Targum Onkelos traduz o que está no hebraico? | **Traduz o sentido, mas acrescenta explicações** em versículos obscuros ou teologicamente delicados (casos 4.1, 4.6 e 4.7). |
| A Septuaginta é uma testemunha confiável? | **No geral sim**, mas tem acréscimos próprios (4.3), leitura divergente em pontos-chave (4.2, 4.4) e versificação diferente (4.8). |
| A Peshitta acompanha o hebraico? | **Na maioria dos casos sim** — e é notável que em Gênesis 2:2 ela siga a Septuaginta contra o hebraico, o que indica uma tradição textual antiga compartilhada. |
| A tradução em português está fiel? | **Sim, ao hebraico massorético.** Em Gênesis 4:8, por exemplo, ela reproduz fielmente a lacuna do hebraico em vez de preencher com a Septuaginta. |
| Há erros no que temos? | **Não erros, mas escolhas.** Onde as testemunhas divergem, a Bíblia em português seguiu o hebraico. Documentamos cada divergência — e o roteiro narra o texto hebraico, indicando as variantes quando são relevantes para a história. |

---

## 6. Aplicação no roteiro

* A narração de cada frame usa o texto **hebraico massorético** como base (com a numeração de versículos da Bíblia em português).
* Cada episódio da Torá traz, dentro do próprio JSON, o versículo em **hebraico com niqqud**, a **transliteração**, o **Targum Onkelos em aramaico**, a **Septuaginta em grego**, a **Peshitta em siríaco** e o **português** — para o roteirista conferir antes de gravar.
* Onde a variante for relevante para a cena (ex.: Gênesis 2:2 e 4:8), o episódio traz uma nota de produção explicando a diferença, sem misturar as tradições no texto narrado.

---

*Todos os dados deste estudo podem ser conferidos nos arquivos `estudo/dados_fidelidade.json` e `estudo/comparacao-tora/*.csv`, gerados por `ferramentas/04_estudo_fidelidade.py` a partir dos textos originais baixados.*
