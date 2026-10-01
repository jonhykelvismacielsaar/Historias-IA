#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_planejar_episodios.py — Divide os 66 livros (1.189 capítulos) em episódios.

Regra de ouro do projeto:
    1 episódio = 12 frames × 5 segundos = 60 segundos de vídeo.
Cada frame recebe 1 prompt de imagem + 1 prompt de vídeo (JSON).

A densidade de versículos por frame depende do gênero literário do trecho:
    narrativo      1,0 versículo  por frame  → 12 versículos por episódio
    profético      1,0 versículo  por frame  → 12
    apocalíptico   1,0 versículo  por frame  → 12
    legislativo    2,5 versículos por frame  → 30
    carta          1,2 versículos por frame  → 14
    poético        0,5 versículo  por frame  →  6 (cada versículo ganha 2 frames)
    lista/censo    4,0 versículos por frame  → 48

Saídas:
    roteiro/indice_episodios.json  — plano completo, episódio por episódio
    roteiro/plano_episodios.csv    — mesma coisa em planilha
    roteiro/INDICE-GERAL.md        — visão geral + resumo por livro
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
from collections import OrderedDict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_biblia import LIVROS, TORA

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(RAIZ, "dados", "processado", "versiculos")
SAIDA = os.path.join(RAIZ, "roteiro")

FRAMES_POR_EPISODIO = 12
SEGUNDOS_POR_FRAME = 5

# ---------------------------------------------------------------------------
# Gênero literário por livro (pode ser sobrescrito por capítulo)
# ---------------------------------------------------------------------------
GENERO_PADRAO = {
    "genesis": "narrativo", "exodo": "narrativo", "levitico": "legislativo",
    "numeros": "narrativo", "deuteronomio": "legislativo",
    "josue": "narrativo", "juizes": "narrativo", "rute": "narrativo",
    "1samuel": "narrativo", "2samuel": "narrativo", "1reis": "narrativo",
    "2reis": "narrativo", "1cronicas": "lista", "2cronicas": "narrativo",
    "esdras": "narrativo", "neemias": "narrativo", "ester": "narrativo",
    "jo": "poetico", "salmos": "poetico", "proverbios": "poetico",
    "eclesiastes": "poetico", "cantares": "poetico",
    "isaias": "profetico", "jeremias": "profetico", "lamentacoes": "poetico",
    "ezequiel": "profetico", "daniel": "profetico", "oseias": "profetico",
    "joel": "profetico", "amos": "profetico", "obadias": "profetico",
    "jonas": "narrativo", "miqueias": "profetico", "naum": "profetico",
    "habacuque": "profetico", "sofonias": "profetico", "ageu": "profetico",
    "zacarias": "profetico", "malaquias": "profetico",
    "mateus": "narrativo", "marcos": "narrativo", "lucas": "narrativo",
    "joao": "narrativo", "atos": "narrativo",
    "romanos": "carta", "1corintios": "carta", "2corintios": "carta",
    "galatas": "carta", "efesios": "carta", "filipenses": "carta",
    "colossenses": "carta", "1tessalonicenses": "carta", "2tessalonicenses": "carta",
    "1timoteo": "carta", "2timoteo": "carta", "tito": "carta", "filemom": "carta",
    "hebreus": "carta", "tiago": "carta", "1pedro": "carta", "2pedro": "carta",
    "1joao": "carta", "2joao": "carta", "3joao": "carta", "judas": "carta",
    "apocalipse": "apocaliptico",
}

DENSIDADE = {           # versículos cobertos por frame
    "narrativo": 1.0,
    "profetico": 1.0,
    "apocaliptico": 1.0,
    "legislativo": 2.5,
    "carta": 1.2,
    "poetico": 0.5,
    "lista": 4.0,
}

# Capítulos que fogem do gênero do livro (mistos)
EXCECOES_GENERO = {
    "genesis": {5: "lista", 10: "lista", 11: "lista", 25: "lista", 36: "lista", 46: "lista", 49: "poetico"},
    "exodo": {15: "poetico", 20: "legislativo", 21: "legislativo", 22: "legislativo", 23: "legislativo", 25: "legislativo", 26: "legislativo", 27: "legislativo", 28: "legislativo", 29: "legislativo", 30: "legislativo", 35: "legislativo", 36: "legislativo", 37: "legislativo", 38: "legislativo", 39: "legislativo", 40: "legislativo"},
    "numeros": {1: "lista", 2: "lista", 3: "lista", 4: "lista", 7: "lista", 26: "lista", 33: "lista", 34: "lista", 35: "lista"},
    "deuteronomio": {32: "poetico", 33: "poetico", 28: "legislativo"},
    "josue": {12: "lista", 13: "lista", 15: "lista", 16: "lista", 17: "lista", 18: "lista", 19: "lista", 21: "lista"},
    "2samuel": {22: "poetico", 23: "poetico"},
    "1cronicas": {1: "lista", 2: "lista", 3: "lista", 4: "lista", 5: "lista", 6: "lista", 7: "lista", 8: "lista", 9: "lista", 11: "lista", 12: "lista", 23: "lista", 24: "lista", 25: "lista", 26: "lista", 27: "lista"},
    "esdras": {2: "lista", 8: "lista", 10: "lista"},
    "neemias": {7: "lista", 10: "lista", 11: "lista", 12: "lista"},
    "daniel": {7: "apocaliptico", 8: "apocaliptico", 9: "apocaliptico", 10: "apocaliptico", 11: "apocaliptico", 12: "apocaliptico"},
    "jeremias": {52: "lista"},
    "mateus": {1: "lista"},
    "lucas": {3: "lista"},
    "apocalipse": {7: "apocaliptico"},
}

# ---------------------------------------------------------------------------
# Títulos curados — Torá completa (187 capítulos) + capítulos-chave de toda a Bíblia
# ---------------------------------------------------------------------------
TITULOS_TORA = {
"genesis": {
 1: "A Criação dos Céus e da Terra", 2: "O Jardim do Éden e a Costela", 3: "A Serpente, a Queda e a Promessa",
 4: "Caim, Abel e o Primeiro Sangue", 5: "As Gerações de Adão até Noé", 6: "A Corrupção da Terra e a Ordem da Arca",
 7: "O Dilúvio: as Águas Cobrem a Terra", 8: "As Águas Baixam e a Pomba Voltou", 9: "A Aliança do Arco-íris",
 10: "A Tábua das Nações", 11: "Babel e a Dispersão dos Povos", 12: "O Chamado de Abrão",
 13: "Abrão e Ló se Separam", 14: "Melquisedeque Abençoa Abrão", 15: "A Aliança: Conta as Estrelas",
 16: "Agar e Ismael", 17: "A Aliança Eterna e a Circuncisão", 18: "Os Três Visitantes e a Intercessão por Sodoma",
 19: "Sodoma e Gomorra", 20: "Abraão e Abimeleque", 21: "O Nascimento de Isaque",
 22: "A Ligadura de Isaque (Akedá)", 23: "A Morte de Sara e o Campo de Macpela", 24: "Rebeca: a Noiva para Isaque",
 25: "A Morte de Abraão; Jacó e Esaú Nascem", 26: "Isaque e os Poços em Gerar", 27: "A Bênção Roubada",
 28: "A Escada de Jacó em Betel", 29: "Jacó, Lia, Raquel e os Doze Filhos", 30: "Os Rebanhos e a Fuga de Labão",
 31: "Jacó Foge de Labão", 32: "Jacó Luta com o Anjo: Israel", 33: "O Reencontro com Esaú",
 34: "Diná e a Vingança dos Filhos de Jacó", 35: "O Retorno a Betel e a Morte de Raquel",
 36: "Os Descendentes de Esaú (Edom)", 37: "José e a Túnica de Muitas Cores", 38: "Judá e Tamar",
 39: "José na Casa de Potifar", 40: "Os Sonhos do Copeiro e do Padeiro", 41: "Os Sonhos do Faraó e a Ascensão de José",
 42: "Os Irmãos Vão ao Egito", 43: "A Segunda Viagem e o Banquete", 44: "A Taça de Prata de Benjamim",
 45: "Eu Sou José: O Perdão", 46: "Jacó Desce ao Egito", 47: "Israel Habita em Gósen",
 48: "As Bênçãos de Efraim e Manassés", 49: "As Bênçãos e Profecias dos Doze", 50: "A Morte de Jacó e Vós Me Vendestes",
},
"exodo": {
 1: "Israel Escravizado no Egito", 2: "O Nascimento e a Fuga de Moisés", 3: "A Sarça Ardente e o Nome YHWH",
 4: "Os Sinais e o Retorno ao Egito", 5: "Deixem Israel Ir: as Cargas Aumentam", 6: "Eu Sou o SENHOR: as Quatro Promessas",
 7: "A Primeira Praga: Água em Sangue", 8: "Rãs, Piolhos e Moscas", 9: "Úlceras, Granizo e a Morte do Gado",
 10: "Gafanhotos e Trevas", 11: "A Décima Praga Anunciada", 12: "A Páscoa e o Êxodo",
 13: "Sinais na Mão e no Tempo", 14: "A Travessia do Mar Vermelho", 15: "O Cântico do Mar e as Águas de Mara",
 16: "O Maná e as Codornas", 17: "Água da Rocha e a Guerra contra Amaleque", 18: "A Sabedoria de Jetro",
 19: "Monte Sinai: Fogo e Tempestade", 20: "Os Dez Mandamentos", 21: "Leis sobre Servos e Reparações",
 22: "Furto, Fogo e Empréstimo", 23: "Festas, Justiça e o Anjo Guardião", 24: "O Pacto Selado com Sangue",
 25: "A Arca, a Mesa e o Candelabro", 26: "O Tabernáculo: Cortinas e Estrutura", 27: "O Altar, o Átrio e o Azeite",
 28: "As Vestes Sacerdotais", 29: "A Consagração dos Sacerdotes", 30: "O Altar do Incenso e o Censo",
 31: "Bezalel e o Sábado", 32: "O Bezerro de Ouro", 33: "Tua Glória Me Mostra",
 34: "As Duas Tábuas Renovadas", 35: "O Chamado para Construir", 36: "O Trabalho do Santuário",
 37: "A Arca e os Móveis do Lugar Santo", 38: "O Altar, o Átrio e a Contagem do Ouro", 39: "As Vestes e a Obra Concluída",
 40: "A Glória Enche o Tabernáculo",
},
"levitico": {
 1: "Holocaustos e a Oferta Voluntária", 2: "Ofertas de Cereais", 3: "Ofertas de Paz", 4: "Ofertas pelo Pecado",
 5: "Ofertas de Culpa", 6: "As Leis do Fogo Perpétuo", 7: "A Porção dos Sacerdotes", 8: "A Consagração de Arão",
 9: "O Fogo que Desce", 10: "Nadabe, Abiú e o Silêncio de Arão", 11: "Animais Puros e Impuros",
 12: "Purificação após o Parto", 13: "Tsara'at: o Diagnóstico do Sacerdote", 14: "A Purificação do Leproso e das Casas",
 15: "Fluxos e Pureza", 16: "O Dia da Expiação (Yom Kippur)", 17: "O Sangue e a Vida",
 18: "Leis de Santidade e Moral Sexual", 19: "Sede Santos: Ame ao Teu Próximo", 20: "Santidade e os Ritos de Moloque",
 21: "Santidade dos Sacerdotes", 22: "Ofertas Aceitáveis ao SENHOR", 23: "As Festas do SENHOR",
 24: "O Azeite, os Pães e a Blasfêmia", 25: "O Ano Sabático e o Jubileu", 26: "Bênçãos e Maldições da Aliança",
 27: "Votos e Ofertas Consagradas",
},
"numeros": {
 1: "O Primeiro Censo de Israel", 2: "A Ordem do Acampamento", 3: "Os Levitas e a Guarda",
 4: "As Funções e o Censo dos Levitas", 5: "Purificação, Restituição e Ciúme", 6: "O Nazireu e a Bênção Sacerdotal",
 7: "As Ofertas dos Príncipes", 8: "O Candelabro e a Consagração dos Levitas", 9: "A Páscoa e a Nuvem Guia",
 10: "As Trombetas de Prata e a Partida", 11: "Fogo, Carne e o Desejo Ingato", 12: "Miriam e Arão contra Moisés",
 13: "Os Doze Espias e Dois Relatórios", 14: "A Revolta e os Quarenta Anos", 15: "Ofertas e o Sábado Violado",
 16: "Corá, Datã e Abirão", 17: "A Vara que Floresceu", 18: "Os Levitas e os Dízimos",
 19: "A Água da Purificação", 20: "A Água de Meribá e a Morte de Arão", 21: "A Serpente de Bronze e o Poço",
 22: "Balaão e o Anjo do SENHOR", 23: "Os Oráculos de Balaão", 24: "Quão Belas São as Tuas Tendas",
 25: "Baal-Peor e o Zelo de Fineias", 26: "O Segundo Censo", 27: "A Lei da Herança e o Sucessor Josué",
 28: "As Ofertas Diárias e das Festas", 29: "As Ofertas do Sétimo Mês", 30: "Votos e o Valor da Palavra",
 31: "A Vingança contra Midiã", 32: "As Duas Tribos Além do Jordão", 33: "As Quarenta Jornadas",
 34: "A Fronteira da Terra Prometida", 35: "Os Levitas e as Cidades de Refúgio", 36: "As Herdeiras e as Tribos",
},
"deuteronomio": {
 1: "Recordando a Jornada", 2: "A Travessia de Seir", 3: "Vitórias e a Oração de Moisés", 4: "Escuta, Ó Israel",
 5: "Os Dez Mandamentos Repetidos", 6: "Amarás o SENHOR: o Shemá", 7: "Povo Escolhido entre Todos os Povos",
 8: "Não Só de Pão Vive o Homem", 9: "O Bezerro e a Intercessão", 10: "As Novas Tábuas e o Coração Circuncidado",
 11: "Bênção e Maldição e a Chuva no Tempo", 12: "O Lugar que Deus Escolher", 13: "Falsos Profetas e a Prova",
 14: "Filhos, Alimentos e o Dízimo", 15: "O Ano da Remissão e os Servos", 16: "Juízes, Reis e Justiça",
 17: "Leis do Rei, dos Sacerdotes e dos Profetas", 18: "Os Levitas e o Profeta como Moisés",
 19: "Cidades de Refúgio e Limites", 20: "Leis da Guerra e o Medo", 21: "Casos de Justiça e o Filho Rebelde",
 22: "Leis de Pureza e o Casamento", 23: "Assembleia, Acampamento e Santidade", 24: "Divórcio, Noivado e o Salário",
 25: "Aços, Azorrague e o Casamento do Irmão", 26: "Primícias: Arameu Errante", 27: "As Pedras do Monte Ebal",
 28: "Bênçãos e Maldições da Aliança", 29: "A Aliança Renovada em Moabe", 30: "A Escolha da Vida",
 31: "Josué É Comissionado e o Cântico", 32: "O Cântico de Moisés: Ele É a Rocha", 33: "As Bênçãos Finais de Moisés",
 34: "A Morte de Moisés no Monte Nebo",
},
}

TITULOS_CHAVE = {
"salmos": {1: "Bem-aventurado o Varão", 8: "Que É o Homem?", 19: "Os Céus Proclamam", 22: "Deus Meu, Deus Meu",
           23: "O SENHOR É Meu Pastor", 27: "O SENHOR É Minha Luz", 34: "Bendirei o SENHOR em Todo Tempo",
           37: "Não Te Indignes por Causa dos Maus", 40: "Esperei com Paciência", 51: "Cria em Mim um Coração Puro",
           84: "Quão Amáveis São os Teus Tabernáculos", 90: "Senhor, Tu Tens Sido o Nosso Refúgio",
           91: "Aquele que Habita no Esconderijo", 100: "Servi ao SENHOR com Alegria", 103: "Bendize, Ó Minha Alma",
           110: "Disse o SENHOR ao Meu Senhor", 119: "Lâmpada para os Meus Pés", 121: "Elevo os Meus Olhos",
           137: "Junto aos Rios da Babilônia", 139: "Tu Me Sondas e Me Conheces", 145: "Grande É o SENHOR",
           150: "Todo Ser que Respira Louve ao SENHOR"},
"isaias": {1: "Visão de Isaías, Filho de Amós", 6: "O Trono, o Carvão e o Envio", 7: "A Immanuel: a Virgem Conceberá",
           9: "Um Menino Nos Nasceu", 11: "O Rebento de Jessé", 14: "A Queda do Diabo (Lúcifer)", 25: "Ele Destruirá a Morte",
           40: "Consolai o Meu Povo", 42: "Eis o Meu Servo", 45: "Sou o SENHOR, e Não Há Outro", 49: "Nas Minhas Mãos Te Gravei",
           52: "Eis o Meu Servo: Quão Formoso", 53: "O Servo Sofredor", 55: "Vinde às Águas Todas as Nações",
           58: "O Jejum que Eu Escolhi", 60: "Levanta-te e Resplandece", 61: "Boa Nova aos Pobres", 66: "Novos Céus e Nova Terra"},
"jeremias": {1: "Antes que Eu Te Formasse", 7: "O Templo do SENHOR", 18: "Na Casa do Oleiro", 23: "O Renovo Justo",
             29: "Planos de Paz e Não de Mal", 31: "A Nova Aliança", 33: "A Justiça que Brotará", 36: "O Rolo Queimado",
             39: "A Queda de Jerusalém", 52: "A Destruição do Templo"},
"ezequiel": {1: "A Visão do Carro de Deus (Merkabá)", 2: "Comer o Rolo", 3: "Atalaia de Israel",
             11: "O Coração de Pedra e o de Carne", 16: "A Infidelidade de Jerusalém", 24: "A Morte da Esposa",
             34: "Os Pastores de Israel", 36: "Água Limpa e o Coração Novo", 37: "Os Ossos Secos e os Dois Paus",
             38: "Gogue e Magogue", 47: "O Rio que Sai do Templo"},
"daniel": {1: "Provados com Legumes e Água", 2: "O Sonho da Estátua", 3: "A Fornalha Ardente", 4: "O Sonho da Grande Árvore",
           5: "Os Dedos na Parede", 6: "A Cova dos Leões", 7: "As Quatro Bestas e o Filho do Homem",
           9: "As Setenta Semanas", 12: "O Tempo do Fim"},
"mateus": {1: "A Genealogia e o Anjo a José", 2: "Os Magos e a Fuga para o Egito", 3: "O Batismo no Jordão",
           4: "A Tentação e o Início do Ministério", 5: "O Sermão do Monte: as Bem-aventuranças",
           6: "O Pai Nosso e o Dinheiro", 7: "Não Julgueis; a Casa na Rocha", 8: "Tempestade no Lago",
           9: "A Mulher com Hemorragia e o Cego", 10: "Os Doze Enviados", 11: "Vinde a Mim Todos",
           12: "O Senhor do Sábado", 13: "As Parábolas do Reino", 14: "A Multiplicação dos Pães e o Mar",
           15: "A Mulher Cananeia", 16: "Pedro Confessa: Tu És o Cristo", 17: "A Transfiguração",
           18: "Sessenta e Dez Vezes Sete", 19: "O Jovem Rico", 20: "Os Trabalhadores da Última Hora",
           21: "A Entrada Triunfal", 22: "O Banquete e o Tributo", 23: "Ai de Vós, Escribas",
           24: "O Sermão Profético", 25: "As Dez Virgens e os Talentos", 26: "Getsêmani e a Prisão",
           27: "A Cruz: Crucifica-O", 28: "A Ressurreição e a Grande Comissão"},
"marcos": {1: "O Início do Evangelho", 2: "O Paralítico Descido pelo Telhado", 4: "A Parábola do Semeador",
           5: "O Gadareno e a Mulher que Tocou", 6: "João Batista Decapitado", 8: "Quem Dizem os Homens que Eu Sou",
           9: "A Transfiguração e o Pai Descrente", 10: "Bartimeu", 11: "A Figueira e a Entrada em Jerusalém",
           15: "A Crucificação", 16: "A Ressurreição"},
"lucas": {1: "O Anúncio a Maria e o Magnificat", 2: "O Nascimento em Belém e os Pastores", 3: "O Batismo e a Genealogia",
          4: "Jesus na Sinagoga de Nazaré", 10: "O Bom Samaritano", 15: "O Filho Pródigo",
          16: "O Rico e Lázaro", 19: "Zaqueu e a Lágrima sobre a Cidade", 22: "A Última Ceia",
          23: "A Crucificação e o Ladrão", 24: "O Caminho de Emaús"},
"joao": {1: "No Princípio Era o Verbo", 2: "As Bodas de Caná e os Vendilhões", 3: "Nicodemos: Deus Amou o Mundo",
         4: "A Samaritana no Poço", 5: "O Paralítico de Betesda", 6: "Os Pães e o Pão da Vida", 7: "A Festa dos Tabernáculos",
         8: "Eu Sou a Luz do Mundo", 9: "O Cego de Nascença", 10: "Eu Sou o Bom Pastor", 11: "Lázaro, Vem Para Fora",
         12: "A Entrada Triunfal e o Grão de Trigo", 13: "O Lava-Pés", 14: "Não Se Turbe o Vosso Coração",
         15: "Eu Sou a Videira", 16: "O Espírito de Verdade", 17: "A Oração Sacerdotal", 18: "A Prisão no Getsêmani",
         19: "A Crucificação", 20: "O Sepulcro Vazio e Tomé", 21: "As Peixes e a Restauração de Pedro"},
"atos": {1: "A Ascensão e a Promessa", 2: "Pentecostes: Línguas de Fogo", 3: "O Coixo de Nascença",
          4: "Pedro e João Perante o Sinédrio", 5: "Ananias e Safira", 6: "Estêvão e os Sete", 7: "O Martírio de Estêvão",
          8: "Filipe e o Eunuco", 9: "A Conversão de Saulo no Caminho de Damasco", 10: "Cornélio: Pedro e o Lençol",
          12: "Herodes e a Libertação de Pedro", 13: "A Primeira Viagem Missionária", 15: "O Concílio de Jerusalém",
          16: "Filipe e o Carcereiro de Filipos", 17: "Atenas: o Deus Desconhecido", 19: "Éfeso: os Livros Queimados",
          20: "O Discurso aos Anciãos de Éfeso", 27: "A Tempestade e o Naufrágio", 28: "Roma: o Evangelho em Cadeias"},
"romanos": {1: "Não Me Envergonho do Evangelho", 3: "Todos Pecaram", 5: "A Paz com Deus", 6: "Batizados na Sua Morte",
            8: "Nenhuma Condenação: Filhos e Herdeiros", 9: "A Eleição de Israel", 11: "O Enxerto da Oliveira",
            12: "A Vida em Santidade", 13: "Autoridades e o Amor", 14: "Não Julgueis o Irmão"},
"1corintios": {13: "O Hino do Amor", 15: "A Ressurreição: o Último Inimigo"},
"2corintios": {4: "Vasos de Barro", 12: "A Graça Basta"},
"galatas": {3: "A Fé de Abraão", 5: "O Fruto do Espírito"},
"efesios": {6: "A Armadura de Deus"},
"filipenses": {2: "Seja a Atitude de Cristo", 4: "Tudo Posso Naquele que Me Fortalece"},
"hebreus": {11: "A Galeria da Fé", 12: "Corramos com Perseverança"},
"tiago": {1: "A Provação Produz Perseverança", 3: "A Língua e a Sabedoria"},
"1pedro": {1: "A Esperança Viva", 5: "Lançando Sobre Ele Toda Ansiedade"},
"1joao": {1: "Luz e Comunhão", 4: "Deus É Amor"},
"judas": {1: "Contendei Pela Fé"},
"apocalipse": {1: "A Visão de Patmos", 2: "Éfeso, Esmirna, Pérgamo e Tiatira", 3: "Sardes, Filadélfia e Laodiceia",
               4: "O Trono e os Vinte e Quatro Anciãos", 5: "O Livro e o Cordeiro", 6: "Os Quatro Cavaleiros",
               7: "A Grande Multidão", 8: "As Trombetas", 9: "Gafanhotos e o Abismo", 10: "O Livrinho Doce e Amargo",
               11: "As Duas Testemunhas", 12: "A Mulher, o Dragão e o Menino", 13: "A Besta e a Imagem",
               14: "O Cordeiro no Monte Sião", 15: "As Sete Taças", 16: "Armagedom", 17: "A Grande Babilônia",
               18: "Caiu Babilônia", 19: "As Bodas do Cordeiro", 20: "O Milênio e o Juízo Final",
               21: "Novo Céu e Nova Terra", 22: "O Rio da Vida e Vem, Senhor Jesus"},
"josue": {1: "Sê Forte e Corajoso", 2: "Raabe e os Espias", 6: "A Queda de Jericó", 10: "O Sol se Deteve",
          24: "Escolhei Hoje a Quem Sirvais"},
"juizes": {6: "Gideão e o Velocino", 7: "Os Trezentos de Gideão", 13: "O Nascimento de Sansão",
           16: "Sansão e Dalila"},
"rute": {1: "Noemi e Rute", 4: "Boaz Resgata Rute"},
"1samuel": {1: "O Nascimento de Samuel", 3: "Fala, SENHOR, o Teu Servo Ouve", 16: "Davi É Ungido", 17: "Davi e Golias"},
"2samuel": {7: "A Promessa a Davi", 11: "Davi e Bate-Seba", 12: "Natã e a Parábola da Ovelhinha"},
"1reis": {3: "O Pedido de Sabedoria", 10: "A Rainha de Sabá", 18: "Elias no Monte Carmelo", 19: "A Voz Mansa e Delicada"},
"2reis": {2: "Elias É Arrebatado", 5: "Naamã, o Leproso", 25: "A Queda de Jerusalém"},
"1cronicas": {21: "O Censo e a Praga", 29: "Davi e a Oferta para o Templo"},
"2cronicas": {7: "Se o Meu Povo se Humilhar", 20: "A Vitória de Josafá"},
"esdras": {1: "O Decreto de Ciro", 3: "Os Alicerces do Templo"},
"neemias": {1: "A Oração de Neemias", 4: "A Espada e a Colher de Pedreiro", 8: "A Leitura da Lei"},
"ester": {4: "Para Tal Tempo como Este", 9: "Purim"},
"jo": {1: "Satanás e o Cercado", 19: "Eu Sei que o Meu Redentor Vive", 38: "Onde Estavas Tu?", 42: "Depois de Ouvir-te"},
"proverbios": {1: "O Princípio da Sabedoria", 3: "Confia no SENHOR de Todo o Teu Coração", 8: "A Sabedoria Clama",
               31: "A Mulher Virtuosa"},
"eclesiastes": {1: "Vaidade de Vaidades", 3: "Tempo para Todas as Coisas", 12: "Lembra-te do Teu Criador"},
"cantares": {1: "O Beijo e a Vinha", 8: "As Muitas Águas"},
"lamentacoes": {1: "Como Está Desertora a Cidade", 3: "As Misericórdias se Renovam"},
"oseias": {1: "Gômer, o Amor e o Adultério", 11: "Como Te Deixarei, Efraim?", 14: "Cura e Amor Gratuito"},
"joel": {2: "Derramarei o Meu Espírito"},
"amos": {5: "Corra o Juízo como as Águas", 9: "A Cabana Caída de Davi"},
"obadias": {1: "O Juízo de Edom"},
"jonas": {1: "A Fuga para Társis", 2: "Do Ventre do Peixe", 3: "Nínive se Arrepende", 4: "A Aboboreira"},
"miqueias": {5: "De Belém Sairá o Governante", 6: "Que É o Que o SENHOR Pede?"},
"naum": {1: "O SENHOR Vingador"},
"habacuque": {3: "Ainda que a Figueira Não Floresça"},
"sofonias": {3: "O SENHOR se Regozija em Ti"},
"ageu": {2: "A Glória da Última Casa"},
"zacarias": {3: "As Vestes Sujas e as Limpas", 9: "Eis o Teu Rei, Manso", 12: "Eles Olharão Para Aquele que Traspassaram", 14: "O SENHOR Será Rei"},
"malaquias": {3: "O Mensageiro e o Sol da Justiça", 4: "Elias Antes do Grande Dia"},
"2corintios_extra": {},
"1tessalonicenses": {4: "A Vinda do Senhor", 5: "O Dia do SENHOR como Ladrão"},
"2tessalonicenses": {2: "O Homem da Iniquidade"},
"1timoteo": {3: "Os Bispos e Diáconos"},
"2timoteo": {3: "Toda a Escritura É Inspirada", 4: "Combati o Bom Combate"},
"tito": {2: "A Graça que Traz Salvação"},
"filemom": {1: "Onésimo, o Escravo Amado"},
"2pedro": {3: "O Dia do Senhor Vem como Ladrão"},
"2joao": {1: "Verdade e Amor"},
"3joao": {1: "Gaio, o Hospitaleiro"},
"eclesiastico": {},
}


def densidade_do_trecho(slug: str, capitulo: int) -> float:
    genero = EXCECOES_GENERO.get(slug, {}).get(capitulo) or GENERO_PADRAO.get(slug, "narrativo")
    return DENSIDADE[genero], genero


def titulo_do_capitulo(slug: str, capitulo: int, primeiro_versiculo: str) -> str:
    if slug in TITULOS_TORA and capitulo in TITULOS_TORA[slug]:
        return TITULOS_TORA[slug][capitulo]
    if slug in TITULOS_CHAVE and capitulo in TITULOS_CHAVE[slug]:
        return TITULOS_CHAVE[slug][capitulo]
    # fallback: usa o incipit real do versículo 1 (dá um título informativo e fiel)
    incipit = " ".join(primeiro_versiculo.split()[:9]).rstrip(",;:. ")
    if len(incipit) > 62:
        incipit = incipit[:59].rsplit(" ", 1)[0] + "…"
    return incipit or f"Capítulo {capitulo}"


def planejar():
    plano = []
    numero_global = 0
    resumo_livros = OrderedDict()
    detalhe_por_livro = {}

    # Episódio 0 — Prelúdio
    numero_global += 1
    preludio = dict(
        id=f"EP-{numero_global:04d}", temporada=0, temporada_nome="PRELÚDIO",
        slug="preludio", livro="Prelúdio", capitulo=None,
        faixa_versiculos=None, referencia="Prelúdio original (inspirado em Gênesis 1:1-2)",
        titulo="O Vazio, a Voz e o Primeiro Traço",
        genero="narrativo", frames=FRAMES_POR_EPISODIO, duracao_segundos=FRAMES_POR_EPISODIO * SEGUNDOS_POR_FRAME,
        status="roteiro_completo",
    )
    plano.append(preludio)

    temporadas = OrderedDict([
        ("Torá", 1), ("Históricos", 2), ("Sapienciais", 3), ("Profetas", 4),
        ("Evangelhos e Atos", 5), ("Cartas de Paulo", 6), ("Cartas Gerais", 7),
        ("Apocalipse", 8),
    ])
    nomes_temporada = {
        "Torá": "T1 — TORÁ (A Lei)",
        "Históricos": "T2 — HISTÓRICOS",
        "Sapienciais": "T3 — SAPIENCIAIS E POESIA",
        "Profetas": "T4 — PROFETAS",
        "Evangelhos e Atos": "T5 — EVANGELHOS E ATOS",
        "Cartas de Paulo": "T6 — CARTAS DE PAULO",
        "Cartas Gerais": "T7 — CARTAS GERAIS",
        "Apocalipse": "T8 — APOCALIPSE",
    }

    for livro in LIVROS:
        slug = livro["slug"]
        caminho = os.path.join(CORPUS, f"{slug}.json")
        if not os.path.exists(caminho):
            continue
        with open(caminho, encoding="utf-8") as fh:
            dados = json.load(fh)
        caps = dados["capitulos"]
        grupo = livro["grupo"]
        mapa_grupos = {
            "Profetas Maiores": "Profetas", "Profetas Menores": "Profetas",
            "Evangelhos": "Evangelhos e Atos", "História NT": "Evangelhos e Atos",
            "Cartas Gerais": "Cartas Gerais", "Apocalíptico": "Apocalipse",
        }
        chave_temporada = mapa_grupos.get(grupo, grupo)
        t = temporadas[chave_temporada]
        episodios_livro = 0
        versiculos_livro = 0

        for cap_str in sorted(caps, key=int):
            cap = int(cap_str)
            versos = caps[cap_str]
            nums = sorted(int(v) for v in versos)
            if not nums:
                continue
            densidade, genero = densidade_do_trecho(slug, cap)
            por_episodio = max(1, int(round(FRAMES_POR_EPISODIO * densidade)))
            blocos = [nums[i:i + por_episodio] for i in range(0, len(nums), por_episodio)]
            titulo_base = titulo_do_capitulo(slug, cap, versos[str(nums[0])].get("pt_aa", ""))
            for i, bloco in enumerate(blocos, start=1):
                numero_global += 1
                episodios_livro += 1
                versiculos_livro += len(bloco)
                titulo = titulo_base if len(blocos) == 1 else f"{titulo_base} ({i}/{len(blocos)})"
                plano.append(dict(
                    id=f"EP-{numero_global:04d}", temporada=t,
                    temporada_nome=nomes_temporada[chave_temporada],
                    slug=slug, livro=livro["nome_pt"], capitulo=cap,
                    faixa_versiculos=[bloco[0], bloco[-1]],
                    referencia=f"{livro['nome_pt']} {cap}:{bloco[0]}" + (f"-{bloco[-1]}" if bloco[-1] != bloco[0] else ""),
                    titulo=titulo, genero=genero, frames=FRAMES_POR_EPISODIO,
                    duracao_segundos=FRAMES_POR_EPISODIO * SEGUNDOS_POR_FRAME,
                    status="planejado",
                ))
        detalhe_por_livro[slug] = {
            "livro": livro["nome_pt"], "grupo": grupo, "temporada": t,
            "capitulos": len(caps), "episodios": episodios_livro, "versiculos": versiculos_livro,
        }
        resumo_livros[livro["nome_pt"]] = episodios_livro

    os.makedirs(SAIDA, exist_ok=True)
    total_frames = len(plano) * FRAMES_POR_EPISODIO
    total_seg = total_frames * SEGUNDOS_POR_FRAME
    indice = {
        "projeto": "Bíblia Completa — Roteiro Cinematográfico em Episódios",
        "regra": {
            "frames_por_episodio": FRAMES_POR_EPISODIO,
            "segundos_por_frame": SEGUNDOS_POR_FRAME,
            "duracao_episodio_segundos": FRAMES_POR_EPISODIO * SEGUNDOS_POR_FRAME,
            "formato": "16:9 (3840x2160) — sempre horizontal",
            "prompts_por_frame": ["imagem", "video"],
        },
        "totais": {
            "episodios": len(plano),
            "frames": total_frames,
            "duracao_segundos": total_seg,
            "duracao_horas": round(total_seg / 3600, 1),
            "duracao_dias": round(total_seg / 86400, 2),
            "imagens_a_gerar": total_frames,
            "clipes_de_video_a_gerar": total_frames,
        },
        "por_temporada": {},
        "por_livro": detalhe_por_livro,
        "episodios": plano,
    }
    for ep in plano:
        chave = ep["temporada_nome"]
        indice["por_temporada"].setdefault(chave, 0)
        indice["por_temporada"][chave] += 1

    with open(os.path.join(SAIDA, "indice_episodios.json"), "w", encoding="utf-8") as fh:
        json.dump(indice, fh, ensure_ascii=False, indent=1)

    with open(os.path.join(SAIDA, "plano_episodios.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["episodio", "temporada", "livro", "capitulo", "versiculo_inicial", "versiculo_final",
                    "referencia", "titulo", "genero", "frames", "duracao_s", "status"])
        for ep in plano:
            w.writerow([ep["id"], ep["temporada_nome"], ep["livro"], ep["capitulo"] or "",
                        (ep["faixa_versiculos"] or ["", ""])[0], (ep["faixa_versiculos"] or ["", ""])[1],
                        ep["referencia"], ep["titulo"], ep["genero"], ep["frames"],
                        ep["duracao_segundos"], ep["status"]])

    # ---- índice legível ----
    linhas = ["# Índice Geral do Roteiro — Bíblia Completa em Episódios", ""]
    linhas.append(f"- **Episódios:** {len(plano):,}".replace(",", "."))
    linhas.append(f"- **Frames (imagens a gerar):** {total_frames:,}".replace(",", "."))
    linhas.append(f"- **Duração total:** {total_seg/3600:.1f} horas ({total_seg/86400:.1f} dias de vídeo)".replace(".", ","))
    linhas.append(f"- **Regra:** 1 episódio = 12 frames × 5 s = 60 s")
    linhas.append("")
    linhas.append("## Episódios por temporada")
    linhas.append("")
    linhas.append("| Temporada | Episódios |")
    linhas.append("|---|---|")
    for nome, qtd in indice["por_temporada"].items():
        linhas.append(f"| {nome} | {qtd} |")
    linhas.append("")
    linhas.append("## Resumo por livro")
    linhas.append("")
    linhas.append("| # | Livro | Grupo | Capítulos | Episódios | Versículos |")
    linhas.append("|---|---|---|---|---|---|")
    for i, (slug, d) in enumerate(detalhe_por_livro.items(), start=1):
        linhas.append(f"| {i} | {d['livro']} | {d['grupo']} | {d['capitulos']} | {d['episodios']} | {d['versiculos']} |")
    linhas.append("")
    linhas.append("## Primeiros 40 episódios (amostra da numeração)")
    linhas.append("")
    linhas.append("| Episódio | Referência | Título | Gênero |")
    linhas.append("|---|---|---|---|")
    for ep in plano[:40]:
        linhas.append(f"| {ep['id']} | {ep['referencia']} | {ep['titulo']} | {ep['genero']} |")
    linhas.append("")
    linhas.append("O plano completo está em `roteiro/indice_episodios.json` e `roteiro/plano_episodios.csv`.")
    with open(os.path.join(SAIDA, "INDICE-GERAL.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(linhas))

    print(f"Episódios: {len(plano)} | Frames: {total_frames} | Duração: {total_seg/3600:.1f} h")
    for nome, qtd in indice["por_temporada"].items():
        print(f"  {nome}: {qtd}")
    return indice


if __name__ == "__main__":
    planejar()
