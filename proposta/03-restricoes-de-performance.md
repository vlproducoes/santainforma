# Caderno de restrições do redesign · Santa Informa

Base medida no repositório em 19/08/2026 (transferência estimada em gzip; o Cloudflare serve Brotli, que fica 10 a 15% menor):

| Ativo | Bruto | Comprimido |
|---|---|---|
| `estilo.css` | 33,1 KB | 9,2 KB |
| `visual.js` | 11,5 KB | 4,0 KB |
| `index.html` | 27,9 KB | 7,4 KB |
| `materia-01...html` | 21,7 KB | ~6 KB |
| Miniatura de card (720×405 JPEG) | 6 a 57 KB | idem |
| Foto de matéria (1600w) | até 528 KB | idem |
| Pasta `imagens/` inteira | 32 MB | — |

O site atual é leve. O redesign parte de uma posição rara: quase todo o orçamento ainda está disponível. O risco é gastá-lo em decoração.

---

## 1. Orçamento de performance

**Cenário de referência:** Android intermediário (classe Samsung A15/Moto G), 4G real (8 a 12 Mbps efetivos, RTT 100 a 170 ms), cache frio, Cloudflare edge no Brasil (TTFB ~200 a 350 ms). Meta: LCP p75 < 2,0 s, CLS < 0,05, INP < 200 ms.

**Aritmética do LCP.** Com TTFB de ~300 ms, sobra ~1,7 s para: baixar e parsear HTML, baixar CSS, layout, e baixar + decodificar a imagem LCP. A 10 Mbps, cada 100 KB custa ~80 ms de rede mais fila. A conclusão prática: o caminho crítico (HTML + CSS + fonte do título + imagem LCP) precisa caber em ~350 KB comprimidos, e **nenhum byte de terceiro pode estar nele**.

**Tetos por categoria (transferência comprimida):**

| Categoria | Teto | Hoje | Observação |
|---|---|---|---|
| HTML por página | 35 KB | 6 a 7,5 KB | inclui sprite SVG e JSON-LD inline |
| CSS total (arquivo único) | 25 KB | 9,2 KB | o redesign pode quase triplicar o CSS e continuar dentro |
| JS próprio total | 30 KB, tudo `defer` | 4 KB (mas síncrono, ver §4) | zero JS no caminho de render |
| Fontes | 110 KB no total, máx. 4 arquivos woff2 | ~90 a 120 KB via Google Fonts, 2 origens extras | auto-hospedar (ver §3.7) |
| Imagem LCP | 100 KB, `fetchpriority="high"`, nunca `lazy` | 37 a 57 KB (home) ✓ | matéria precisa do ajuste do §4.3 |
| Imagens acima da dobra, somadas | 200 KB | ok na home | |
| Página completa sem anúncios | 500 KB | ~350 KB | |
| DOM | ≤ 1.500 nós na home, ≤ 1.000 na matéria | dentro | |
| Long task própria | nenhuma > 50 ms | dentro | |

**O que os terceiros já custam (e o redesign não controla):**

- `gtag.js` (GA4): ~100 a 130 KB de transferência, ~350 KB descomprimido, 150 a 400 ms de main thread num aparelho intermediário.
- `adsbygoogle.js`: ~30 KB iniciais, que puxam mais módulos até ~200 a 300 KB somando os frames. Cada slot preenchido adiciona um iframe com criativo de 50 a 300 KB. Bloqueio de main thread típico do AdSense: 200 a 600 ms, espalhado.
- Total realista de terceiros numa matéria com 2 slots preenchidos: **400 a 800 KB e 0,5 a 1,0 s de CPU**. Isso é 3 a 5 vezes todo o código próprio do site.

Consequência: o AdSense e o GA4 **são** o orçamento de JS do site. Já estão `async` e fora do caminho crítico, e é assim que pagam a conta. Qualquer JS decorativo novo compete com eles pela mesma CPU, então cada recurso do redesign precisa custar perto de zero no main thread. A defesa contra o custo dos anúncios é posicional: slot nunca no primeiro viewport, altura sempre reservada (o site já faz as duas coisas).

---

## 2. O que NÃO pode entrar, com o preço em métrica

**2.1 Canvas/WebGL em tela cheia permanente (fundo animado, "hero shader").**
Numa tela de 393×851 CSS px com DPR 2,75, um fragment shader pinta ~2,3 megapixels por frame; a 60 fps é um compositor permanentemente ocupado num GPU de celular de entrada, 5 a 15% de CPU/GPU contínuos, aquecimento e bateria. Pior: `<canvas>` não é candidato a LCP. Se o herói vira canvas, o LCP cai para o maior texto visível, e se esse texto entra com fade-in via JS, o LCP explode para o momento do script. Efeito colateral: os iframes de anúncio também compõem em GPU; canvas grande + 2 anúncios = disputa de memória de GPU e jank de rolagem. Veredito: proibido em home e template de matéria, em qualquer tamanho "full-screen".

**2.2 Shader ou animação no elemento LCP.**
Regra dura: o LCP precisa ser um `<img>` ou bloco de texto presente no HTML inicial, pintado no primeiro render do CSS, sem `opacity:0` inicial, sem dependência de JS. Cada 100 ms de atraso artístico no herói é 100 ms somado direto no LCP de todas as visitas. Discover e Top Stories usam o p75 de CWV como sinal; isso é receita, não estética.

**2.3 Scroll-jacking / smooth scroll sintético (o que o Lenis faz).**
Sequestrar a rolagem move o scroll do thread do compositor para o main thread: cada `wheel`/`touchmove` vira trabalho de JS. Num aparelho intermediário isso é INP degradado (handlers de 30 a 80 ms por evento em página com anúncios), quebra `scroll-snap` do carrossel, quebra as animações CSS por rolagem que o site já usa (elas leem o scroll real), quebra âncoras, busca na página e leitores de tela. Custo certo, benefício zero para leitura de notícia. Proibido.

**2.4 Framework com hidratação (React, e por tabela React Three Fiber e Framer Motion).**
React DOM ~45 KB gz, Three.js ~150 KB gz, R3F por cima. Só o parse e execução disso num Android intermediário custa 1 a 3 s de CPU antes de qualquer pixel útil, TBT na casa de centenas de ms, INP comprometido em página com anúncios. Além do custo, a Constituição veda dependência externa. Não entra em nenhuma forma, nem "só numa página".

**2.5 GSAP (~28 a 70 KB gz) e bibliotecas de animação em geral.**
Vedado pela regra de dependências, e desnecessário: transform/opacity via CSS e WAAPI cobrem 95% do repertório, com easing de mola via `linear()` (ver §3.11).

**2.6 WebAssembly/Rust.**
Tecnicamente compatível com site estático, mas honestamente sem caso de uso aqui: o acervo tem dezenas de matérias, qualquer busca local resolve com um índice JSON de poucos KB e JS puro. Wasm adicionaria fetch + compile (dezenas de ms) para nada. Se um dia houver mapa interativo pesado ou processamento de dados no cliente, reavaliar; hoje, não.

**2.7 WebGPU.**
Suporte móvel ainda desigual em 2026 e mesmo problema do 2.1. Se algum dia entrar, entra pelas mesmas regras do WebGL pequeno (§3.10), como camada extra de enhancement com fallback. Não é fundação de nada.

**2.8 Mais famílias ou pesos de fonte.**
Cada peso novo custa 15 a 45 KB no caminho de render do texto, e cada troca de fonte sem métrica de fallback ajustada é CLS. O redesign trabalha com Archivo + Newsreader e os pesos que já existem. Direção de arte nova se expressa em tamanho, cor, espaçamento e composição, não em fonte nova.

**2.9 Parallax via `background-attachment: fixed` e blur generoso.**
`background-attachment: fixed` força repaint por frame de rolagem (e é ignorado em boa parte do mobile). `backdrop-filter` com raio alto em header sticky custa GPU em cada frame de rolagem em cima justamente do gesto mais frequente do leitor. Se quiser vidro fosco, raio ≤ 8 px e testar em aparelho real; na dúvida, cor sólida com transparência.

**2.10 Rolagem infinita na home.**
Cresce DOM sem teto, briga com CLS quando anúncios entram no meio, quebra rodapé, histórico e paginação para o Google. A paginação existente fica.

---

## 3. O que PODE entrar barato

Registro primeiro o que o site **já usa** e o redesign deve preservar, porque já é estado da arte de custo zero: view transitions cross-document com header/footer fixos, barra de progresso via `animation-timeline: scroll()`, `text-wrap: balance/pretty`, speculation rules com prerender `moderate`, reserva de espaço de anúncio por `aspect-ratio`, carrossel por `scroll-snap` funcional sem JS, `prefers-reduced-motion` global.

Adições recomendadas, cada uma com custo e fallback:

1. **View transitions expandidas (a assinatura visual do redesign).** Dar `view-transition-name` à imagem do card e à imagem de topo da matéria: o clique faz a foto "voar" do card para a matéria, com o prerender das speculation rules garantindo que a página destino já está pronta. Custo: só CSS, 0 JS. Fallback: navegação instantânea normal. Limite: no máximo ~8 elementos nomeados por página, cada um vira snapshot em camada própria. Este recurso, bem coreografado, entrega a sensação de "app moderno" que se pediria ao Framer Motion, por zero byte.

2. **Animações CSS por rolagem (`animation-timeline: view()`) no lugar do reveal-on-scroll em JS.** Substitui ~120 linhas de `visual.js` (IntersectionObserver + listener de scroll + failsafe de 2 s). Progressive enhancement invertido e seguro: o elemento só é escondido dentro de `@supports (animation-timeline: view())`, então onde não há suporte o conteúdo simplesmente aparece. Custo: negativo (remove JS). Roda no compositor.

3. **`content-visibility: auto` + `contain-intrinsic-size`** nas seções abaixo da dobra (Resumo Semanal, Ferramentas, rodapé, "Outros jeitos de ler"). Corta 20 a 40% do trabalho de layout/paint inicial em página longa. Custo: 0 bytes. Fallback: nada acontece, que já é o comportamento atual.

4. **Container queries** para o card existir em três densidades (grade, coluna lateral, lista) sem media query global. Custo: 0, suporte universal em 2026. É a ferramenta que permite o redesign ter layout editorial mais rico sem duplicar CSS.

5. **`@property`** para animar cor/gradiente tipados (ex.: o degradê do bloco escuro respirando ao rolar, amarrado ao item 2). Custo: bytes de CSS. Fallback: valor estático.

6. **`interpolate-size: allow-keywords`** para abrir/fechar os painéis do Modo de Leitura com transição de altura suave sem JS de medição. Chrome-only por ora; fallback: abre instantâneo, que é o comportamento atual.

7. **Auto-hospedar as fontes** (ver §4.2). Não é técnica nova, é a maior vitória individual de LCP disponível.

8. **AVIF nas miniaturas e fotos**, com `srcset` 480w/720w/1600w. Um card 720w em AVIF q50 fica em 25 a 35 KB contra 37 a 57 KB do JPEG atual, e o celular baixa a variante 480w. Ganho de 50 a 150 ms no LCP em 4G, e corte de ~40% no peso total de imagem. Custo: pipeline no `ferramentas/`, zero em runtime.

9. **SVG animado da marca (o `.anima` existente) como linguagem visual principal.** Já é compositor-friendly (só transform/opacity), pausável e com reduced-motion. É o equivalente honesto do "site com movimento": expandir o repertório de cenas (mar, obra, mapa) custa 2 a 5 KB de SVG por cena e nada de JS novo.

10. **WebGL pequeno, manual e pausável, só em páginas especiais** (retrospectiva do ano, especial do verão), nunca no template de matéria nem na home. Regras de contrato: canvas limitado (faixa de herói ou vinheta ≤ ~50% do viewport), DPR travado em ≤ 1,5, init adiado para depois do `load` via `requestIdleCallback`, pausa por IntersectionObserver quando fora de tela e por `visibilitychange`, `prefers-reduced-motion` recebe um poster estático (imagem ou SVG), shader + boilerplate escritos à mão em ~4 a 6 KB. Fallback obrigatório: a página funciona inteira com o poster.

11. **WAAPI + easing `linear()`** para microinterações com física de mola (chips do Modo de Leitura, botão de pausa): `element.animate()` nativo, easing de mola serializado em `linear(...)`. É o substituto de GSAP a custo zero de dependência.

12. **Popover API e `<dialog>`** para menu de compartilhar e avisos, sem JS de posicionamento. Custo: 0. Suporte universal em 2026.

13. **Early Hints no Cloudflare Pages** via `_headers` (`Link: rel=preload` das fontes e do CSS no 103). Custo: um arquivo de configuração. Ganho: 50 a 150 ms no caminho crítico em conexões de RTT alto.

14. **Speculation rules, ajuste fino:** manter `moderate` como está; adicionar `prefetch` `eagerness: conservative` como degrau para navegadores sem prerender. O Chrome já desativa prerender sozinho com Save-Data ativo, então o leitor de plano limitado está protegido.

---

## 4. Riscos do site atual que o redesign deve corrigir

1. **`<script src="visual.js">` síncrono no `<head>` de todas as páginas.** É render-blocking: o parser para, baixa e executa antes de pintar qualquer coisa. Em cache frio 4G, 100 a 250 ms somados direto no FCP/LCP de graça. Correção: `defer` (uma palavra; o código já espera `DOMContentLoaded`). A única linha que precisa rodar cedo, o `classList.add('rv-on')`, morre junto com o item 3.2 acima, ou vira um inline de 40 bytes.

2. **Google Fonts em duas origens de terceiro no caminho crítico.** O CSS de `fonts.googleapis.com` é render-blocking e os woff2 vêm de `fonts.gstatic.com`: dois handshakes extras, 300 a 700 ms típicos em móvel frio, mais CLS de swap. Correção: baixar os woff2 subsetados (latin), servir da própria origem no Cloudflare, `font-display: swap` com fallback metricamente ajustado (`size-adjust`, `ascent-override` sobre Georgia/system-ui) para o swap não deslocar nada. Corta as duas origens e praticamente zera o CLS de fonte.

3. **Imagem de topo da matéria sem `fetchpriority="high"`.** Na home o primeiro slide já tem; na matéria (o template que o Discover manda gente ver) a `figure` é `loading="eager"` mas concorre em prioridade normal com todo o resto. Correção no template canônico: `fetchpriority="high"` no `<img>` da figura de topo, e conferir que nenhuma matéria a marque como `lazy`.

4. **Pipeline de WebP ineficaz.** `obra-emissario-rua.webp` tem 493 KB contra 528 KB do JPEG de origem; várias conversões passam de 300 KB. Está convertendo sem recomprimir. Correção em `ferramentas/`: teto de 1600w, qualidade ~60 a 70, meta ≤ 180 KB por foto de matéria, e gerar AVIF junto (item 3.8).

5. **Fotos de matéria de até 528 KB servidas a celular.** Com `srcset` 800w presente só em parte das páginas. Padronizar o bloco `<picture>` do modelo canônico em todas as matérias, com a variante 800w como default móvel.

6. **Wordmark do logo depende da webfont dentro do SVG.** Os `<text>` do cabeçalho usam Archivo; até a fonte chegar, o logo pinta com fallback e troca de desenho no swap, no elemento mais visível do site. Correção: converter o wordmark em paths (custo único de ~2 a 3 KB por página, estabilidade total de pintura).

7. **Altura de anúncio AdSense reservada no mínimo, não no provável.** `min-height: 90px` (100 no celular) segura o layout, mas formato responsivo pode devolver criativo mais alto e empurrar o texto (CLS no meio da leitura). Correção: fixar altura por breakpoint no contêiner (`height`, não `min-height`) casada com `data-ad-format` fixo, aceitando eventual letterbox dentro do slot.

8. **Autoplay do carrossel.** `setInterval` + `scrollTo smooth` a cada 6 s gera trabalho de rolagem no main thread e disputa atenção com o conteúdo. O controle de pausa está impecável (WCAG 2.2.2 coberta), mas o redesign deveria considerar autoplay desligado por padrão, girando só após interação. Custo zero, INP e bateria agradecem, e a acessibilidade que já existe (pausa, foco, reduced-motion) não pode regredir em nenhum cenário.

9. **Estilos inline repetidos no HTML** (`style="color:inherit;text-decoration:none"` em cada card, `style="padding-bottom:56px"` em seção). Multiplicado por página gerada em lote, é peso e armadilha de especificidade. Mover para classes em `estilo.css` no template canônico.

10. **Reveal-on-scroll em JS** com listener de scroll global e failsafe de timeout: funciona, mas é main thread em cada rolagem. Substituir pela versão CSS (item 3.2), que também elimina o risco residual de conteúdo ficar 2 s invisível se o observer atrasar.

Síntese para o agente que vai desenhar: o orçamento livre real do redesign é ~15 KB de CSS extra, ~25 KB de JS extra (tudo defer) e zero terceiros novos. A modernidade que cabe aqui se chama view transitions + scroll-driven animations + container queries + SVG animado, com WebGL artesanal confinado a páginas especiais. Three.js, R3F, GSAP, Framer Motion e Lenis não entram nem tecnicamente (Constituição veda dependência) nem economicamente (o AdSense já consome o main thread que eles exigiriam); os equivalentes vanilla acima cobrem o efeito percebido. As quatro correções de maior retorno, antes de qualquer estética: `defer` no `visual.js`, fontes auto-hospedadas com fallback ajustado, `fetchpriority="high"` no topo da matéria e pipeline de imagem com AVIF e recompressão.