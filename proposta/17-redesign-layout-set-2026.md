# Redesign de layout · setembro de 2026

Registro do redesign aprovado pelo editor em 06 de setembro de 2026, publicado em
`main` pelo pull request 3 e no ar em santainforma.com.br.
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
  `ferramentas/contraste.py` (tabela no estudo de cores). Os tons e parte
  das matizes mudaram na revisão registrada mais abaixo; vale a lista de lá.
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

## Revisão da cor, no mesmo dia

Com o redesign no ar, o editor pediu para rever a questão das cores. A conta
mostrou onde estava o problema: os doze tons de texto do leque iam de 6,5:1 a
10,5:1 sobre branco. Passavam no AA com folga demais e, em caixa alta de 12px,
liam como preto. O site tinha paleta, mas não tinha cor. A superfície também
era mínima: fora o chapéu de 12px, quase nada no layout carregava a editoria.

O que mudou:

- **Faixa de trabalho.** Cada editoria passou a ter um tom só, resolvido para
  o ponto mais claro que ainda passa 4,6:1 sobre branco, sobre o fundo, sobre
  a espuma e sobre o próprio tint. Deu de 4,60:1 a 4,79:1 no pior caso e
  cerca de 5,1:1 sobre branco. O `-texto` deixou de ser um tom separado e
  virou apelido do tom vivo.
- **Matizes redistribuídas.** Com tons mais vivos, três azuis quase iguais
  ficaram impossíveis de separar. Poder Público foi para 222°, Esporte para
  199°, e Cidade saiu do azul da casa.
- **Serviço ganhou cor própria.** É o maior grupo do site (87 chamadas, 12%)
  e vestia o azul da marca, a mesma cor do cabeçalho, dos links e do rodapé:
  sumia. Recebeu o violeta quaresmeira (264°), a única faixa vazia do
  círculo. Cidade virou apelido de Serviço, porque é a mesma pauta.
- **Mais superfície.** Fio de 3px na cor da editoria no topo de cada card,
  ponto colorido em todo chapéu (antes só no da matéria), ícones da barra de
  editorias sempre coloridos, fio à esquerda das chamadas da pilha, topo da
  página de editoria em tint, filete da manchete na cor da editoria, rótulo
  do Resumo Semanal na cor da editoria e box "o que ainda está em aberto"
  seguindo a matéria.
- **Modo escuro.** Saiu da fase 2 e entrou. Segue a preferência do sistema,
  sem botão. Cada editoria troca o tom vivo pelo `-claro`, que já existia e já
  estava medido sobre breu. As únicas regras de componente são inversões:
  peça escura sobre claro que precisa virar clara sobre escuro.
- **Duas pendências fechadas.** Os textos do aviso de cookie ganharam acento,
  e a foto de topo da matéria passou a receber o mesmo `capa-mNN` da chamada,
  então a imagem viaja de uma página à outra em vez de sumir e voltar.

Validação da revisão: `checa-site.py` em zero; auditoria em 14 páginas por 5
larguras, nos dois modos (140 telas), com zero overflow horizontal, zero alvo
de toque abaixo do mínimo e zero par texto/fundo abaixo de AA. Os três links
de fonte que ficavam abaixo do alvo mínimo no `regiao.html` foram corrigidos
de passagem. O CSS foi de 23,6 kB para 25,7 kB comprimido.

## A marca sai do azul esverdeado, 08/09

O editor foi direto: o azul esverdeado e o amarelo davam ao site a cara de
material gerado por IA. É uma queixa justa. Aquele par turquesa mais âmbar é o
padrão de saída de meio mundo de tema automático, e o problema não parava no
acento: o leque inteiro de neutros tinha fundo ciano (espuma, fios, cinza de
legenda, cinza do modo escuro), que é de onde vem metade da impressão.

Montei três saídas e mostrei as três renderizadas na capa de verdade, não em
amostra de cor: grafite e osso, azul-tinta e osso, sépia e areia. O editor
escolheu **grafite e osso** e mandou deixar o leque de editorias como estava.

O que mudou:

- **Marca.** `--breu` virou `#15171A`, um cinza neutro quase preto. Entraram
  `--grafite` (`#262A2E`, a faixa de marca e o link), `--osso` (`#D9D2C4`, o
  acento, que era o amarelo), `--pedra` e `--papel`. O coral escureceu um
  grau, para `#C8341F`, e virou o único tom forte da marca.
- **Apelidos.** `--mar`, `--sol`, `--mar-claro` e `--espuma` continuam de pé
  apontando para os nomes novos. Não é preguiça: 143 páginas trazem
  `style="color:var(--mar)"` cravado no HTML e não vão ser reescritas.
- **Neutros.** Fundo, fios, tinta secundária e a camada inteira do modo escuro
  perderam o ciano. É a mudança que mais pesa e a menos visível de descrever.
- **Logo sem tocar em HTML.** O SVG do cabeçalho traz os hex antigos como
  atributo de apresentação, que perde para qualquer regra de CSS. Sete linhas
  no bloco 4 repintam sol, linhas d'água, marca e tagline. Página que o ciclo
  de notícias gerar amanhã copiando o cabeçalho antigo já nasce certa.
- **A marca ganhou estrutura de volta.** Antes era claro mais amarelo. Agora
  SANTA recua em cinza e INFORMA avança em branco, então o peso fica na metade
  que diz o que o jornal faz.
- **Link.** Sem cor própria: é a tinta com sublinhado fino, e o hover engrossa
  em coral. Osso sobre branco some, então não servia.
- **Céu.** Ficou monocromático, como o editor sabia ao escolher. Para não virar
  borrão cinza, a linha d'água puxa para a areia: vira a luz do horizonte.
  Amanhecer e entardecer seguem quentes, em coral e osso.
- **Colunistas.** O Seu Prudêncio usava o azul da casa, que era justamente o
  tom em questão. Passou para a ardósia do leque editorial, que combina com o
  criterioso. A régua da Clara era o amarelo e virou o ouro de Economia.

Ficou de fora, por decisão do editor: o turquesa do Turismo e o ouro da
Economia. Ali a cor tem função, identifica editoria, aparece em pedaço pequeno
e nunca como fundo de página. O único ajuste foi o tom claro de Economia, que
apontava para o amarelo da marca e agora tem hex próprio (`#D29810`).

Validação: `checa-site.py` em zero, `contraste.py` em zero, auditoria em 14
páginas por 5 larguras nos dois modos, com zero overflow, zero alvo de toque
pequeno e zero par abaixo de AA.

## Site todo claro, topo no jeito Apple, 09/09

Quatro pedidos do editor de uma vez: tirar as ondas, refazer o topo inspirado
no menu do site da Apple, deixar o site todo claro, e o logo com o sol e o mar
nas cores do desenho e as letras em azul marinho.

- **Ondas.** A faixa `.horizonte` da capa, com as duas ondas derivando, o botão
  de pausa e o selo de simulação, saiu. O HTML das páginas não foi tocado, então
  o CSS esconde a faixa. As ondas das páginas internas e do rodapé já estavam
  desligadas desde o redesign.
- **Topo.** Barra branca e translúcida com blur por trás, tipo em peso 400,
  hairline de 1px embaixo e nada mais. Sem faixa colorida, sem gradiente, sem
  sombra. O logo encolheu de 179 para 164px. Depois de rolar sobra só a barra
  de editorias, com 44px, que é a altura da barra da Apple. Ajustei o padding
  da nav para manter o alvo de toque em 44px: a primeira versão tinha caído
  para 31px e a auditoria pegou.
- **Tudo claro.** O Resumo Semanal e a leitura do horóscopo, os dois únicos
  blocos escuros, viraram faixas em `--superficie-2`. Chip pressionado, signo
  escolhido e botão de aceitar cookie viraram azul marinho com texto branco. O
  modo escuro automático saiu inteiro: um site que vira escuro sozinho na
  preferência do sistema não é um site todo claro. Os tons `-claro` do leque
  ficaram no CSS, medidos, caso o modo escuro volte um dia.
- **Céu.** Saiu junto. Com a faixa de marca branca não há onde pintar céu, e
  com ele foram as classes `ceu-*`, o véu de chumbo do clima e o sol que virava
  lua. O `visual.js` continua escrevendo essas classes e chamando o `/clima`,
  sem efeito nenhum: mexer nisso é decisão do editor, porque envolve
  `functions/`, que o ciclo de notícias não pode tocar.
- **Logo.** O sol voltou a ser sol (`--sol-logo`) e o mar voltou a ser mar
  (`--mar-logo`). As duas variáveis não aparecem em mais nenhum lugar do site:
  o desenho guarda as cores literais, o resto do site não. As letras foram para
  o azul marinho, que virou a cor da marca em tudo: link, foco, item ativo da
  nav, régua de bloco, número do Resumo Semanal. A tagline de 9,5px ficou no
  cinza, que é o que passa no contraste naquele corpo.

O grafite de 08/09 continua no CSS como cinza de apoio. O osso saiu: só servia
sobre fundo escuro, e fundo escuro não existe mais.

O favicon veio atrás, no mesmo dia. Era um quadrado escuro com o sol amarelo
antigo, sobra da faixa de marca que não existe mais. Virou fundo branco, sol em
`--sol-logo` e mar em `--mar-logo`, a mesma geometria do desenho do cabeçalho.
O `ferramentas/icone.py` desenha em 16 vezes o tamanho final e reduz, para o
sol e os dois fios do mar saírem limpos em 16px; ele reescreve o `favicon.ico`
(16, 32, 48 e 64), o `apple-touch-icon.png` e os dois PNG de uma vez. O
`favicon.svg` continua escrito à mão, com a mesma geometria.

Depois o editor pediu redondo. O quadrado virou disco: a mesma cena recortada
num círculo, com um fio de mar em volta e transparência fora dele. O fio não é
enfeite: sem ele o disco branco some em aba clara e o ícone volta a parecer
quadrado. A linha d'água, que ia de ponta a ponta, virou uma corda do círculo,
e a cena ficou parecendo uma escotilha, o que cai bem para jornal de litoral.
O `apple-touch-icon.png` ficou de fora e segue quadrado: o iOS aplica a própria
máscara e transforma área transparente em preto, então PNG redondo lá volta com
quatro cantos pretos.

Validação: `checa-site.py` e `contraste.py` em zero, auditoria em 14 páginas por
5 larguras com zero overflow, zero alvo de toque pequeno e zero par abaixo de
AA. Nenhum HTML mudou.

## Miniatura na pilha e a marca na base do nome, 09/09

Dois ajustes pedidos olhando a capa no ar.

- **Miniatura na coluna da direita.** As três chamadas da seção "Itapema e
  Costa Esmeralda" eram só texto e ganharam a miniatura quadrada da matéria à
  direita, no mesmo desenho do rio de últimas: 96px no desktop, 88px no
  celular. Foi preciso mexer no `index.html`, a primeira vez neste trabalho
  todo: as chamadas não tinham `<img>` nenhuma. O `prompt-agente-noticias.md`
  passou a mandar o ciclo de notícias levar a miniatura junto quando a pilha
  gira, senão a coluna voltaria a ficar só-texto na próxima rotação. No CSS o
  `:has(.pilha-mini)` devolve a coluna única quando a imagem não existe, então
  chamada sem foto não abre buraco.
- **A linha d'água na base do nome.** No SVG do logo a linha do mar nasce em
  y=23 e a base de SANTA INFORMA está em y=26: a marca boiava três unidades
  acima do nome. Um `translateY(3px)` no grupo do sol resolve, por CSS, sem
  tocar no SVG das 198 páginas.
- **A tagline justificada na largura do nome.** LITORAL DE SANTA CATARINA
  parava bem antes do A de INFORMA. O jeito certo no SVG seria `textLength`,
  que é atributo e não dá para escrever por CSS, e mexer nisso pediria editar
  o cabeçalho das 198 páginas. Então a justificação saiu pelo `letter-spacing`,
  que é a mesma coisa para uma linha só de caixa alta espaçada: 3,066 em vez
  do 2,5 que vem no SVG. O valor foi medido no navegador, com
  `getExtentOfChar` do último glifo de cada um dos dois textos, até as bordas
  direitas baterem. Está em unidade do viewBox, então escala junto e fecha
  igual no celular.

## O que o editor decidiu

-1. Site todo claro, topo no jeito Apple, sem ondas, logo com sol e mar nas
   cores do desenho e letras em azul marinho, em 09/09.
0. Marca em grafite e osso, em 08/09. Fora o azul esverdeado e o amarelo.
1. Paleta editorial aprovada. As doze cores entraram no `estilo.css` (bloco 1) e a regra do
   CLAUDE.md foi reescrita: a seção 9 agora lista as variáveis de marca, a camada semântica e
   a família `--ed-*`, e diz que cor fora dessas variáveis só entra com aprovação. A seção 9.5
   virou "O layout (redesign aprovado em 06/09/2026)".
2. Merge aprovado pelo editor e feito na hora. Publicado e conferido: `estilo.css` e
   `visual.js` em produção batem byte a byte com o `main` (o `index.html` difere só pela
   ofuscação de e-mail que o Cloudflare aplica sozinho, comportamento que já existia).

## O que ficou para depois

1. O rio de últimas continua sem cor. As chamadas de lá não têm chapéu na
   marcação, então não há de onde ler a editoria sem mexer no HTML das
   páginas. Se um dia o gerador puser o chapéu no rio, a cor entra sozinha.
2. O modo escuro saiu em 09/09. Se voltar, o leque editorial já tem os tons
   `-claro` medidos e o que falta é a camada semântica.
3. A tagline do logo, dentro do SVG, tem 9,5px. É desenho de marca, não texto
   de leitura, mas é o único ponto do site abaixo do piso de 12px.
