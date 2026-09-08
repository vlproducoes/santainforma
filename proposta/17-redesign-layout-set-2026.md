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

## O que o editor decidiu

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
2. O botão de modo escuro. Hoje quem manda é o sistema. Um botão pediria
   marcação nova nas 185 páginas e um lugar para guardar a escolha; vale se o
   editor quiser.
3. A tagline do logo, dentro do SVG, tem 9,5px. É desenho de marca, não texto
   de leitura, mas é o único ponto do site abaixo do piso de 12px.
