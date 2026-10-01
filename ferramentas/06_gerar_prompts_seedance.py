#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
06_gerar_prompts_seedance.py — Gera as FOLHAS DE PROMPT para produção.

Para cada episódio, cada frame recebe:
  1) PROMPT DE IMAGEM ......... para gerar o quadro na IA de imagem (Midjourney/Flux/SDXL)
  2) PROMPT DE VÍDEO .......... para o Seedance 1.5 Pro, COM A FALA DENTRO, para gerar o
                                frame de 5 segundos já com a voz e o som.
  3) FALA (PT-BR) ............. a linha exata que o narrador diz, para conferência
  4) AJUSTES .................. duração, proporção, áudio ligado (sem legendas: não usar texto na tela)
  5) AJUSTES .................. duração, proporção, áudio ligado etc.

Formato do prompt de vídeo — as 4 camadas que o Seedance 1.5 Pro entende
(ver guias oficiais e da fal.ai/GPTunneL):
    Camada 1 ... sujeito + ação (o que acontece na cena)
    Camada 2 ... diálogo, sempre ENTRE ASPAS, com locutor, idioma e tom
    Camada 3 ... som ambiente e efeitos (uma fonte por vez, sem contradição)
    Camada 4 ... estilo visual e clima

Uso:
    python3 ferramentas/06_gerar_prompts_seedance.py            # todos os episódios
    python3 ferramentas/06_gerar_prompts_seedance.py EP-0001    # um episódio
"""

from __future__ import annotations

import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURADORIA = os.path.join(RAIZ, "roteiro", "curadoria")
SAIDA = os.path.join(RAIZ, "prompts")

DURACAO_S = 5
LARGURA = 78

# ---------------------------------------------------------------------------
# ESTILO — reaproveitado do 03_gerar_episodio.py
# ---------------------------------------------------------------------------
ESTILO_IMAGEM_EN = (
    "Hyper-realistic cinematic oil painting on coarse linen canvas, thick impasto brushwork with "
    "glistening wet paint ridges, museum-grade baroque realism fused with photoreal detail, dramatic "
    "chiaroscuro, volumetric god-rays, immense biblical scale, epic composition, rich earthy palette of "
    "ochre, deep umber, crimson and gold, subtle craquelure of old varnish, shallow depth of field, "
    "ultra-detailed canvas weave, 8k, masterpiece"
)

PINCEL_EN = (
    "a single large wooden-handled artist's brush floating in mid-air at the edge of the composition, "
    "bristles wet with fresh pigment, a gleaming trail of just-painted paint behind it, clearly mid-stroke"
)
SEM_PINCEL_EN = (
    "no brush visible in this frame, no painter, no human figure present, the painting already alive on its own"
)

NEGATIVO_IMAGEM = (
    "text, letters, numbers, subtitles, captions, burned-in words, lower thirds, titles, watermark, signature, logo, "
    "human face of God, depiction of the divine "
    "figure, cartoon, cgi look, low resolution, blurry, deformed anatomy, extra limbs, modern objects, anachronism"
)

# ---------------------------------------------------------------------------
# Tradução do vocabulário de som (SFX) e da trilha para o prompt em inglês
# ---------------------------------------------------------------------------
SFX_EN = {
    "abelhas e vida surgindo": "bees buzzing, small life stirring",
    "anel de ondulação": "a ring of water ripples spreading outward",
    "animais ao longe": "distant animals",
    "animais pastando": "animals grazing and chewing",
    "asas batendo": "beating wings",
    "asas em uníssono": "wings beating in unison",
    "aves ao longe": "distant birds",
    "batimento cardíaco": "a slow deep heartbeat",
    "batimento cardíaco grave, quase inaudível, a 30 Hz": "a deep, barely audible heartbeat",
    "bolhas": "bubbles rising",
    "broto rompendo": "a shoot breaking through the soil",
    "broto rompendo a terra": "shoots breaking through the soil",
    "canto de baleia grave": "a deep whale call",
    "cardume rompendo": "a shoal of fish breaking the surface",
    "cascos": "hooves on dry ground",
    "cintilância cristalina": "crystalline shimmering",
    "ciscar de aves": "birds pecking at the ground",
    "coro a duas vozes": "a two-voice choir",
    "coro alegre": "a joyful choir",
    "coro amplo": "a broad choir",
    "coro baixo sustentado": "a low sustained choir",
    "coro distante e etéreo": "a distant ethereal choir",
    "coro em duas vozes": "a two-voice choir",
    "coro entrando": "a choir entering",
    "coro etéreo": "an ethereal choir",
    "coro etéreo quase inaudível": "a barely audible ethereal choir",
    "coro pleno": "a full choir",
    "coro suave entrando": "a soft choir entering",
    "crescendo de cordas muito graves": "a crescendo of very low strings",
    "duas respirações": "two soft breaths",
    "eco imenso": "a vast echo",
    "eco profundo": "a deep echo",
    "encaixe suave": "a soft settling click",
    "ervas sendo abertas": "grass being parted",
    "estalos de plasma": "crackling plasma",
    "estalos delicados de tinta": "the delicate flicking of wet paint",
    "estrelas": "faint star twinkling",
    "feixes de luz": "shafts of light",
    "folhas": "rustling leaves",
    "folhas se abrindo": "leaves unfurling",
    "fruto colhido": "fruit being picked",
    "frutos balançando": "fruit swaying on the branch",
    "gaivotas distantes": "distant seagulls",
    "gota caindo": "a single drop falling",
    "gotejar ecoando no vazio": "dripping echoing in the void",
    "grilos": "crickets",
    "grilos distantes no lado da noite": "distant crickets on the night side",
    "gritos de aves": "birds crying out",
    "impacto colossal de subgraves": "a colossal sub-bass impact",
    "impacto de luz, som metálico brilhante": "a bright metallic burst of light",
    "impacto luminoso": "a luminous impact",
    "impacto luminoso suave": "a soft luminous impact",
    "madeira rangendo levemente": "wood creaking faintly",
    "mar recuando": "the sea drawing back",
    "maré": "the tide turning",
    "nota sustentada de violoncelo": "a sustained cello note",
    "nota sustentada muito longa": "a very long sustained note",
    "nuvens": "high clouds",
    "ondas em pedra": "waves breaking on stone",
    "ondas mansas": "gentle waves",
    "ondas pesadas": "heavy ocean swells",
    "ondas quebrando em pedra": "waves breaking on black pebbles",
    "ondulações": "ripples",
    "peixes saltando em sequência": "fish leaping one after another",
    "pincel pousando suavemente": "the brush settling softly onto the linen",
    "pincel raspando a borda": "the brush wiping against the canvas edge",
    "primeira chuva": "the first rain beginning to fall",
    "primeiras gotas de chuva": "the first raindrops",
    "primeira respiração": "a first breath",
    "pulsação rítmica de relógio natural": "a slow natural rhythmic pulse",
    "pulsação subgrave": "a sub-bass pulse",
    "pássaros distantes insinuando o dia 5": "distant birdsong",
    "queda de gota de tinta": "a drop of paint falling",
    "respiração": "slow breathing",
    "respiração lenta e distante": "slow distant breathing",
    "respiração profunda do mundo criado": "the deep slow breathing of the created world",
    "reverb infinito": "infinite reverb",
    "revoada": "a flock taking off at once",
    "rocha rachando": "rock cracking",
    "rugido distante": "a distant roar",
    "selo de vidro": "glass sealing shut",
    "silêncio": "near-total silence",
    "silêncio absoluto (−60 dB)": "absolute silence",
    "silêncio amplo": "a wide open silence",
    "silêncio de expectativa": "an expectant silence",
    "silêncio do fim do dia": "the silence of the end of the day",
    "silêncio quase total": "almost total silence",
    "silêncio que permanece depois do corte": "silence that lingers",
    "silêncio radiante": "a radiant silence",
    "silêncio radiante depois": "a radiant silence afterwards",
    "silêncio súbito": "sudden silence",
    "silêncio tenso": "a tense silence",
    "sino do quarto dia": "a single soft bell marking the fourth day",
    "sino do quinto dia": "a single soft bell marking the fifth day",
    "sino do segundo dia": "a single soft bell marking the second day",
    "sino do sexto dia": "a single soft bell marking the sixth day",
    "sino do terceiro dia": "a single soft bell marking the third day",
    "sino suave marcando o fim do dia": "a soft bell marking the end of the day",
    "sino único": "one single bell",
    "som lunar cristalino e frio": "a cold crystalline chime",
    "som solar grave e quente": "a warm deep solar hum",
    "sopro": "a low breath of wind",
    "sopro criador": "a low creator's breath of wind",
    "sopro grave": "a deep breath of wind",
    "suco estalando": "juice bursting from fruit",
    "tambores marciais suaves": "soft martial drums",
    "tela recebendo tinta, som de pincel em linho": "bristles dragging across raw linen",
    "tensão em corda fina": "a thin tense string",
    "tinkles cristalinos de estrelas": "crystalline twinkling",
    "tinta estalando": "wet paint crackling as it dries",
    "tinta fina sendo traçada": "a fine line of paint being drawn",
    "tinta se separando": "wet paint pulling apart",
    "toda a vida soando junta": "all of life sounding together",
    "transição tonal": "a soft tonal shift",
    "transição tonal suave": "a soft tonal shift",
    "trovões distantes": "distant thunder",
    "vapor": "hissing steam",
    "ventania leve no capim": "wind moving through grass",
    "vento": "wind",
    "vento alto": "high wind",
    "vento cortando": "cutting wind",
    "vento leve": "a light breeze",
    "vento na planície": "wind over the plain",
    "vento nas folhas": "wind in the leaves",
    "vento no trigo": "wind through wheat",
    "vento suave": "a soft breeze",
    "vida selvagem em movimento": "wildlife in motion",
    "vidro surgindo": "glass forming",
    "vidro vibrando suavemente": "glass humming softly",
    "whoosh de expansão": "an expanding whoosh",
    "zinido cristalino": "a crystalline ring",
    "zumbido ascendente": "a rising hum",
    "zumbido cósmico profundo": "a deep cosmic hum",
    "água agitada": "churning water",
    "água fervilhando de vida": "water boiling with life",
    "água ondulando": "rippling water",
    "água pesada": "heavy water",
    "água profunda": "deep underwater ambience",
    "água recuando": "water retreating",
    "água suspensa": "suspended water shimmering overhead",
    "água suspensa vibrando": "suspended water vibrating overhead",
}

TRILHA_EN = {
    "arpejos ascendentes de harpa": "ascending harp arpeggios",
    "celesta e sinos, notas pingadas como estrelas": "celesta and bells, notes plucked like stars",
    "clímax de percussão e metais": "a climax of percussion and brass",
    "clímax orquestral de toda a criação": "the full orchestral climax of creation",
    "clímax orquestral: coro, metais e tímpanos": "an orchestral climax with choir, brass and timpani",
    "coda serena com harpa": "a serene coda with harp",
    "corda grave sustentada, quase silêncio": "one sustained low string, almost silence",
    "cordas amplas, sensação de alívio": "broad strings, a feeling of relief",
    "cordas ascendentes e resolvidas": "ascending, resolving strings",
    "cordas e piano em movimento de queda suave": "strings and piano in a gentle falling motion",
    "cordas em arpejo ascendente": "strings in ascending arpeggio",
    "cordas em crescendo, harpa e sinos": "strings crescendo, harp and bells",
    "cordas em nota suspensa": "strings holding a suspended note",
    "cordas em ostinato, sensação de passagem do tempo": "ostinato strings, the passing of time",
    "cordas graves em movimento de recuo": "low strings receding",
    "cordas leves e flautas, pastoril": "light pastoral strings and flutes",
    "cordas muito graves, quase um gemido": "very low strings, almost a groan",
    "cordas pastoris em movimento contínuo": "pastoral strings in continuous motion",
    "cordas rápidas e leves, flautas": "fast light strings and flutes",
    "cordas suspensas, algo por vir": "suspended strings, something about to happen",
    "corta para quase silêncio, só uma nota de piano suspensa": "near-silence with one suspended piano note",
    "dois temas em contraponto, resolvendo em harmonia": "two themes in counterpoint resolving into harmony",
    "dois temas simultâneos, um em maior e um em menor": "two simultaneous themes, one major and one minor",
    "drone grave e suspenso": "a low suspended drone",
    "drone grave, tensão contínua": "a low drone of continuous tension",
    "entra o tema principal da série, em piano solo": "the main theme entering on solo piano",
    "entra um drone de violoncelo, pianíssimo": "a cello drone entering, pianissimo",
    "harpa e cordas em glissando ascendente": "harp and strings in an ascending glissando",
    "metais graves introduzindo o tema de autoridade": "low brass introducing the theme of authority",
    "percussão de tambores graves entrando": "deep drums entering",
    "piano solo, notas isoladas e suspensas": "solo piano, isolated suspended notes",
    "primeiro clímax da temporada: coro e metais": "the season's first climax with choir and brass",
    "silêncio total; apenas um drone subgrave entrando aos poucos": "total silence with a sub-bass drone fading in",
    "sustentação de cordas, sem percussão": "sustained strings, no percussion",
    "tema com flautas suaves": "the theme with soft flutes",
    "tema completo, cordas e coro suave; coda suspensa para o próximo episódio": "the full theme with strings and soft choir, ending in a suspended coda",
    "tema em versão ampla e luminosa": "the theme in a broad luminous version",
    "tema em versão jubilosa": "the theme in a jubilant version",
    "tema em versão serena, com sino": "the theme in a serene version with a bell",
    "tema principal completo com orquestra": "the full main theme with orchestra",
    "tema principal em modo maior, jubiloso": "the main theme in major, jubilant",
    "tema principal em sua forma mais terna, violino solo": "the main theme at its most tender, solo violin",
    "tema principal em versão ampla": "the main theme in a broad version",
    "tema principal em versão desacelerada, quase terminando": "the main theme slowing down, almost finished",
    "tema principal em versão esperançosa; termina com um sino suspenso": "the main theme in a hopeful version, ending on a suspended bell",
    "tema principal em versão final, completa, deixando a última nota suspensa": "the main theme in its final complete version, last note left hanging",
    "tema principal, piano e cordas, entrando suave": "the main theme on piano and strings, entering softly",
    "uma única nota de piano que fica soando; nenhum outro instrumento": "a single piano note ringing, nothing else",
}

# Apelidos: como o usuário chama cada episódio (o prelúdio é o "episódio zero")
APELIDOS = {
    "EP-0001": ("EPISODIO-00", "PRELUDIO"),
    "EP-0002": ("EPISODIO-01", "NO-PRINCIPIO"),
    "EP-0003": ("EPISODIO-02", "LUMINARES-PEIXES-AVES"),
    "EP-0004": ("EPISODIO-03", "IMAGEM-BENCAO-SETIMO-DIA"),
}


def traduzir(dicionario: dict, termo: str) -> str:
    return dicionario.get(termo, termo)


# ---------------------------------------------------------------------------
def montar_prompt_imagem(frame: dict) -> str:
    pincel = PINCEL_EN if frame.get("pincel", True) else SEM_PINCEL_EN
    luz = frame.get("luz_en", "dramatic volumetric light")
    partes = [
        frame["imagem_scene_en"].strip().rstrip(".") + ".",
        ESTILO_IMAGEM_EN + ".",
        pincel + ".",
        f"Lighting and mood: {luz}.",
        "Aspect ratio 16:9 horizontal widescreen, composition leaving clean negative space at the bottom for a golden day-line.",
    ]
    return " ".join(partes)


def montar_prompt_video(frame: dict) -> str:
    """Prompt para o Seedance 1.5 Pro, em 4 camadas, com a fala dentro."""
    fala = (frame.get("narracao") or "").strip()
    movimento = frame.get("video_movimento_en", "").strip().rstrip(".")
    camera = frame.get("camera_en", "slow cinematic dolly-in").strip().rstrip(".")
    # O Seedance se confunde com sinais opostos no áudio: separamos os sons
    # "silenciosos" dos "sonoros" e limitamos a 3 fontes por frame.
    sons, silencios = [], []
    for termo in frame.get("sfx", []):
        traducao = traduzir(SFX_EN, termo)
        if "silence" in traducao.lower() or traducao.lower().startswith("silence"):
            silencios.append(traducao)
        else:
            sons.append(traducao)
    escolhidos = sons[:3] + silencios[:1]
    sfx = ", ".join(escolhidos)
    trilha = traduzir(TRILHA_EN, frame.get("trilha", "")) if frame.get("trilha") else ""

    # Camada 1 — sujeito e ação
    camada1 = (
        "Using the uploaded image as the first frame and keeping the exact oil-painting look, "
        f"the painted scene comes alive: {movimento}. "
        "The wet brushstrokes dissolve into real three-dimensional matter as the camera moves in."
    )
    # Camada 2 — diálogo (entre aspas, com locutor, idioma e tom)
    camada2 = (
        "Dialogue: a disembodied off-camera narrator with a deep, calm, ancient masculine voice — "
        "no visible speaker anywhere in the scene, no mouth moving, no person appearing — says in "
        f'Brazilian Portuguese, slowly and solemnly, one time only: "{fala}"'
    )
    # Falas de personagens humanos (quando existirem na cena, com lip-sync)
    for fala_personagem in (frame.get("falas_personagens") or []):
        if isinstance(fala_personagem, dict):
            quem = fala_personagem.get("personagem", "the character")
            linha = fala_personagem.get("fala", "")
            tom = fala_personagem.get("tom", "natural and emotional")
        else:
            quem, linha, tom = "the character", str(fala_personagem), "natural and emotional"
        camada2 += (
            f' Then {quem} speaks in Brazilian Portuguese, {tom}, lips synced to the words, '
            f'one short line only: "{linha}" Nobody else speaks and nobody overlaps.'
        )
    # Camada 3 — som ambiente e efeitos
    camada3 = f"Sound effects: {sfx}." if sfx else ""
    if trilha:
        camada3 += f" Music kept low and soft under the voice: {trilha}."
    # Camada 4 — estilo visual e clima
    camada4 = (
        f"Camera: {camera}. Style: hyper-realistic oil painting brought to life, baroque biblical epic, "
        "volumetric light, floating dust, 24fps, photographic motion blur. Absolutely no text of any kind on "
        "screen: no subtitles, no captions, no burned-in words, no lower thirds, no titles, no watermarks, no logos, "
        "no extra people."
    )
    return " ".join(p for p in (camada1, camada2, camada3, camada4) if p)


def folha_do_episodio(caminho: str) -> tuple:
    # A curadoria traz os campos criativos (movimento, câmera, som);
    # o episódio gerado traz o cabeçalho já com a passagem e o texto bíblico.
    with open(caminho, encoding="utf-8") as fh:
        cur = json.load(fh)
    numero = cur["id"]
    caminho_ep = os.path.join(RAIZ, "roteiro", "episodios", f"{numero}.json")
    ep = dict(cur)
    if os.path.exists(caminho_ep):
        with open(caminho_ep, encoding="utf-8") as fh:
            gerado = json.load(fh)
        ep.update({
            "passagem": gerado.get("passagem", cur.get("referencia", "")),
            "livro": gerado.get("livro", cur.get("nome_livro", "")),
            "temporada": gerado.get("temporada", cur.get("temporada_nome", "")),
            "narrador": gerado.get("narrador", {"personagem": "DEUS"}),
        })
    else:
        ep["passagem"] = cur.get("referencia", "")
    apelido, tema = APELIDOS.get(numero, (numero, ""))
    ep_num = {"EP-0001": "0", "EP-0002": "1", "EP-0003": "2", "EP-0004": "3"}.get(numero, "?")

    L = []
    add = L.append

    add(f"# EPISÓDIO {ep_num} — {ep['titulo'].upper()}")
    add("")
    add(f"**Passagem:** {ep['passagem']}  ")
    add(f"**Livro:** {ep['livro']} · **Temporada:** {ep['temporada']}  ")
    add(f"**Estrutura:** {len(ep['frames'])} frames × 5 segundos = {len(ep['frames']) * 5} segundos  ")
    add(f"**Narração:** {ep['narrador']['personagem'] if isinstance(ep.get('narrador'), dict) else 'DEUS'}  ")
    add("")
    add("## COMO USAR ESTA FOLHA")
    add("")
    add("1. Copie o **PROMPT DE IMAGEM** e gere o quadro na sua IA de imagem (Midjourney, Flux, SDXL…).")
    add("2. Pegue a imagem gerada e suba no **Seedance 1.5 Pro** (modo imagem-para-vídeo).")
    add("3. Cole o **PROMPT DE VÍDEO** do mesmo frame — ele já traz a fala, o som e a câmera.")
    add("4. Gere **5 segundos** com **áudio ligado**. A voz sai junto com o vídeo.")
    add("5. Repita para os 12 frames e emende na edição — **sem legendas e sem texto na tela**: "
        "a imagem e a voz contam a história sozinhas.")
    add("")
    add("**Ajustes recomendados no Seedance 1.5 Pro:** duração `5` (inteiro, de 4 a 12) · proporção `16:9` "
        "**(sempre horizontal — não gerar vertical)** · resolução `720p` para teste e `1080p` para o final · "
        "`generate_audio` **LIGADO** · `camera_fixed` desligado.")
    add("")
    add("> Se a voz sair abafada pela música, gere com a música em volume mínimo — a trilha completa "
        "entra depois, na edição, por baixo da voz.")
    add("")
    add("---")
    add("")

    for idx, fr in enumerate(ep["frames"], start=1):
        i = fr.get("frame", idx)
        t_ini = (i - 1) * 5
        t_fim = i * 5
        fala = fr.get("narracao") or (fr.get("falas", {}) or {}).get("narrador_deus_pt", "")
        texto_biblico = fr.get("texto_passagem_pt") or (fr.get("falas", {}) or {}).get("texto_da_passagem_pt", "")
        referencia = fr.get("referencia") or fr.get("referencia_biblica") or ep.get("passagem", "")
        add(f"## ▸ FRAME {i} — {fr['titulo']}  ({t_ini:02d}s → {t_fim:02d}s)")
        add("")
        if referencia:
            add(f"*Referência: {referencia}*")
            add("")
        add("🎙️ **FALA DA VOZ DE DEUS (PT-BR)**")
        add("")
        add(f"> {fala}")
        if texto_biblico:
            add("")
            add(f"> *Versículo de referência (só para conferência — NÃO exibir na tela):* {texto_biblico}")
        add("")
        add("🖼️ **1) PROMPT DE IMAGEM** — cole na IA de imagem:")
        add("")
        add("```text")
        add(montar_prompt_imagem(fr))
        add("```")
        add("")
        add("*Parâmetros (Midjourney/SDXL):* `--ar 16:9 --style raw --stylize 250 --chaos 0` "
            "(sempre horizontal)")
        add("")
        add("**Evitar (negative prompt):**")
        add("")
        add("```text")
        add(fr.get("imagem_negativo_en", NEGATIVO_IMAGEM))
        add("```")
        add("")
        add("🎬 **2) PROMPT DE VÍDEO — Seedance 1.5 Pro** (suba a imagem gerada e cole isto):")
        add("")
        add("```text")
        add(montar_prompt_video(fr))
        add("```")
        add("")
        cfg = "`5 s` · `16:9` horizontal · `720p` teste / `1080p` final · `generate_audio: ON` · `camera_fixed: OFF`"
        add(f"⚙️ **Ajustes:** {cfg}")
        add("")
        if fr.get("nota_producao"):
            add(f"📌 **NOTA DE PRODUÇÃO:** {fr['nota_producao']}")
            add("")
        add(f"🎞️ **Continuidade:** {fr.get('continuidade','')}")
        add("")
        add("---")
        add("")

    return ep, apelido, tema, "\n".join(L)


def versao_txt(markdown: str) -> str:
    """Versão limpa, sem marcação markdown, para copiar e colar."""
    linhas = []
    for linha in markdown.split("\n"):
        l = linha
        l = re.sub(r"^#+\s*", "", l)
        l = re.sub(r"^\*\*\s*", "", l)
        l = l.replace("**", "").replace("*", "")
        l = re.sub(r"^>\s*", "    ", l)
        l = l.replace("```text", "").replace("```", "")
        l = l.replace("`", "")
        l = l.replace("▸ ", "").replace("🖼️ ", ">> ").replace("🎬 ", ">> ").replace("🎙️ ", ">> ")
        linhas.append(l)
    return "\n".join(linhas)


def gerar(numeros: list):
    os.makedirs(SAIDA, exist_ok=True)
    todos = []
    for numero in numeros:
        caminho = os.path.join(CURADORIA, f"{numero}.json")
        if not os.path.exists(caminho):
            print(f"!! curadoria não encontrada: {caminho}")
            continue
        ep, apelido, tema, markdown = folha_do_episodio(caminho)
        base = f"{apelido}-{tema}-prompts"
        with open(os.path.join(SAIDA, base + ".md"), "w", encoding="utf-8") as fh:
            fh.write(markdown)
        with open(os.path.join(SAIDA, base + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(versao_txt(markdown))
        todos.append(markdown)
        print(f"✔ {base}.md  ({len(ep['frames'])} frames)")

    if len(todos) > 1:
        juncao = ("# BÍBLIA COMPLETA — FOLHAS DE PROMPT (PREPARADAS PARA SEEDANCE 1.5 PRO)\n\n"
                  "Cada frame traz: a fala da voz de Deus, o prompt de imagem e o prompt de vídeo "
                  "de 5 segundos com áudio.\n\n---\n\n") + "\n---\n\n".join(todos)
        with open(os.path.join(SAIDA, "TODOS-OS-EPISODIOS.md"), "w", encoding="utf-8") as fh:
            fh.write(juncao)
        print("✔ TODOS-OS-EPISODIOS.md")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    if not args:
        numeros = sorted(a[:-5] for a in os.listdir(CURADORIA) if a.endswith(".json"))
    else:
        numeros = args
    gerar(numeros)
