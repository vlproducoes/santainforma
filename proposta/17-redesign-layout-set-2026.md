# Redesign de layout · setembro de 2026

Registro do redesign entregue na branch `claude/santa-informa-layout-redesign-s1rsqt`.
Pedido do editor: refazer todo o layout, sem cara de "feito por IA", inspirado na Apple
e no G1, responsivo e validado no celular, multicolorido a partir de estudo de cores.
Restrição: só layout. Nenhum HTML, conteúdo, configuração, `functions/` ou ferramenta
mudou. O que mudou: `estilo.css` (reescrito) e `visual.js` (um bloco novo no fim).

## Como foi feito

Uma equipe de agentes produziu três direções de arte (Tela Apple, Portal G1 com
acabamento Apple, Litoral Cromático) e quatro pareceres (cores, tipografia e grid,
mobile, crítica anti-cara-de-IA). Três juízes com lentes diferentes (editor de jornal,
designer de produto, líder de produto mobile) pontuaram: a direção "Portal G1 com
acabamento Apple" venceu por unanimidade (93, contra 84 e 72), com enxertos das outras
duas. O blueprint final e o CSS seguem esse veredito.

## Decisões de layout

- **Anatomia de jornal.** Faixa de marca em `--mar` (na capa, o céu da hora), barra de
  editorias branca e translúcida de 44px que gruda no topo, manchete de até 54px, rio de
  últimas com hora tabular e fio coral, cards brancos com fio de 1px, régua dupla nos
  títulos de seção, hairlines, números tabulares.
- **Acabamento Apple.** Ar entre blocos (escala fluida de espaço), Archivo 800 com tracking
  negativo, raio máximo de 12px (8px em miniatura, pílula só em botão e chip), sombra só
  no hover, navegação em caixa normal, folha branca, rodapé claro.
- **Cor por editoria.** Doze cores-mãe com nome e origem (Azul Fórum, Ouro Velho, Laranja
  Obra, Vinho Serra, Turquesa, Verde Mata, Mar, Grafite, Rosa Primavera, Azul Céu, Ardósia,
  Coral), cada uma com tom principal, tom de texto (AA sobre branco), tom claro (AA sobre
  breu) e tint de fundo. A cor identifica editoria: chapéu, item ativo da barra, topo da
  página de editoria, barra de leitura da matéria, painel de 30 segundos, régua dos
  colunistas. Nunca em título de chamada, corpo ou fundo de seção. Contraste medido em
  `design/contraste.py` do estudo (tabela no estudo de cores).
- **Hook único de JS.** O `visual.js` lê o texto do chapéu ("Cidade · Assunto") e escreve
  `data-editoria` no chapéu e no bloco que o contém. Sem JS, tudo cai na tinta escura.
  Páginas de editoria e a barra usam `a[href="editoria-x.html"]` e `body:has()`, sem JS.
- **Mobile.** Cabeçalho de 52 + 40 + 44px (só a barra de editorias gruda), listas com
  miniatura de 88px à direita, foto da manchete sangrando até a borda, tabela de preços em
  fichas até 980px, cookie como folha inferior, alvos de 44px, texto mínimo de 12px, sem
  overflow horizontal em 360px.
- **O que saiu.** Ondas nas páginas internas, hero escuro da matéria, chapéu em etiqueta
  amarela, ícone antes de título de texto, cartões com ícone das Ferramentas e do 404,
  hover em foto, filtro dessaturando foto, sombra em repouso, cascata de animações do rio,
  parallax das capas, gradiente do Resumo Semanal.
- **O que ficou.** Sol que vira lua à noite, céu por hora na faixa de marca da capa, véu do
  clima, ondas do horizonte (24px, só desktop, pausáveis), barra de leitura, transição entre
  páginas, mola de toque, consentimento de cookie, cenas animadas das matérias.

## Validação

`python3 ferramentas/checa-site.py` em zero. Auditoria automática em 14 páginas × 5
larguras (360, 390, 768, 1024, 1440): zero overflow horizontal, zero alvo de toque abaixo
do mínimo, zero par texto/fundo abaixo de AA. Testes de interação: folha de cookie no
celular, barra grudada depois de rolar, horóscopo (signo e chips), foco por teclado,
`prefers-reduced-motion` (nada some), estados `ceu-noite` e `tempo-chuva`.

## Pendências para o editor

1. Aprovar a paleta editorial: o CLAUDE.md (seções 9 e 9.5) diz "nenhum hex novo"; esta
   branch propõe doze cores novas, documentadas acima e no bloco 1 do `estilo.css`. Se
   aprovada, a regra do CLAUDE.md precisa ser atualizada pelo editor.
2. Modo escuro: proposto no estudo de cores, fica para a fase 2.
3. Os textos do aviso de cookie no `visual.js` seguem sem acento (vêm de antes); é conteúdo,
   não foi tocado.
