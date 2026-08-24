# JÚRI FINAL · REDESIGN SANTA INFORMA

## 1. Notas

### Direção 1 · Primeira Página
| Critério | Nota | Justificativa |
|---|---|---|
| Identidade | 7 | Elegância de Zeit/NYT bem executada, mas é uma identidade de categoria (jornal sério), não de lugar: qualquer portal poderia vesti-la. |
| Viabilidade | 10 | 100% CSS com fallback declarado em tudo; o risco técnico mais grave é um `clamp()` mal calibrado. |
| Performance | 9 | Quase custo zero; perde um ponto pelos ~50 KB de itálico e peso 500 da Newsreader no caminho do LCP. |
| Jornalismo | 10 | É a única direção que ataca o defeito número um da crítica: a home sem manchete. Capa de 3 chamadas, rail de matéria, medida de 65ch, tudo serve à leitura. |
| Fator uau | 6 | O leitor sente qualidade mas não vê espetáculo; a assinatura (entrada da capa + voo) é discreta por tese. |

### Direção 2 · Litoral Vivo
| Critério | Nota | Justificativa |
|---|---|---|
| Identidade | 10 | Céu que segue a hora de Itapema e mar na dobra: nenhum veículo do Brasil tem isso, e é intransferível. |
| Viabilidade | 7 | O shader é o único trecho do repositório que exige conhecimento especializado, num projeto mantido por agentes e um editor solo. |
| Performance | 7 | As salvaguardas são exemplares, mas GPU contínua + AdSense no Android intermediário é exatamente a disputa que o caderno de restrições manda evitar; e a faixa de 96px empurra a dobra no celular. |
| Jornalismo | 6 | Mantém o carrossel e a grade uniforme: o problema editorial da home fica em pé. O movimento mora nas bordas e não hierarquiza nada. |
| Fator uau | 10 | O amanhecer às 6h40 com reflexo dourado alinhado ao logotipo é o momento mais memorável de todo o material. |

### Direção 3 · Cinética Editorial
| Critério | Nota | Justificativa |
|---|---|---|
| Identidade | 7 | "Movimento como hierarquia" é um sistema forte, mas é gramática, não sotaque: falta o litoral. |
| Viabilidade | 9 | Quase tudo é plataforma; o ponto frágil declarado (dois sistemas de reveal coexistindo atrás de um `CSS.supports`) é real mas administrável. |
| Performance | 8 | Disciplinada (LCP proibido de animar, tabular-nums nos contadores), mas split de manchete em spans e mola global são JS novo em cima do main thread que o AdSense já cobra. |
| Jornalismo | 8 | O movimento diz o que ler primeiro e o voo de capa dá continuidade de leitura; porém não redesenha a capa, e manchete palavra a palavra atrasa a informação em nome do efeito. |
| Fator uau | 8 | O voo de capa entre páginas é o efeito "de app" de maior retorno por byte de todo o material. |

**Totais: D1 = 42 · D2 = 40 · D3 = 40.**

## 2. Vencedora e enxertos

**Vence a Direção 1, Primeira Página.** É a única que resolve o problema editorial (hierarquia), tem risco técnico próximo de zero e protege a receita (CWV). Um portal de notícias precisa primeiro parecer um jornal excelente; espetáculo é camada, não fundação.

**Enxertos da Direção 2 (o sotaque):**
- Céu por hora no cabeçalho via `color-mix()` sobre as variáveis existentes, com fallback no breu atual. Custo: bytes de CSS, pega carona no relógio que já roda por minuto.
- Onda divisória com deriva animada (loop `translateX`, padrão `.corre` já existente), pausável.
- Resumo Semanal cravado no estado "anoitecer" como âncora fixa da marca.
- O módulo Mar Vivo WebGL do especialista, **confinado a uma página especial**, nunca na home nem no template de matéria (ver §3.6).

**Enxertos da Direção 3 (a gramática):**
- O voo de capa: view transition nomeada na imagem card → matéria, com o tuning do especialista de motion (`view-transition-class`, sem crossfade esticado).
- A mola física de ~60 linhas para chips e botões.
- Tokens de movimento com curva única da casa.
- Dark mode por camada semântica de tokens (com a tabela de contraste do tipógrafo).
- Stroke-draw dos ícones das Ferramentas (420ms, decorativo, barato).

**Do time de especialistas, integral:** escala tipográfica do tipógrafo (é mais completa que a da D1), receitas do motion (reveal CSS substituindo o IO, mola, view transition), e as quatro correções de fundação do caderno de restrições.

**O que se rejeita em definitivo:** manchete palavra a palavra na home (atrasa o LCP textual e a informação), contadores numéricos na home (ficam para matéria, fase 2), faixa de mar de 160px (dobra do celular é sagrada), Three.js, R3F, GSAP, Framer Motion, Lenis, WASM, Rust e WebGPU (vetados por Constituição e por mérito, como os quatro pareceres convergem).

---

## 3. BLUEPRINT FINAL · Protótipo da home

### 3.0 Fundação obrigatória antes de qualquer estética

Na ordem, cada item é um commit pequeno:

1. `defer` no `<script src="visual.js">` de todas as páginas.
2. Fontes auto-hospedadas: baixar woff2 subsetados (latin) de Archivo variável (wght 400..800) e Newsreader variável (opsz 6..72, wght 400..600, roman + itálico). Máximo 4 arquivos, teto de 110 KB somados. `font-display:swap` + dois `@font-face` de fallback com `size-adjust`/`ascent-override` (Newsreader-fb sobre Georgia ~105%, Archivo-fb sobre Arial ~97%). Remove as duas origens Google do caminho crítico. `_headers` no Cloudflare com Early Hints (preload do CSS e das 2 fontes principais).
3. `og:image` + `twitter:card` no index e no template de matéria (defeito de maior impacto real apontado pela crítica: a matéria circula no WhatsApp sem cartão).
4. `fetchpriority="high"` na imagem de topo do template de matéria.
5. Todos os estilos inline do index viram classes (`.link-cartao`, `.secao-funda`, etc.). Truncamento "…" manual sai; entra `-webkit-line-clamp:3` na chamada do card.
6. Wordmark do logo convertido em paths (~2 KB por página, estabilidade de pintura no elemento mais visível).
7. Pipeline em `ferramentas/`: teto 1600w, qualidade 60-70, meta ≤180 KB por foto, gerar AVIF + `srcset` 480/720/1600w.

### 3.1 Estrutura da home, de cima a baixo

Grid mestre: `.capa-grade{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:clamp(16px,2.4vw,32px)}` no wrap de 1180px.

**S1 · Cabeçalho-céu.** Estrutura atual (logo SVG com wordmark em paths, nav, barra de editorias). Fundo: `linear-gradient(var(--ceu-alto),var(--ceu-baixo))` com defaults iguais ao breu de hoje; ~10 linhas no `visual.js` (penduradas no relógio existente, `Intl` com `America/Sao_Paulo`) escrevem as variáveis por hora. Quatro estados via `color-mix()` conforme a receita da D2 (noite/amanhecer/dia/entardecer), texto sempre no terço superior, topo nunca mais claro que `--mar` (pior caso espuma sobre mar ≈ 8:1). `@property` nas duas variáveis para transição de 1200ms; sem suporte, troca seca por minuto. Sol do logotipo com `translateY` por hora; lua (`#i-lua` do sprite) das 19h às 5h. Animação de entrada do logo passa a rodar só na home. Barra `.editorias` vira sticky com elevação por `animation-timeline:scroll(root)`, range 0-120px, dentro de `@supports`.

**S2 · Pacote de capa (o carrossel sai).**
- Colunas 1-8: manchete. Filete 28×3px em `--sol`, chapéu `--t-ui` Archivo 600 caps, título em `--t-capa-lead` Archivo 800 (ls -0.03em, max-width 20ch), linha fina Newsreader itálico `--t-linhafina` cor `--tinta-2` (max 52ch), meta com data em oldstyle. Foto 3:2 com `fetchpriority="high"`, `aspect-ratio` reservado, receita única `.foto-tratada{filter:saturate(.94) contrast(1.03)}`.
- Colunas 9-12: rio de últimas. 5-6 itens, hora em Archivo 600 `tabular-nums` cor `--tinta-2`, título Archivo 600 (não 800), filete `--fio` entre itens, sem imagem. `border-left:var(--fio) solid var(--fio-cor)`.
- Colunas 1-8, abaixo da manchete: banda de 2 sub-destaques em N-card com chapéu, separados por filete.
- Mobile (<720px): empilha manchete → rio (4 itens) → sub-destaques. A manchete textual vira candidata a LCP (melhor cenário). Cards viram linha de lista com miniatura 88px à direita (3 matérias por tela).
- Bloco HTML comentado com ordem fixa (líder, sub1, sub2, rio) para o agente de notícias preencher.

**S3 · Super banner.** Intocado, mas a reserva muda de `min-height` para `height` fixa por breakpoint casada com `data-ad-format` fixo (aceita letterbox, mata o CLS de criativo alto).

**S4 · Onda divisória animada.** A `.onda` atual ganha segunda path defasada, as duas a 200% de largura em loop `translateX` (26s e 34s, compositor). Obedece o kill switch global e o botão de pausa.

**S5 · Itapema e Costa Esmeralda.** Título de seção com filete duplo (scotch rule: 3px `--breu` + 1px `--areia` com 3px de vão). Primeira linha assimétrica: líder com foto 16:9 em 6 colunas; à direita, pilha de 3 chamadas só-texto (Newsreader 600 `--t-card`, linha fina de uma frase, filetes). Segunda linha: 3 cards de 4 colunas herdando `article.card`. `container-type:inline-size` na grade; o card se adapta à coluna, não à tela.

**S6 · Resumo Semanal.** Bloco escuro cravado no gradiente anoitecer (mar → breu), independente da hora. Números 01-07 em Newsreader 500 2rem `oldstyle-nums` cor `--sol` pendurados à esquerda (contraste >3:1 em texto grande, revalidar). `content-visibility:auto` + `contain-intrinsic-size` daqui para baixo.

**S7 · Ferramentas do litoral.** Cards `.d` atuais; rótulo em Newsreader 600 2rem; ícones stroke-draw ao entrar (`stroke-dasharray/dashoffset`, 420ms); linha da maré no hover/focus (2px `--sol`, `scaleX` 320ms). Rótulo genérico "Abrir página" vira verbo específico por card.

**S8 · Rodapé.** Onda espelhada na entrada, estático, `view-transition-name` mantido.

**Manifesto/institucional:** sai da grade de notícias; vira uma faixa fina própria acima do rodapé, visualmente distinta (fundo `--espuma`, sem card), para nunca mais confundir institucional com jornalismo.

### 3.2 Sistema tipográfico final

Duas vozes (padrão Zeit): **Archivo = fluxo** (capa, cards, UI, números), **Newsreader = leitura** (matéria, linhas finas, semanal). Tokens no `:root`:

```css
--t-manchete:   clamp(1.9rem,1.13rem + 3.08vw,3.4rem);    /* matéria, Newsreader 600 opsz 72 forçado, lh 1.1, ls -.01em */
--t-capa-lead:  clamp(1.625rem,1.05rem + 2.31vw,2.75rem); /* capa, Archivo 800, lh 1.05, ls -.03em */
--t-secao:      clamp(1.19rem,1.06rem + .51vw,1.44rem);   /* Archivo 800, caps não */
--t-card:       clamp(1.0625rem,.95rem + .45vw,1.28rem);  /* Archivo 800, lh 1.18 */
--t-linhafina:  clamp(1.0625rem,.97rem + .38vw,1.25rem);  /* Newsreader itálico 500, lh 1.45 */
--t-corpo:      clamp(1.0625rem,1rem + .26vw,1.1875rem);  /* Newsreader 400, lh 1.6 */
--t-legenda:    clamp(.85rem,.8rem + .2vw,.95rem);        /* Newsreader 400, opsz 10 forçado */
--t-ui:         clamp(.72rem,.68rem + .18vw,.81rem);      /* Archivo 600 caps, tracking .09-.13em */
--t-num:        clamp(1.625rem,1.3rem + 1.28vw,2.25rem);  /* Archivo 800 tabular-nums */
```

Espaçamento em base 4: `--esp-1` a `--esp-6` (0.25 a 2rem), `--esp-7:clamp(2.5rem,2rem + 1.5vw,3.5rem)`, `--esp-secao:clamp(3rem,2.2rem + 2.5vw,4.5rem)`. Todos os paddings/margins aleatórios atuais (52/50/56/38) migram para a escala.

Detalhes finos que entram: hairline `--fio:1px` (0.5px em 2dppx); `oldstyle-nums` em datas e semanal, `lining-nums tabular-nums` em preços e rio (testar se o subset expõe `onum`; se não, inerte); `hyphens:auto` no corpo <600px; `hanging-punctuation` (Safari, 1 linha); `text-box:trim-both cap alphabetic` em manchetes e títulos de card (progressivo). Versaletes sintéticos proibidos (`font-synthesis-small-caps:none`). Nenhuma família nova, nunca.

### 3.3 Paleta final

Os 8 hex são intocáveis. Entra camada semântica fina:

```css
:root{
  --fundo:var(--espuma); --tinta:var(--breu); --tinta-2:var(--suave);
  --superficie:#fff; --fio-cor:var(--areia); --link:var(--mar);
  color-scheme:light;
}
@media(prefers-color-scheme:dark){:root{
  --fundo:#0C181E; --tinta:#E9F0F1; --tinta-2:#9FB1B6;
  --superficie:#10222B; --fio-cor:rgba(207,196,180,.16);
  --link:var(--mar-claro); --coral-chapeu:#F0654C;
  color-scheme:dark;
}}
```

Dark mode **entra no protótipo**: cabeçalho, hero, semanal e rodapé já são escuros e não mudam (âncora da marca nos dois modos); só o papel inverte. Contrastes validados pelo tipógrafo (tinta 15:1, sol 10.4:1, link 7.9:1, coral clareado 5.8:1). As duas cores novas (#0C181E, #F0654C) são derivação por necessidade de contraste e **precisam de aprovação explícita do editor**, porque a Constituição é dele. `<meta name="color-scheme" content="light dark">` no head. Fotos: `filter:brightness(.88)` opcional no dark + fio `rgba(255,255,255,.12)`. Dosagem no light: `--sol` só como acento fino (filete 3px, foco, hover), `--coral` exclusivo de chapéu, `--areia` cor oficial de filete. Céu por hora: exclusivamente `color-mix()` das variáveis existentes, regra "nenhum hex novo" registrada no CLAUDE.md junto da aprovação.

### 3.4 Hero assinatura: "A capa amanhece, a capa voa"

**Tempo 1, a chegada (CSS puro, roda uma vez, <1s total).** A página pinta completa de imediato; no mobile a manchete textual é o LCP e nada a esconde. Sobre a base estável: filete âmbar se desenha (`scaleX` 0→1, 450ms, curva da casa), chapéu fade 300ms, manchete sobe 14px com fade (650ms, delay 120ms), linha fina idem (delay 260ms), foto se revela por `clip-path inset(0 0 100% 0)→inset(0)` (700ms, delay 200ms, img de scale 1.03→1). Sem split de palavras (rejeitado na home). Estado invisível mora só no `from` dos keyframes: sem suporte ou com reduced motion, a capa nasce pronta. Sem JS, roda igual (é CSS).

**Tempo 2, a partida.** No `pointerdown` de um card, mola para scale 0.985. No `click`, 6 linhas de JS gravam `view-transition-name` único (`capa-mNN`) na `<img>` do card; a matéria carrega a mesma imagem com o mesmo nome. A foto viaja e cresce até virar o topo da matéria em 300ms (`--dur-troca`), sem crossfade (`::view-transition-old/new(.capa){animation:none}` conforme receita do motion), cabeçalho e rodapé imóveis (nomes já existem), raiz em fade de 180ms. Speculation rules (já ativas) pré-renderizam o destino no hover: o voo pousa em página pronta. Teto duro: 5 elementos nomeados por página.

**Degradação:** Firefox e navegadores antigos, navegação normal instantânea; reduced motion, `@view-transition{navigation:none}` já existente; a assinatura degrada para silêncio, nunca para erro.

**Orçamento do hero:** ~0 KB de JS além das 6 linhas do nome dinâmico; keyframes ~1 KB de CSS; zero impacto em LCP (nada anima o candidato), zero CLS (tudo transform/opacity/clip-path).

### 3.5 Sistema de movimento final (lista fechada)

Tokens no topo do `estilo.css`: `--dur-toque:.15s`, `--dur-troca:.3s`, `--dur-chegada:.55s`; curva única da casa `--curva:cubic-bezier(.2,.7,.3,1)` (a que já existe, agora nomeada); `--curva-mola:cubic-bezier(.34,1.56,.64,1)` só em transform de micro-interação. Duração fora dos tokens é proibida. Só `transform`, `opacity` e `filter` curto.

| # | Efeito | Técnica | Reduced motion |
|---|---|---|---|
| 1 | Entrada da capa (home, 1x) | CSS keyframes encadeados | Não roda; capa nasce pronta (estado no `from`) |
| 2 | Voo de capa card→matéria | Cross-doc view transition nomeada + tuning `.capa` | Desligado pelo `@view-transition` existente |
| 3 | Reveal por rolagem | `animation-timeline:view()`, range entry 0/55%, `linear`, `both`, escalonado por `:nth-child` em `@supports`; onde falta, o IO do `visual.js` assume via `if(!CSS.supports('animation-timeline: view()'))` (interruptor único, comentário gordo) | Kill switch global; conteúdo visível |
| 4 | Céu por hora | `@property` + transition 1200ms, `color-mix()` | Troca seca (cor não é movimento, mantém) |
| 5 | Onda divisória | Loop `translateX` 26s/34s, padrão `.corre` | Parada |
| 6 | Elevação da barra sticky | `animation-timeline:scroll(root)` 0-120px | Sombra estática ausente |
| 7 | Linha da maré (hover/focus card) | Pseudo-elemento `scaleX` 320ms | Morta |
| 8 | Mola de pressão (chips, botões) | JS ~60 linhas, rigidez 220/amort. 26, WeakMap, rAF que dorme | `matchMedia` no início: aplica estado final direto |
| 9 | Stroke-draw ícones Ferramentas | `dasharray/dashoffset` 420ms ao `.vis` | Ícone pronto |
| 10 | Barra de progresso (matéria) | `scroll()` já em produção | Já ausente |

Governança: nenhum listener de scroll novo; o bloco de reveal em JS (linhas 67-118 do `visual.js`) é rebaixado a fallback; anúncios fora de qualquer contêiner com timeline ou transition; nenhuma animação encosta em `.pub-google`/`.anuncio`. Consolidação reduced-motion em 3 mecanismos: kill switch global CSS (linha 494), `@view-transition navigation:none`, `matchMedia` em todo caminho JS. Princípio inegociável: **estado invisível mora sempre no `from` do keyframe.**

### 3.6 WebGL: o que entra e com que salvaguardas

**Não entra na home nem no template de matéria. Ponto.** O caderno de restrições demonstrou a conta: canvas permanente disputa GPU com os iframes do AdSense e não gera page view.

O que entra: o módulo **Mar Vivo** do especialista (shader ~150 linhas + boilerplate ~80 linhas no fim do `visual.js`, 3 linhas de CSS), aplicado a **uma única página especial** (candidata: `especial-verao.html` ou a página institucional, decisão do editor). Salvaguardas, todas obrigatórias, todas já escritas no parecer:

- Camadas: gradiente estático no HTML (camada 0) → SVG animado `.anima` (camada 1, o padrão) → canvas WebGL2 por cima (camada 2, opt-in do navegador). O HTML entrega a camada 1 pronta; o canvas cobre, nunca substitui.
- Montagem: só depois do `load`, em `requestIdleCallback` (timeout 2000ms, fallback `setTimeout` 1200ms). Nada compila na janela do LCP.
- Portões: sem `prefers-reduced-motion` (nem monta; mudou na sessão, desmonta), sem `saveData`, `deviceMemory` ≥ 4 quando exposto, WebGL2 real, compile+link com sucesso (falhou, retorno silencioso).
- Execução: 30fps por gate de timestamp no rAF, DPR ≤ 1.5, relógio próprio acumulado, `powerPreference:'low-power'`, IO cancela fora da viewport, `visibilitychange` pausa, `webglcontextlost` desmonta em definitivo, botão "Pausar animação" existente vale (MutationObserver na classe `.pausada`).
- Killswitch editorial: `data-mar="off"` no `<html>` impede a montagem sem novo deploy.
- Correção anotada pelo próprio especialista: a última linha do boilerplate é `cena.appendChild(cv);`.
- Paleta do shader: os mesmos hex de `estilo.css` convertidos, nenhuma cor nova.

O enxerto da D2 que a home recebe é a versão barata do mesmo espírito: céu por hora + onda animada, custo de bytes de CSS.

### 3.7 Ordem de construção

1. **Fundação** (§3.0, itens 1-7). Cada item um commit. Medir PageSpeed antes/depois.
2. **Tokens**: escala tipográfica, espaçamento, movimento, camada semântica de cor. Refatorar valores fixos existentes para os tokens.
3. **Capa nova**: pacote 8/4 + rio, carrossel removido, banda de sub-destaques, breakpoints 1020/720. Testar dobra em 360×640: manchete visível, `fetchpriority` na foto só quando ela cabe na dobra.
4. **Seções**: grade assimétrica com container queries, scotch rules, semanal anoitecer, ferramentas, faixa institucional, rodapé.
5. **Movimento**: reveal CSS + interruptor de fallback, entrada da capa, voo de capa, mola, linha da maré, stroke-draw.
6. **Céu por hora + onda animada** (último enhancement, primeiro a cortar se algo estourar orçamento).
7. **Dark mode**: tokens remapeados, varredura dos literais `--espuma`/`#fff`/`--breu` nos seletores de conteúdo.
8. **QA de gate**: contraste AA nos 4 estados de céu (entardecer é o pior caso) e nos 2 temas; reduced-motion em tudo (Tab real, leitor de tela); teste em aparelho classe Moto G com anúncio servido; LCP p75 < 2,0s, CLS < 0,05, INP < 200ms; nenhuma regressão de a11y (skip link, foco, alvos 24px). Sem carrossel, a obrigação WCAG 2.2.2 da home desaparece; o botão de pausa da onda permanece.

**Orçamento do protótipo:** CSS +~14 KB bruto (fica < 25 KB gz de teto com folga), JS líquido ≈ +1 KB (mola e céu entram, reveal IO vira fallback), zero requests de terceiro novos, 2 origens de terceiro removidas (fontes).

## 4. Fase 2 (boas ideias que não entram no protótipo)

1. **Mar Vivo WebGL na página especial** (código pronto no parecer, espera a página existir e o editor aprovar).
2. **Template de matéria completo**: rail sticky de 200px com âncoras, medida 65ch com mídia sangrando a 760px, capitular `initial-letter`, manchete Newsreader opsz 72, chips do Modo de Leitura com identidade por colunista (Clara `--sol`, Prudêncio `--mar`, Caco `--coral`, pictogramas do sprite), `interpolate-size` nos painéis. O protótipo é a home; a matéria herda os tokens depois.
3. **Sistema de dataviz autoral**: stat tiles, sparklines SVG com stroke-draw, mapa SVG do trecho da orla, contadores `data-conta` com `tabular-nums`. É a assinatura editorial de maior potencial do material inteiro, mas pertence ao template de matéria.
4. **Scrollytelling** com `animation-timeline:view()` para matérias especiais (a técnica já está na casa).
5. **Cascata de palavras** no h1 de matérias especiais com foto (nunca quando o título disputa LCP), com o par aria-label/aria-hidden obrigatório.
6. **Popover nativo** para compartilhar e microglossário (Selic, LDO).
7. **Archivo wdth** (voz condensada em chapéus) se a sintaxe de intervalo não custar bytes: medir.
8. **Autoplay de carrossel desligado por padrão** onde carrosséis sobreviverem (páginas de editoria).
9. **Prefetch `conservative`** como degrau das speculation rules.
10. **Auditoria de 28 dias** pós-deploy em CrUX e Search Console antes de promover qualquer enhancement da fase 2.

**Registrar no CLAUDE.md junto da aprovação:** convenção `capa-mNN` (card e topo de matéria usam a mesma imagem/enquadramento), regra "nenhum hex novo, toda cor derivada por color-mix", as duas cores do dark aprovadas pelo editor, e a nota de que em Firefox o site fica correto e mais sóbrio (sem voo, sem capitular), por design e não por defeito.