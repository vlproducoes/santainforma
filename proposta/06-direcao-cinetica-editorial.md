## nome
Cinética Editorial

## conceito
O movimento é hierarquia editorial: cada animação existe para dizer ao leitor o que ler primeiro, de onde a informação veio e para onde ela vai. A rolagem nativa é a linha do tempo da edição, e a coreografia inteira se pendura nela com CSS scroll-driven animations, nunca com sequestro de scroll. A página funciona completa sem nenhum efeito (HTML primeiro, movimento como camada), e cada técnica declara seu fallback no próprio código, como o site já faz hoje com a barra de progresso. Nada de biblioteca: o equivalente honesto de GSAP e Framer Motion aqui são view transitions nativas, WAAPI e um integrador de mola de ~60 linhas dentro do visual.js. A regra sóbria que segura tudo: corpo de texto nunca se move; quem dança são molduras, chapéus, números e capas.

## home
Seção por seção, sobre o index.html atual, sem mudar a estrutura do HTML além de atributos data-*:

1. CABEÇALHO. O nascer do sol do logo permanece (keyframes nascer/aparecer já existem em estilo.css). Novidade: a barra .editorias vira sticky no topo. Ao rolar, ela ganha elevação (sombra e fundo levemente mais denso) dirigida por animation-timeline: scroll(root), animation-range 0 120px. Sem suporte, fica sticky sem sombra, zero JS.

2. CAPA (carrossel de destaques). O primeiro slide recebe data-cine="palavras": o título entra palavra a palavra (detalhe no campo hero). O chapéu amarelo .ed entra como carimbo, translateX(-10px) para 0 com leve overshoot, 60ms depois do início do título. A imagem do slide NÃO anima nunca: ela é o LCP e precisa pintar imediatamente com fetchpriority="high", como já está. Autoplay, pausa e pontos permanecem exatamente como no visual.js atual (WCAG 2.2.2 já resolvido, não se toca).

3. SUPER BANNER. Intocado. O aspect-ratio reservado é a defesa de CLS e continua.

4. GRADE ITAPEMA E COSTA ESMERALDA. Três movimentos por card, todos transform/opacity: (a) entrada por rolagem, translateY(16px) mais opacity, via animation-timeline: view() com animation-range entry 0% / cover 30%, e onde não houver suporte o sistema .rv/.vis do visual.js assume (detecção por CSS.supports para nunca rodarem os dois juntos); (b) parallax leve na capa: o img.capa passa a viver numa moldura overflow:hidden, com height 112% e translateY indo de -6% a 0 conforme o card atravessa a viewport, timeline view(), só compositor; (c) o chapéu .ed desliza -8px com 60ms de atraso sobre a entrada do card. Pressionar o card dispara mola de escala 0.985 e solta (JS, campo motion).

5. ONDA DE TRANSIÇÃO (.onda). Ganha uma segunda path defasada e deriva horizontal de ±40px amarrada ao scroll da seção (view() na divisória), dando profundidade de maré ao custo de um transform.

6. RESUMO SEMANAL (bloco .escuro). Os itens entram em cascata com o stagger de irmãos que o visual.js já calcula (índice x 70ms), mantido como está. O .num amarelo entra 80ms antes do título do próprio item, um tique de máquina de compor. Nada de contador aqui, 01 a 07 são rótulos, não dados.

7. FERRAMENTAS DO LITORAL. Quando o card .d ganha .vis, o ícone SVG de traço desenha a si mesmo: stroke-dasharray/dashoffset animado em 420ms. Decorativo, barato, e como os ícones já são stroke no sprite, não exige redesenho.

8. RODAPÉ. Estático e congelado nas view transitions (view-transition-name: rodape já existe). Porto seguro visual: cabeçalho e rodapé nunca se mexem entre páginas, só o miolo viaja.

## materia
Sobre o modelo canônico materia-01-alargamento-meia-praia.html:

1. CHEGADA. Se o leitor veio de um card da home, a capa voou até a figura de topo via view transition (detalhe no campo tecnicas). O cabeçalho e a barra de progresso não piscam, já têm view-transition-name próprio. O resto do miolo entra num fade curto de 180ms (::view-transition-new(root)).

2. HERO ESCURO. O chapéu (Itapema · Obras) carimba: scale .92 para 1 com -2deg para 0, overshoot pequeno via keyframe, 240ms. O h1 recebe data-cine="palavras" e compõe palavra a palavra. A linha fina aparece 80ms após a última palavra, num fade simples. O painel de 30 segundos sobe 12px com opacity, 420ms, fechando a sequência de abertura em menos de 1,2s no total.

3. MODO DE LEITURA. Os chips ganham a mola de pressão (escala 0.96 no pointerdown, solta com spring). A troca de versão usa document.startViewTransition quando existir: crossfade de 240ms com subida de 8px do painel novo. Sem a API, cai na classe .trocando que já faz o mesmo gesto em CSS. Leitor de tela não percebe diferença nenhuma entre os dois caminhos.

4. ENTENDA O ASSUNTO. Parágrafos não animam. Texto corrido é zona morta de movimento por decisão de direção: notícia se lê parada.

5. BOX "O QUE AINDA ESTÁ EM ABERTO" (.destaque). A borda esquerda amarela cresce, scaleY 0 para 1 com transform-origin no topo, dirigida por view(). O texto dentro já está visível antes do traço terminar.

6. OS NÚMEROS QUE IMPORTAM. Cada <strong> numérico ganha data-conta="60" (e data-prefixo="R$ " quando houver): ao ficar 60% visível, o JS conta de zero ao valor em 900ms com easeOutExpo, usando font-variant-numeric: tabular-nums e min-width em ch para o layout não respirar. O número verdadeiro permanece escrito no HTML: sem JS, sem observer ou com reduced motion, ele simplesmente está lá.

7. OUTROS JEITOS DE LER. As três .leitura-v entram em cascata de 70ms pela mesma trilha dos cards. Nomes dos colunistas (.autor) deslizam -8px como os chapéus.

8. LEIA TAMBÉM E PUBLICIDADE. Cards do "Leia também" usam o mesmo sistema da home, incluindo a capacidade de lançar o voo de capa para a próxima matéria. Blocos .pub-google e .anuncio ficam fora de qualquer coreografia: iframe de anúncio repinta por conta própria e não pode participar de transição.

## tipografia_cor
TIPOGRAFIA. Troca do pedido ao Google Fonts: em vez de três pesos estáticos de Archivo, a versão variável (eixos wght 100-900 e wdth 62.5-125), um arquivo só, payload igual ou menor. A largura vira voz editorial dentro da mesma família: manchetes em wdth 104 (presença de capa impressa), chapéus e rótulos em wdth 88 (carimbo condensado), números de destaque em wght 800 com tabular-nums. Newsreader segue como está, o eixo opsz já vem no pedido atual. Movimento sobre tipo é raríssimo e cirúrgico: só a manchete da capa, só em pointer:fine, hover leva wght de 800 a 860 em 200ms via font-variation-settings. Honestidade técnica: animar eixo variável repinta glifo a glifo, então isso jamais entra em scroll ou em elemento repetido.

COR. Paleta intocada, nenhum valor novo. O que muda é a introdução de meia dúzia de tokens semânticos em cima dela (--fundo, --tinta, --superficie, --realce, --tinta-suave), definidos no :root com os valores claros de hoje e redefinidos num único bloco @media (prefers-color-scheme: dark). O modo escuro automático é o bloco .escuro promovido a página inteira, com receita que o site já validou: fundo --breu, texto --espuma, corpo em #E3EDEF (valor que já existe no .painel), superfície de card rgba(255,255,255,.05), realce e links no --sol. Ajuste obrigatório: o coral #D1331F sobre breu rende ~3,2:1 e falha em caps de 10px, então no escuro o chapéu coral remapeia para --sol via token, sem criar cor. Fotos não são escurecidas à força; figuras ganham um fio rgba(255,255,255,.12) para assentar no fundo. A onda divisória inverte os fills pelos mesmos tokens.

## motion
Sistema com tokens declarados no topo do estilo.css: --t-micro 120ms (pressão, hover), --t-ui 240ms (chips, troca de painel), --t-entrada 560ms (revelações por rolagem), --t-voo 480ms (view transition da capa). Uma única curva mestre, batizada de "maré": cubic-bezier(.2,.7,.3,1), que já é a curva usada hoje no logo e no reveal, agora oficializada como identidade.

O QUE ANIMA, QUANDO, COM QUÊ:
1. Entradas por rolagem: cards, figuras, box destaque, leituras. Técnica primária CSS animation-timeline: view() com animation-range, dentro de @supports. Fallback: o IntersectionObserver do visual.js atual, que passa a rodar apenas quando CSS.supports('animation-timeline: view()') é falso, um contrato só de classes (.rv/.vis) para os dois caminhos.
2. Parallax leve: só nas capas de card, translateY -6% a 0 dentro de moldura overflow:hidden, timeline view(), 100% compositor. Sem suporte: imagem parada, nada quebra.
3. Chapéus que deslizam: translateX(-8px) mais opacity, 60ms após a entrada do bloco pai, mesma timeline.
4. Números que contam: JS com rAF e easeOutExpo, 900ms, disparado por observer a 60% de visibilidade, valor real sempre no HTML, largura reservada em ch com tabular-nums.
5. Manchete palavra a palavra: JS divide o título em spans com --i, CSS anima translateY(.55em) e opacity com atraso calc(var(--i) * 40ms). Acessibilidade blindada: o texto integral vai para aria-label do heading e o contêiner de spans fica aria-hidden="true", padrão split-text seguro. Sem JS, o título simplesmente aparece inteiro.
6. Voo de capa entre páginas: MPA view transition (campo tecnicas), 480ms maré, miolo antigo some em 180ms.
7. Molas físicas: um único integrador em visual.js (~60 linhas): estado {pos, vel}, stiffness 210, damping 24, massa 1, integração semi-implícita por rAF, para quando |vel| e |delta| caem abaixo de 0.01. Um só loop global serve todos os elementos ativos (chips, botões de carrossel, cards pressionados), escrevendo apenas transform:scale. É o equivalente honesto do spring de Framer Motion e do GSAP elastic, sem os 60KB.
8. Ambiente: as cenas SVG .anima (corre/pulsa/sobe) e a barra de progresso continuam como estão, já são scroll-driven ou compositor-only.

DESLIGAMENTO. O kill switch global já existente (@media prefers-reduced-motion: *{animation:none!important;transition:none!important} mais a reposição de opacidade) cobre todos os novos keyframes por construção. O JS novo consulta matchMedia antes de dividir palavras, contar números ou iniciar molas, seguindo o padrão que o visual.js já pratica no carrossel. View transitions já estão desligadas para reduced motion no CSS atual.

## hero
A assinatura da home tem dois tempos e um nome: A CAPA AMANHECE, A CAPA VOA.

Tempo um, a abertura (0 a 1,3s). O HTML pinta completo de imediato: a foto do destaque principal é o LCP e aparece no primeiro frame, com fetchpriority="high", proibida de participar de qualquer fade (animar o LCP é maquiar a própria receita). Sobre essa base estável, a coreografia: em 0ms o sol do logotipo começa a nascer atrás das linhas de texto do símbolo (keyframe nascer, 1,3s, já existente); em 120ms o chapéu amarelo do primeiro slide carimba da esquerda com overshoot curto; em 180ms a manchete principal se compõe palavra a palavra, cada palavra subindo 0.55em com opacity, 40ms de intervalo entre elas, como linotipo assentando tipos: uma manchete de oito palavras fecha em ~700ms; em 450ms e 800ms wordmark e tagline acendem (existentes). Percepção final: o jornal do dia sendo montado diante do leitor, em menos de um segundo e meio, sem empurrar um pixel de layout (só transform e opacity, CLS zero).

Tempo dois, a partida. O leitor toca um card. No pointerdown o card cede 0.985 de escala pela mola; no click, o JS grava view-transition-name: capa na imagem daquele card específico (só um elemento pode ter o nome, por isso ele é atribuído no gesto, não no CSS) e deixa a navegação MPA seguir nativa. O navegador então executa a transição de documento cruzado: cabeçalho, barra de editorias e rodapé ficam cravados no lugar (nomes próprios já existentes), o miolo da home se dissolve em 180ms, e a capa do card voa e cresce até se tornar a figura de topo da matéria, 480ms na curva maré, com o speculationrules já presente pré-renderizando o destino no hover para o voo pousar numa página já pronta. O chapéu e o título da matéria recebem o leitor compondo-se palavra a palavra no hero escuro. Em Firefox, que ainda não tem transição entre documentos, o clique vira navegação normal e instantânea: a assinatura degrada para silêncio, nunca para erro.

## tecnicas
O QUE ENTRA, COM FALLBACK DECLARADO:
1. CSS scroll-driven animations (animation-timeline: scroll() e view(), animation-range): entradas, parallax, chapéus, elevação do sticky, borda do destaque. Suporte: Chromium 115+, Safari 26, Firefox chegando. Fallback: @supports guarda tudo; onde falta, o sistema IntersectionObserver do visual.js atual assume as entradas e o resto fica estático. O site já usa esse padrão na barra .progresso.
2. Cross-document View Transitions (@view-transition{navigation:auto}, já ativo no estilo.css, mais view-transition-name dinâmico na capa clicada): o voo de capa. Suporte: Chromium 126+, Safari 18.2+. Fallback: navegação normal, custo zero.
3. Same-document View Transition (document.startViewTransition): troca do Modo de Leitura. Fallback: a classe .trocando existente.
4. Speculation Rules (já no site, eagerness moderate): pré-renderiza o destino no hover e faz o voo de capa pousar em página pronta. Fallback: navegação comum.
5. Mola física vanilla em rAF (~60 linhas no visual.js): micro-interações de pressão. Fallback: as transitions CSS que já vestem os mesmos elementos.
6. Archivo variável (wght+wdth): hierarquia por largura e o único hover de eixo. Fallback: navegador sem variable font usa o peso estático mais próximo, nativamente.
7. @property para registrar --i e afins com tipagem. Fallback: valores estáticos, animação some.
8. SVG pesado: sprite existente, cenas .anima, onda de duas camadas, stroke-draw nos ícones. Universal, sem fallback necessário.

O QUE NÃO ENTRA, E O EQUIVALENTE HONESTO:
Three.js e React Three Fiber: exigem dependência, React e build, três proibições do projeto de uma vez; o papel de "cena viva" já é das ilustrações SVG .anima, que rodam em qualquer aparelho. WebGL/GLSL à mão: possível em vanilla, mas num portal lido em celular intermediário um canvas com shader cobra GPU, bateria e LCP para entregar decoração; a assinatura visual desta direção vem de view transitions e tipografia, que custam quase nada. WebGPU: mesma conta, com suporte ainda desigual. WebAssembly/Rust: não existe aqui problema computacional para acelerar; o gargalo de um site de notícia é layout e paint, e WASM não toca neles. GSAP: substituído pela dupla WAAPI/keyframes mais a mola de 60 linhas. Framer Motion: as layout animations que o justificariam são exatamente o que view transitions nativas fazem. Lenis e qualquer scroll suavizado: recusado por princípio, ver riscos e conceito; rolagem nativa preserva restauração de posição do histórico e do BFCache, busca na página, âncoras, momentum do iOS, leitores de tela e INP. Leitor de notícia escaneia a página; adicionar latência entre o dedo e o texto é regressão funcional vestida de sofisticação.

## riscos
PERFORMANCE. (1) LCP: a regra dura é nenhuma animação de opacidade sobre a imagem de destaque e nenhum JS de coreografia antes dela; o split de palavras roda em DOMContentLoaded e só em headings, mas ainda assim causa um reflow do heading, aceitável porque acontece antes da primeira rolagem e nunca no corpo. (2) View transitions tiram snapshot das duas páginas; em celular fraco, muitos elementos nomeados custam caro: teto de 5 nomes por página (cabecalho, editorias, rodape, progresso, capa) e voo de 480ms no máximo. Testar em aparelho classe Moto G, não no desktop do desenvolvedor. (3) Contadores mudam largura de texto: tabular-nums e min-width em ch são obrigatórios, senão o CLS que o site tanto protege volta pela porta dos fundos. (4) Hover de eixo variável repinta glifos: um elemento só, nunca em lista. (5) O loop de mola precisa dormir: um rAF global que se desregistra quando todas as molas assentam, senão vira dreno de bateria e piora INP.

ACESSIBILIDADE. (1) Split de manchete sem o par aria-label/aria-hidden faz leitor de tela soletrar palavra por palavra com pausas: o padrão descrito no motion é inegociável e precisa entrar no template de matéria para as gerações em lote não o perderem. (2) O kill switch global de reduced motion cobre CSS, mas os caminhos JS (contador, split, mola, startViewTransition) precisam cada um consultar matchMedia, como o carrossel já faz; um esquecimento aqui é regressão direta. (3) Foco de teclado durante view transition: garantir que o outline chegue vivo na página de destino (o snapshot congela o frame, mas o foco pós-navegação segue normal; testar com Tab real). (4) Nada do que existe de conquista atual (carrossel pausável, alvos de 24px, skip link) é tocado por esta direção, e qualquer PR que encoste nisso reprova.

MANUTENÇÃO. (1) Sem build, a coreografia só sobrevive se for contrato de atributos: data-cine="palavras", data-conta, e classes já existentes; matéria gerada em lote ganha o movimento herdando o template, sem uma linha de CSS nova por página. Documentar os tokens de tempo no topo do estilo.css como a folha já documenta suas decisões. (2) Dois sistemas de revelação coexistem (CSS view() e o IO do visual.js): o interruptor único por CSS.supports é o que impede animação dupla; esse if é o ponto mais frágil do projeto e merece comentário gordo. (3) A spec de scroll-driven animations já mudou sintaxe uma vez; manter tudo atrás de @supports transforma drift de navegador em degradação silenciosa em vez de página quebrada. (4) Iframes do AdSense ignoram a coreografia e repintam sozinhos: mantê-los fora de qualquer contêiner com timeline ou transition, com as alturas reservadas de hoje. (5) Modo escuro automático dobra a matriz de teste visual: cada componente novo passa a ser conferido nos dois temas, e o remapeamento do coral precisa constar do checklist de publicação.