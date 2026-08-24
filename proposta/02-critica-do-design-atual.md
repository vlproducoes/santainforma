CRÍTICA DE DESIGN EDITORIAL · SANTA INFORMA (estado atual: index.html, estilo.css v1.0, visual.js v1.2, materia-01 como modelo canônico)

---

## 1. O QUE É FORTE E PRECISA SER PRESERVADO

**A paleta é uma identidade de verdade, não um tema.** `--breu #0A1F28` como escuro de marca (em vez de preto puro), `--sol #FFB627` como único acento quente, `--coral #D1331F` restrito ao chapéu de editoria (`.ed`), `--areia` como cor de borda estrutural da `.grade`. Nenhum portal regional catarinense tem isso; a maioria é azul genérico com vermelho de urgência. Qualquer redesign que troque essa paleta destrói o único ativo visual consolidado.

**A marca SVG inline é conceito, não logotipo decorativo.** O sol nascendo sobre linhas que simulam texto impresso (grupo `.sun` no header, com as três `rect` em `#8FB0B9` de opacidade decrescente) diz "notícia + litoral" em 45px. A animação de entrada escalonada (`@keyframes nascer` e `aparecer`, delays .45s/.8s em `.wordmark`/`.tagline`) é microdetalhe de veículo grande, e o fallback em `prefers-reduced-motion` (linhas 494-501 do estilo.css) repõe a opacidade corretamente. Preservar a marca, a animação e a disciplina do fallback.

**A onda divisória (`.onda` + `.escuro+.onda`)** é assinatura territorial barata: um path, cor herdada da seção. É o tipo de detalhe que Zeit Online faria. Está subusada, não errada.

**O sprite de ícones próprio** (símbolos `#i-onda` a `#i-pessoas`, traço 1.7, `stroke-linecap:round`, tudo `currentColor` via `.icone`) é consistente e proprietário. Melhor que qualquer icon font. Preservar e expandir no mesmo traço.

**O par tipográfico é escolha editorial real.** Archivo 800 com tracking negativo no display + Newsreader com eixo óptico (`opsz 6..72`) no corpo. Newsreader variável é sofisticação que quase ninguém no Brasil regional usa.

**O baixo nível do front é mais moderno que o visual.** Barra de progresso com `animation-timeline:scroll()` protegida por `@supports` (`.progresso`), `@view-transition{navigation:auto}` com header/rodapé nomeados, `speculationrules` para prerender, `text-wrap:balance/pretty`, `aspect-ratio` reservando o espaço de anúncio contra CLS, `width/height` em toda `<img>`. Isso é engenharia de 2026 servindo um layout de 2016. O redesign deve construir EM CIMA dessas APIs, não substituí-las.

**Acessibilidade acima da média e não negociável:** carrossel com pausa (WCAG 2.2.2, quatro mecanismos no visual.js), alvos de 24px nos pontos (`.carrossel-pontos button`), link único por card com área esticada por `::after` e foco no contêiner via `:has()` (`article.card:has(h3 a:focus-visible)`), `.so-leitor` com `clip-path`, tabela de preços com primeira coluna sticky no celular. Nada disso pode regredir.

---

## 2. O QUE ESTÁ DATADO, GENÉRICO OU FRACO

**A home não hierarquiza. Esse é o defeito número um.** `index.html` abre com um carrossel de 6 slides de peso idêntico (`.carrossel-trilho` com `grid-auto-columns:calc(50% - 11px)`), seguido de uma `.grade` de 9 cards idênticos. Não existe manchete. Um portal precisa dizer "isto é o mais importante hoje" e o Santa Informa diz "aqui estão 6 coisas iguais, 5 delas escondidas atrás de um botão". Carrossel como abertura de capa é padrão 2012-2016; NYT, Folha e Zeit abrem com pacote de capa: uma manchete dominante, duas ou três secundárias, coluna de últimas. O carrossel ainda joga fora a fotografia: `.slide img` com `opacity:.5` sobre `--breu` mais gradiente transforma toda foto em textura escura ilegível.

**A `.grade` é um feed uniforme, sem ritmo.** `repeat(3,1fr)`, todos os cards com a mesma capa 16/9, mesmo chapéu de 10px, mesmo corpo `.96rem`. Não há card-destaque de 2 colunas, não há card só-texto intencional, não há variação de escala. Pior: os dois cards "Manifesto" no fim (linhas 170-181 do index.html) têm exatamente o mesmo peso visual de notícia, confundindo institucional com jornalismo.

**A distância hierárquica entre níveis é quase nula.** Título de seção (`.titulo h2`, 1.32rem uppercase) contra título de card (`article.card h3`, 1.18rem): 0.14rem de diferença. O olho não encontra a escada. E não existe escala fluida: fora o `clamp()` do `.hero h1`, tudo é tamanho fixo.

**Placeholders de anúncio no primeiro scroll matam a percepção de veículo estabelecido.** O `.anuncio.a-super` ("Espaço disponível, 970×250") aparece logo abaixo do carrossel da home, moldura tracejada `#9F8A6A` sobre branco. É honesto, mas visualmente é um buraco que grita "site novo sem anunciante". O mesmo na matéria (`.a-faixa` e `.a-ret` no fim da materia-01).

**Estilos inline denunciam sistema incompleto.** `style="color:inherit;text-decoration:none"` repetido em cada link de card, `style="padding-bottom:56px"` na section Ferramentas, `style="margin-top:30px"` na `.fonte`, `style="max-width:44ch"` no footer, `style="width:20px;height:20px"` nos ícones dos botões do carrossel. Essas decisões deviam ser classes; hoje são remendos.

**Truncamento manual com "…" gravado no HTML** (cards m46, m45, m44: "quando as propostas…"). Frágil e feio; `-webkit-line-clamp` resolve sem tocar no conteúdo.

**O produto principal tem o tratamento visual mais pobre.** O Modo de Leitura é o diferencial editorial do portal e, na matéria canônica, é: um painel cinza no hero (`.painel`, `rgba(255,255,255,.05)` com border-left) e três caixas brancas idênticas empilhadas no rodapé (`.leitura-v`), sem os chips de alternância que o CSS até prevê (`.chips`/`.chip` existem no estilo.css e não são usados na materia-01). As cinco versões prometidas não têm interface. E Clara, Seu Prudêncio e Caco, que são as três marcas editoriais da casa, não têm identidade visual nenhuma: mesma caixa, mesma borda amarela, nenhum avatar, nenhuma cor de voz.

**Ritmo vertical dessincronizado.** `main{padding:52px 0}`, `.escuro{padding:50px 0;margin:52px 0}`, section com `padding-bottom:56px` inline, `.anuncio{margin:38px auto}`. Valores vizinhos mas aleatórios; não há escala de espaçamento.

**A seção `.semana` (Resumo Semanal)** é sidebar de 2014: duas colunas de itens com miniatura 60px. Os números `01-07` em `--sol` são o único charme. **A seção `.dados` (Ferramentas do litoral)** está em nível de wireframe: quatro caixas brancas, ícone de 20px, e o rótulo genérico "Abrir página" repetido quatro vezes.

**Crédito de foto em 10px uppercase** (`figure.foto .credito`) beira o ilegível no celular, que é o aparelho do leitor típico.

**Não existe modo escuro.** Cores todas fixas, nenhum `prefers-color-scheme` no estilo.css inteiro. Leitor de notícia noturno em celular é o caso de uso central do público.

**Distribuição visual furada: não há `og:image` nem no index.html nem na materia-01** (a imagem só existe no JSON-LD). No litoral, a matéria circula por WhatsApp; hoje ela circula sem cartão. É o defeito de design de maior impacto real do site.

---

## 3. ONDE O SITE NÃO PARECE "DE 2026" (e o que cabe na stack)

**Zero visualização de dados num veículo que se vende por número.** A seção "Os números que importam" da materia-01 é uma `<ul>` de bullets. Zeit e The Pudding transformariam em stat tiles (Archivo 800 gigante, o número como elemento gráfico), sparklines SVG desenhadas à mão, e um mapa: uma matéria sobre 4,75 km de orla sem um mapa SVG do trecho é a maior oportunidade perdida do site. Tudo isso é SVG inline vanilla, dentro da Constituição, custo de bytes quase nulo.

**Sem scrollytelling.** A matéria é texto corrido uniforme. O padrão Pudding/NYT (mapa ou diagrama fixo que evolui conforme o leitor rola) hoje se faz com `animation-timeline:view()` em CSS puro, e o site JÁ usa `scroll()` na barra de progresso e JÁ tem IntersectionObserver no visual.js. A técnica está na casa; falta ambição de uso.

**View transitions paradas no básico.** Header e footer nomeados, mas falta o efeito que essa API dá de graça: `view-transition-name` único na capa de cada card, para a imagem do card voar para a foto de abertura da matéria. É a transição "de app" que o NYT tem, sem uma linha de framework.

**Tipografia sem coragem.** O `.hero h1` para em 3.7rem. Veículos de 2026 usam o display como elemento gráfico (Zeit, NYT Magazine): título em 6-8rem em desktop para matérias especiais, entrelinha apertada, o amarelo `--sol` como grifo tipográfico. Archivo 800 aguenta isso; o CSS atual não pede.

**Microinteração de 2018.** Hover de card é `background:#fff` e `filter:saturate(1.1)`. O timing function `linear()` (CSS nativo, 2024+) dá molas e bounces sem GSAP; `interpolate-size`/`transition-behavior` dão transições de altura para os painéis do Modo de Leitura sem JS.

**As cenas `.anima` são o embrião certo e estão escondidas.** Parallax de camadas SVG com `transform/opacity`, pausável, com reduced-motion. Isso é a resposta vanilla honesta a "quero WebGL": está pronta, aparece só nas matérias 04 e 05, e nunca na capa.

**Sobre a lista de desejos do usuário, com franqueza:**
- **Three.js, R3F, GSAP, Framer Motion, Lenis: não entram.** A Constituição proíbe dependência, e num portal que vive de Core Web Vitals em celular intermediário, 150-600 KB de biblioteca é receita a menos. Lenis em particular (sequestro do scroll) é anti-padrão para leitura de notícia.
- **WebGL/WebGPU vanilla: cabe no máximo como vinheta única e opt-in** (ex.: ondas procedurais num canvas 2D/WebGL leve no topo da capa, escrito à mão, pausável, desligado em `prefers-reduced-motion` e em `saveData`). Nunca como moldura de conteúdo.
- **WebAssembly/Rust: não há workload que justifique.** Não existe processamento pesado no cliente aqui.
- **Os equivalentes nativos que entregam a mesma sensação de "site caro":** scroll-driven animations (`scroll()`/`view()`), View Transitions por elemento, `linear()` easing, `@property` para animar variáveis, SVG autoral animado por transform/opacity (técnica já dominada no `.anima`), `light-dark()` para o modo escuro. O site já demonstra maturidade exatamente nessas APIs; o redesign de 2026 é usá-las no palco, não nos bastidores.

**Síntese para o redesign:** manter paleta, marca, onda, sprite, tipografia e todo o chassi de acessibilidade/performance; demolir a capa (carrossel fora, pacote hierarquizado dentro), criar escada tipográfica fluida com coragem no display, dar interface e identidade visual às cinco vozes do Modo de Leitura (cor e avatar SVG por colunista), instituir um sistema de números/mapas em SVG autoral como assinatura da casa, promover as cenas `.anima` à capa, adicionar modo escuro e `og:image`, e eliminar os estilos inline transformando cada remendo em componente do sistema.