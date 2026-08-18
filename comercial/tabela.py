# -*- coding: utf-8 -*-
"""Tabela de precos do Santa Informa. Fonte unica: o PDF comercial, a pagina
Anuncie e os espacos do site saem todos daqui, para nunca divergirem.

Duas regras que valem para tudo neste arquivo:
  1. Nenhum valor abaixo de PISO.
  2. Todo valor e multiplo de 250, para qualquer soma fechar redondo.
O teste no fim do arquivo cobra as duas."""

PISO = 1000   # nenhuma opcao custa menos que isto por mes
PASSO = 250   # todo valor e multiplo disto

# a partir de quanto por mes o cliente ganha a materia mensal
MATERIA_A_PARTIR = 2500

# (id, nome, onde, largura, altura, largura movel, altura movel, mensal)
ESPACOS = [
 ('sb-home',  'Super Banner',        'Topo da página inicial, antes da manchete do dia', 970, 250, 320, 100, 3750),
 ('bb-home',  'Billboard',           'Meio da página inicial, onde o leitor já parou de rolar', 970, 250, 320, 100, 2500),
 ('bb-regiao','Billboard Raio-X',    'Página de dados da região, onde corretor e construtora procuram número', 970, 250, 320, 100, 2500),
 ('bn-mat',   'Banner de matéria',   'Meio do texto de todas as matérias, e nas páginas de arquivo', 728,  90, 320, 100, 2000),
 ('rt-mat',   'Retângulo de matéria','Fim do texto, depois dos colunistas. Pega quem leu até o fim', 300, 250, 300, 250, 1500),
 ('rt-home',  'Retângulo',           'Página inicial, ao lado do Resumo Semanal', 300, 250, 300, 250, 1250),
 ('bn-edit',  'Banner de editoria',  'Na editoria do seu assunto, à sua escolha entre as seis', 970, 250, 320, 100, 1250),
 ('bn-arq',   'Banner do arquivo',   'Todas as páginas de Todas as notícias',    728,  90, 320, 100, 1000),
 ('rodape',   'Selo de apoio',       'Seu nome no rodapé de todas as páginas do site', 300,  90, 300,  90, 1000),
]

# patrocinios de secao: a marca aparece junto do conteudo, sem banner
PATROCINIOS = [
 ('pat-editoria','Editoria inteira','Seu nome na editoria, no menu e no banner dela, e mais ninguém ali dentro', 4500),
 ('pat-semanal', 'Resumo Semanal',  'Sua marca assina o bloco que reúne a semana de Itapema', 3000),
 ('pat-horo',    'Horóscopo e Tarô','Sua marca na página que o leitor volta para ver toda semana', 1250),
]

# conteudo escrito pela redacao
EDITORIAIS = [
 ('pub-1', 'Publieditorial', '1 publicação',  'até 3.400 caracteres, com foto e link permanente', 1250),
 ('pub-3', 'Publieditorial', '3 publicações', 'mesmo formato, ao longo do mês, para contar em partes', 3000),
 ('pub-5', 'Publieditorial', '5 publicações', 'mesmo formato, uma por semana', 4500),
]

# cotas fechadas, mais caras
COTAS = [
 ('take-home',  'Página inicial fechada',
  'Super Banner, Billboard, Retângulo da home e Billboard do Raio-X, mais um publieditorial. Nenhum outro anunciante na home', 8500),
 ('cota-master','Cota Master',
  'A página inicial fechada, mais banner e retângulo em todas as matérias, o Resumo Semanal assinado e dois publieditoriais', 14500),
 ('cota-verao', 'Cota Verão',
  'A Cota Master de dezembro a março, os quatro meses da temporada fechados de uma vez', 55000),
]

def tudo():
    d = {}
    for e in ESPACOS:      d[e[0]] = (e[1], e[7])
    for p in PATROCINIOS:  d[p[0]] = (p[1], p[3])
    for x in EDITORIAIS:   d[x[0]] = (f'{x[1]} {x[2]}', x[4])
    for c in COTAS:        d[c[0]] = (c[1], c[3])
    return d

def diario(mensal):
    return round(mensal / 30, 2)

def brl(v):
    return f'R$ {v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def confere():
    """Cobra o piso e o multiplo. Roda sozinho ao importar."""
    erros = []
    for nome, valor in tudo().values():
        # a Cota Verao e de quatro meses, entao o piso vale no valor mensal
        mensal = valor / 4 if nome == 'Cota Verão' else valor
        if mensal < PISO:
            erros.append(f'{nome}: {brl(mensal)} por mês, abaixo do piso de {brl(PISO)}')
        if valor % PASSO:
            erros.append(f'{nome}: {brl(valor)} não é múltiplo de {brl(PASSO)}')
    if erros:
        raise SystemExit('tabela.py: ' + '; '.join(erros))
    return True

confere()
