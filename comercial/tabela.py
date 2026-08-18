# -*- coding: utf-8 -*-
"""Tabela de precos do Santa Informa. Fonte unica: o PDF comercial, a pagina
Anuncie e os espacos do site saem todos daqui, para nunca divergirem."""

ALVO = 6250  # o valor que precisa ser alcancavel por varios caminhos

# (id, nome, onde, largura, altura, largura movel, altura movel, mensal)
ESPACOS = [
 ('sb-home',  'Super Banner',        'Topo da página inicial, abaixo do menu', 970, 250, 320, 100, 3750),
 ('bb-home',  'Billboard',           'Meio da página inicial, entre os blocos', 970, 250, 320, 100, 2500),
 ('rt-home',  'Retângulo',           'Página inicial, ao lado do Resumo Semanal', 300, 250, 300, 250, 1250),
 ('bn-mat',   'Banner de matéria',   'Meio do texto, em todas as matérias',      728,  90, 320, 100, 2000),
 ('rt-mat',   'Retângulo de matéria','Fim do texto, em todas as matérias',       300, 250, 300, 250, 1500),
 ('bn-edit',  'Banner de editoria',  'Uma das seis editorias, à sua escolha',    970, 250, 320, 100, 1250),
 ('bn-arq',   'Banner do arquivo',   'Todas as páginas de Todas as notícias',    728,  90, 320, 100,  750),
 ('bb-regiao','Billboard Raio-X',    'Página Raio-X da Região, público qualificado', 970, 250, 320, 100, 2500),
 ('rodape',   'Selo de apoio',       'Rodapé de todas as páginas do site',       300,  90, 300,  90,  500),
]

# patrocinios de secao: a marca aparece junto do conteudo, sem banner
PATROCINIOS = [
 ('pat-semanal', 'Resumo Semanal', 'Marca única na seção mais lida da home, com assinatura no bloco', 3000),
 ('pat-horo',    'Horóscopo & Tarô','Marca única na página de horóscopo, atualizada toda semana',    1250),
 ('pat-editoria','Editoria inteira','Seu nome na editoria, no menu e no banner dela, com exclusividade', 4500),
]

# conteudo
EDITORIAIS = [
 ('pub-1', 'Publieditorial',        '1 publicação', 'até 3.400 caracteres, com foto e link permanente',  750),
 ('pub-3', 'Publieditorial',        '3 publicações','mesmo formato, publicadas ao longo do mês',       2000),
 ('pub-5', 'Publieditorial',        '5 publicações','mesmo formato, uma por semana',                   3000),
]

# cotas fechadas, mais caras
COTAS = [
 ('take-home', 'Take-over da Home', 'Todos os espaços da página inicial, com exclusividade no dia',  8500),
 ('cota-master','Cota Master',      'Todos os espaços do site, mais Resumo Semanal e 2 publieditoriais por mês', 14500),
 ('cota-verao','Cota Verão',        'Cota Master de dezembro a março, com 4 meses fechados',        52000),
]

# combinacoes que fecham exatamente no alvo
PACOTES = [
 ('Vitrine',  ['sb-home','bb-home'],
  'Domina a home inteira, de cima a baixo.'),
 ('Bairro',   ['bn-edit','bn-edit','bn-edit','bn-edit','bn-edit'],
  'As seis editorias menos uma, à sua escolha. Presença em todo o noticiário temático.'),
 ('Leitura',  ['bn-mat','rt-mat','rt-home','pub-1','bn-arq'],
  'Aparece no meio e no fim de toda matéria, mais uma publieditorial.'),
 ('Semana',   ['pat-semanal','bn-mat','bn-edit'],
  'Assina o Resumo Semanal e aparece dentro de todas as matérias.'),
 ('Região',   ['bb-regiao','bb-home','rt-home'],
  'Foco em quem pesquisa dado da região: corretor, construtora e investidor.'),
 ('Conteúdo', ['pub-5','rt-mat','rt-home','rodape'],
  'Cinco publieditoriais no mês, mais presença fixa em matéria e rodapé.'),
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
