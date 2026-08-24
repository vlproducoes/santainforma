# PLANO DE VIABILIZAÇÃO · CENAS TEMÁTICAS PSEUDO-3D

## 1. DECISÃO TÉCNICA

SVG inline em camadas dentro do `div.anima` existente, profundidade por sobreposição desenhada mais razão de velocidades entre camadas (multiplane), animando só `transform` e `opacity` com os verbos de `estilo.css`. Perspective real (`perspective`, `preserve-3d`, `translateZ`) fica proibida: incompatível com o `overflow:hidden` obrigatório do `.anima` (clipping força flattening, é spec), e o tilt de entrada proposto pelo motion cai junto, ganho visual nulo numa faixa 16/7. Scroll-driven parallax (`animation-timeline:view()`, classes `.paralaxe-1..3`) entra como enhancement de Fase 2 sob `@supports`, degradando para os loops atuais. Entrega pelo modelo de fragmentos canônicos de PRODUÇÃO (opção c): o agente da nuvem copia byte a byte de `ferramentas/cenas/`, nunca desenha; validação no `checa-site.py` compara o núcleo do fragmento com o cânone. Divergências resolvidas: o clarão do raio da cena clima é cortado (regra de fotossensibilidade do motion vence; o raio fica no desenho com `.pulsa` comum de 6 s, degradação que o próprio autor da cena já documentou como válida), e a regra "máximo 1 `.corre`" da plataforma é substituída por orçamento de textura verificável (abaixo), porque a cena clima aprovada tem 3 `.corre` e passa no orçamento real.

## 2. FASE 1 (esta semana)

Tudo numa branch. Nada em `main` sem o editor (Regra 2).

**Passo 1 · Canonizar os fragmentos.** Criar `ferramentas/cenas/` com:

- `cena-clima.html`: a cena de temporal pronta (fonte em `/private/tmp/claude-501/-Users-viniciusdelego-Documents-santainforma/0c959ae5-b969-4b71-8972-9a42f078e3ec/scratchpad/cena-clima-temporal.html`), com três ajustes: (a) remover a classe `.raro` e o CSS do clarão, o raio anima com `.pulsa` padrão; (b) renomear ids `tmp-*` para `cena-clima-*` (padrão de namespace de PRODUÇÃO, a matéria 08 prova que duas cenas coexistem numa página); (c) inserir os marcadores `{{ARIA_COMPLEMENTO}}` no fim do aria-label e `{{FIGCAPTION}}` na legenda.
- `cena-obras.html`: a cena de obras pronta (bloco do parecer), com id `obra-rolo` renomeado para `cena-obras-rolo` e os mesmos dois marcadores.
- `cena-marca.html`, `cena-poder.html`, `cena-legado-08a.html`, `cena-legado-08b.html`, `cena-legado-52.html`: as figuras existentes das matérias 04, 12, 08 e 52, copiadas sem alteração, só para o acervo não reprovar no validador. Hex antigos dessas cenas ficam congelados como paleta legada.

**Passo 2 · CSS aditivo em `estilo.css`** (bloco CENAS ANIMADAS, ~linha 371):

- Verbo `.gira` (3 linhas do parecer obras, com `transform-box:view-box`, obrigatório).
- Duas vírgulas: `.anima.pausada .gira` no seletor de pausa (linha 370) e `.anima .gira` no bloco de `prefers-reduced-motion` (linha 372).
- Nada mais. Nenhum token `--cena-*` novo: a proposta de tokens do motion fica rejeitada, a fonte única é o fragmento validado byte a byte, e cor via `color-mix` em atributo `style` já está provada em navegador nas duas cenas. O validador garante a paleta proibindo hex literal novo.

**Passo 3 · Rasters.** Renderizar localmente, uma vez, `imagens/cena-clima.jpg` e `imagens/cena-obras.jpg` em 1200×675 (16:9, largura mínima do Google News, serve `og:image` e JSON-LD), JPEG ≤ 80 KB, no enquadramento da pose de repouso. Pôr `og:image` nas matérias 04, 08, 12 e 52 apontando para os `ilustracao-mNN.jpg` que já existem. A nuvem nunca rasteriza (Pillow não lê SVG); raster novo só nasce local, junto com fragmento novo.

**Passo 4 · `ferramentas/aplica-cena.py`.** `--materia NN --tema clima`: imprime o bloco `figure` do fragmento no stdout e gera `imagens/miniaturas/mNN-card.jpg` (720×405) e `mNN-mini.jpg` (160×160) recortando `imagens/cena-<tema>.jpg`, reusando o corte do `foto-oficial.py`.

**Passo 5 · `ferramentas/cenas/TEMAS.md`.** Tabela determinística de PRODUÇÃO (palavra-chave do assunto primeiro, editoria depois, `cena-marca` como resto) mais a lista fechada de gatilhos lexicais de sobriedade do motion (morte, vítima, afogamento, feminicídio, acidente fatal etc.): um gatilho no título ou linha fina proíbe cena animada.

**Passo 6 · Validador em `checa-site.py`.** A função `checa_cenas` de PRODUÇÃO entra como está (núcleo byte-idêntico ao cânone, `role="img"`, aria-label ≥ 40 caracteres, `aria-hidden` nas camadas, crédito "Ilustração animada: Santa Informa" ou "Ilustração" nas legado, ids sem colisão, `visual.js` presente, `og:image` raster existente em disco), com três checagens a mais:

- SVG da cena acima de 8 KB cru: reprova.
- Orçamento de textura: máximo 4 camadas animadas por cena, e a soma de `2 × (altura do viewBox da faixa .corre / 525)` mais 1 por camada animada não-corre não pode passar de 4 quadros-equivalentes (~7 MB de GPU num 360px DPR 2,75). A cena clima fecha em ~3,5 e passa; é esta regra que substitui o "máximo 1 corre".
- Gatilho lexical de sobriedade no `<title>`/linha fina de página com `class="anima"`: reprova.

Fora do laço, a sentinela: reprovar se `estilo.css` perder a linha de reduced-motion das cenas ou o `.pausa-anima{display:none}`.

**Passo 7 · `ensaio-geral.py`.** Caso novo: rodar `aplica-cena.py` em cada tema disponível numa matéria de teste e conferir que a saída passa no próprio `checa-site.py`. Defeito de fragmento nunca chega à nuvem.

**Passo 8 · `prompt-agente-noticias.md`.** Texto da seção 4 abaixo.

Pendência anotada fora deste projeto: nenhuma matéria do site tem `og:image` hoje. Estender a checagem a todas as matérias é tarefa separada e independente, e é buraco de Discover.

## 3. FASE 2 · Catálogo e ordem de produção

Onze temas mais a marca. Feitos: clima-temporal, obras, marca (m04), poder (m12, versão básica). Ordem de produção das restantes, por frequência real de pauta no acervo de 59 matérias:

1. **Economia** (Selic, Simples, abono, Pix, inflação: a editoria mais órfã de foto honesta). Skyline-gráfico do motion, barras em `sobe` defasado, linha estática, ponto final em `pulsa` virando o traço de onda.
2. **Poder público v2** (refresh da cena 12: porta acesa estática em `--sol` 20%, bandeira em rotate ±2°/11 s, novo verbo não precisa, usa `gira` com duração inline).
3. **Saúde** (ritmo pela metade, `pulsa` de 9 s, coral proibido no tema).
4. **Educação** (janelas com verbo novo `acende`, pipa em `sobe`+rotate).
5. **Praia/turismo** (m04 mais guarda-sóis e veleiro em 60 s).
6. **Esporte** (bola em verbo novo `quica`, cena mais rápida da casa).
7. **Cultura** (bandeirinhas em `sobe` escalonado, estrelas em `pulsa` com durações que não se dividem).
8. **Segurança** (farol, facho ±14° em 30 s via `gira`; só pauta preventiva, ocorrência com pessoa cai na sobriedade).
9. **Clima-frio** (variante: céu invertido, fumaça em `sobe`).

Regras de produção herdadas do motion, agora normativas: três faixas de velocidade (maré 30-60 s, corrente 14-24 s, espuma 7-12 s, uma camada de espuma por cena), pulsos de opacidade entre 6 e 9 s, delays negativos ímpares, durações que não se dividem, amplitude vertical ≤ 2,5%, rotação ≤ ±4° (facho ±14° é exceção nomeada), pose de repouso sempre ilustração completa, assinatura mínima de dois entre sol/onda/traço 1.7, onda na base inegociável em todo tema. Cada verbo novo (`cai`, `quica`, `acende`) entra no `estilo.css` no commit da cena que o usa: 3 linhas mais as duas vírgulas de pausa e reduced-motion, nunca antes.

Também na Fase 2, dois enhancements de plataforma: as classes `.paralaxe-1..3` (amplitudes 3/7/12%, sangria desenhada igual à amplitude, dentro de `@supports (animation-timeline:view())`, incluídas no bloco de reduced-motion) aplicadas primeiro nas cenas de praia e obras; e ~10 linhas no `visual.js`, no bloco do botão de pausa, um IntersectionObserver com `rootMargin:'25%'` alternando `.pausada` fora do viewport, respeitando o estado manual do botão.

## 4. REGRAS PARA O CICLO (texto final, substitui a linha "copie o padrão das matérias 04 e 12" na seção 4 do `prompt-agente-noticias.md`)

> **Cena temática no lugar de desenhar SVG.** Quando a escolha de imagem cair na ilustração (sem foto própria, sem divulgação oficial e sem foto de banco que ilustre o assunto específico com honestidade), você NÃO desenha nada e NÃO edita geometria. Regra de decisão: assunto fotografável (praia, obra, geada, ginásio) tende a ter foto ilustrativa honesta, foto vence; ato abstrato (votação, lei, prazo, edital, índice, alerta) pede cena, porque foto de banco sugeriria documentar o que não documenta. Empate: cena.
>
> Antes de qualquer cena, confira os gatilhos de sobriedade em `ferramentas/cenas/TEMAS.md` contra o título e a linha fina. Um gatilho presente (morte, vítima, afogamento e os demais da lista) proíbe cena animada: use a ilustração estática da marca ou nenhuma figura, e crime contra pessoa não ganha cena figurativa nenhuma. Na dúvida, estática, mesma lógica do "na dúvida, não publica".
>
> Passando na sobriedade: escolha o tema pela tabela de `TEMAS.md` (palavra-chave do assunto primeiro, editoria depois, `cena-marca` se nada servir) e rode `python3 ferramentas/aplica-cena.py --materia NN --tema <tema>`. Cole o bloco `figure` impresso e preencha só os dois marcadores: o complemento do aria-label e a figcaption, que sempre declara que é ilustração e não retrata o local real, com o crédito "Ilustração animada: Santa Informa". A geometria, as classes e as durações não se tocam: o `checa-site.py` reprova cena que não bate com o fragmento canônico de `ferramentas/cenas/`. No `og:image` e no `image` do JSON-LD entra `imagens/cena-<tema>.jpg`, que já existe no repositório; as miniaturas mNN o próprio `aplica-cena.py` gera. Nunca declare imagem que não está no disco, e nunca gere raster na nuvem.

## 5. O QUE SEGUE VETADO

WebGL e `<canvas>` em matéria e na home (o shader de `proposta/07` segue confinado a página especial futura). `requestAnimationFrame` permanente, timer visual, listener de scroll/pointer para efeito. Qualquer biblioteca ou polyfill, zero bytes de JS além do IO da Fase 2. SMIL, GIF/APNG, vídeo decorativo, iframe. Animar propriedade fora de transform/opacity, animar variável CSS, `will-change` fora das camadas animadas. `perspective`, `preserve-3d`, `translateZ` (desenhar perspectiva dentro do SVG é permitido e incentivado). `content-visibility` no sistema. Relâmpago, flash claro sobre escuro, ciclo de opacidade menor que 3 s. Mais de uma cena por página, cena fora de `figure.foto`, cena convivendo com foto. Animação de entrada por opacity em h1, linha fina ou primeiro parágrafo de matéria com cena (protege o LCP de texto, que com SVG inline cai no título e fica mais rápido que foto). Publicar cena sem aria-label, crédito, raster e aprovação do editor.

**Frase para o editor:** "3D real" (WebGL) num portal de notícias briga por GPU e bateria com o AdSense no mesmo celular de 4G que paga o site, adiciona centenas de KB de biblioteca que a Constituição proíbe, e quebra em parte dos aparelhos; o que o leitor percebe como profundidade numa faixa de 1200×525 é sobreposição, escala e camadas em velocidades diferentes, e isso a gente entrega com SVG de 4 KB que chega junto com o HTML, roda no compositor sem custar um milissegundo de Web Vitals, para sozinho para quem pediu menos movimento e degrada para uma ilustração completa; é o mesmo truque de multiplane do cinema de animação clássico, e o cinema nunca precisou de Three.js.

**Arquivos tocados na Fase 1:** `ferramentas/cenas/` (novo, 7 fragmentos), `ferramentas/aplica-cena.py` (novo), `ferramentas/cenas/TEMAS.md` (novo), `estilo.css` (verbo `.gira` mais duas vírgulas), `ferramentas/checa-site.py` (função `checa_cenas` mais sentinela), `ferramentas/ensaio-geral.py` (caso novo), `ferramentas/prompt-agente-noticias.md` (seção 4), `imagens/cena-clima.jpg` e `cena-obras.jpg` (novos), matérias 04, 08, 12 e 52 (só `og:image`).

---

# Estudos de viabilidade

ENVELOPE TÉCNICO · SISTEMA DE CENAS TEMÁTICAS PSEUDO-3D

Base examinada: `.anima` em `/Users/viniciusdelego/Documents/santainforma/estilo.css` (linhas 353-374), cenas reais nas matérias 04 (1,4 KB de figura inline) e 12 (2,2 KB), botão de pausa e infra de IntersectionObserver em `/Users/viniciusdelego/Documents/santainforma/visual.js` (linhas 244-260 e 81-97), padrão `@supports (animation-timeline:...)` já usado nas linhas 48, 564 e 705 do CSS, orçamentos herdados de `/Users/viniciusdelego/Documents/santainforma/proposta/03-restricoes-de-performance.md`.

---

**1) TÉCNICA BASE: parallax de velocidades por scroll-driven animation. Perspective real está descartada.**

Comparação honesta das duas abordagens de profundidade:

Perspective real (`perspective` no contêiner + `transform-style:preserve-3d` + `translateZ` negativo com `scale` compensatório):
- Incompatível com o sistema atual por construção: `.anima` tem `overflow:hidden` (obrigatório, a camada `.corre` tem 200% de largura), e overflow com clipping força *flattening* do contexto 3D. Ou se abre mão do clip, ou do 3D. Não há terceira opção na spec.
- Parallax por perspective só se move com a rolagem se o próprio scroller tiver a perspective (técnica do scroller aninhado). Em matéria isso significa transformar `main` ou a figura num scroller próprio: quebra barra de endereço móvel, quebra `position:fixed` (a barra `.progresso`), quebra medição de viewability do AdSense. Vetado.
- `preserve-3d` promove cada plano a camada permanente de GPU mesmo parado, e o Safari acumula bugs históricos de clipping com preserve-3d. Custo de memória igual ou pior que o parallax 2D, com superfície de bug maior.
- Ganho visual sobre o parallax de velocidades: nenhum que o leitor perceba numa faixa 16/7. Perspective real só compensa quando há rotação em Y/X, que numa figura de matéria vira ruído.

Parallax de velocidades (camadas 2D, cada uma com `translateY` de amplitude diferente, dirigidas por `animation-timeline: view()`):
- Roda 100% no compositor, mesmo pipeline dos `.corre/.pulsa/.sobe` atuais. Zero JS, zero listener de scroll.
- Encaixa no padrão progressivo que o site já pratica: `@supports (animation-timeline:scroll())` na linha 48 e `view()` na 705. Onde não existe (Firefox ainda atrás de flag no início de 2026), a cena degrada para o que existe hoje: loops de tempo, que funcionam em todo navegador. Chrome/Edge 115+ e Safari 26+ cobrem a esmagadora maioria do leitor 4G de celular.
- Profundidade desenhada + profundidade de movimento: o SVG já desenha perspectiva (horizonte, sobreposição, escala decrescente das matérias 04/12); o parallax só precisa confirmar a ilusão com 3 velocidades.

DECISÃO: SVG inline em camadas, profundidade por sobreposição desenhada, movimento ambiente pelos loops existentes (`.corre`, `.pulsa`, `.sobe`) e profundidade cinética por três novas classes de parallax no `estilo.css`:

```css
.anima .paralaxe-1{--amp:3%}  /* fundo: céu, morro distante */
.anima .paralaxe-2{--amp:7%}  /* meio: prédio, mar, objeto-tema */
.anima .paralaxe-3{--amp:12%} /* frente: vegetação, espuma, moldura */
@supports (animation-timeline:view()){
  .anima [class*=paralaxe]{will-change:transform;animation:paralaxe linear both;
    animation-timeline:view();animation-range:entry 0% exit 100%}
}
@keyframes paralaxe{from{transform:translate3d(0,calc(var(--amp)),0)}to{transform:translate3d(0,calc(-1*var(--amp)),0)}}
```

Cada camada precisa de sangria vertical desenhada igual à amplitude (a camada é mais alta que o quadro), senão aparece borda. Isso é regra de template, não de CSS.

`perspective`/`preserve-3d`/`translateZ` ficam proibidos no CSS do sistema. "3D" aqui é vocabulário de desenho e de velocidade, não de matriz.

---

**2) ORÇAMENTO DURO POR CENA**

- **Peso:** SVG inline da cena ≤ 8 KB sem compressão (alvo 3-5 KB; as cenas atuais têm 1,4-2,2 KB, então 8 KB já é generoso). Teto absoluto 12 KB, acima disso a cena é recusada pela validação. O HTML inteiro da matéria continua sob os 35 KB do parecer 03.
- **Camadas animadas:** máximo 4 elementos com animação por cena (soma de loops + parallax), das quais no máximo 1 `.corre` (largura 200% dobra a textura de GPU). Camadas estáticas do desenho não contam, não são promovidas. Aritmética que justifica: textura ≈ largura×altura×DPR²×4 bytes; num celular 360px de largura, faixa 16/7 (157px), DPR 2,75 → ~1,7 MB por camada, ~3,4 MB para a `.corre`. Com 4 camadas o teto fica em ~8-12 MB de GPU, conviável com os iframes do AdSense. `will-change` só nessas camadas, nunca no contêiner.
- **Propriedades:** só `transform` e `opacity`. Proibido animar filter, clip-path, mask, stroke-dashoffset em loop, atributos de geometria SVG, variáveis CSS (invalidam estilo em cascata) e qualquer propriedade de paint/layout. SMIL (`<animate>` dentro do SVG) proibido: ignora `.pausada`, ignora o bloco de reduced-motion e roda fora do controle do sistema.
- **Ritmo:** nenhuma animação em loop com duração menor que 6 s (as atuais: 6, 9 e 20 s). Alvo de quadro: 60 fps de compositor com **0 ms de main thread atribuível à cena** no trace; essa é a métrica de aceitação, não "fps médio".
- **prefers-reduced-motion:** já resolvido pelo bloco da linha 371 e pelo global da 494; obrigação nova é incluir `[class*=paralaxe]` no mesmo bloco (`animation:none;transform:none`). Regra de desenho decorrente: **o quadro estático da cena precisa ser uma ilustração completa e correta**. A cena parada é o produto; o movimento é enfeite. Isso também cobre navegador antigo.
- **Aba oculta:** nada a fazer. CSS animation em camada composta não produz frame com a aba oculta, o navegador suprime o compositing. Documentar e não adicionar JS.
- **Fora do viewport:** `content-visibility` fica fora do sistema inteiro (regra dada, e o custo de bug em alvo de âncora não paga o ganho). O parallax por `view()` já é inerte fora da viewport por definição. Para os loops de tempo, ~10 linhas no `visual.js`, no bloco que já cria o botão de pausa (linha 244): um IntersectionObserver com `rootMargin:'25%'` que alterna a classe `.pausada` existente (que já aplica `animation-play-state:paused`), respeitando o estado manual do botão (se o leitor pausou, o IO não retoma). Sem IO disponível, comportamento atual (loops rodam), que é o fallback aceitável.

---

**3) ONDE A CENA MORA E O CONTRATO DE LCP**

- **Lugar:** exatamente a estrutura da matéria 12: `figure.foto > div.anima[role=img][aria-label] > svg.fundo` + `figcaption` com "Ilustração animada: Santa Informa". Uma cena por página, sempre e somente como figura de topo. Nunca em card, lista, rio ou home.
- **Quando substitui a foto:** a cena é a versão animada do degrau 4 da hierarquia de imagem do CLAUDE.md (ilustração SVG da marca). Entra somente quando não há foto honesta (própria, divulgação identificada) e o Pexels seria desonesto ou redundante. Foto real disponível vence a cena, sempre. A figcaption nunca pode sugerir que a cena documenta o fato (a da matéria 12 é o modelo de redação).
- **LCP:** SVG inline **não é candidato a LCP** (a spec só considera `<img>`, `<image>` dentro de SVG, poster de vídeo, background por `url()` e blocos de texto). Com cena no topo, o LCP cai para o maior bloco de texto, tipicamente o `h1`, que pinta com HTML+CSS, sem esperar imagem nenhuma na rede. Em 4G isso costuma ser **melhor** que os ~80 ms por 100 KB de uma foto LCP. Duas condições para esse ganho existir: o título e a linha fina do template de matéria jamais recebem animação de entrada por opacity (senão o LCP escorrega para o fim do fade), e a cena mantém `aspect-ratio:16/7` no contêiner, que já garante CLS zero por construção.
- **fetchpriority:** não se aplica, não há fetch; a regra operacional é a inversa: matéria com cena não pode carregar nenhum resquício de `<img fetchpriority=high>` do template de foto.
- **og:image raster:** obrigatório e já tem precedente (`/Users/viniciusdelego/Documents/santainforma/imagens/ilustracao-m04.jpg`, 21 KB; `ilustracao-m12.jpg`, 28 KB). Contrato: cada um dos 10 temas ganha um pôster raster 1200×630 exportado do quadro estático da cena, JPEG ≤ 60 KB, gerado por script em `ferramentas/` (o script resolve as variáveis de cor para hex na exportação), salvo em `imagens/` e referenciado no `og:image` e no campo `image` do JSON-LD (Google News exige raster). O agente da nuvem nunca gera raster na hora: ele escolhe o pôster do tema, pronto no repositório.
- **Cor:** para respeitar "nenhum hex novo", os fills das cenas novas usam `style="fill:var(--sol)"` ou `color-mix(...)` em atributo style (SVG inline herda custom properties). As cenas 04/12 usam hex literais da paleta e tons antigos (`#0E3646`, `#0A2A37`, `#16536A`); esses tons ficam congelados como legado, cena nova não cria hex.

---

**4) PROIBIÇÕES EXPLÍCITAS (lista fechada, para o validador e para o prompt do agente)**

1. WebGL e `<canvas>` em template de matéria e na home, em qualquer tamanho (o parecer do shader em `proposta/07-especialista-webgl-glsl.md` segue confinado a página especial futura, fora deste sistema).
2. `requestAnimationFrame` permanente, `setInterval`/`setTimeout` visual, listener de `scroll`/`pointermove` para efeito. Parallax por JS é jank garantido em celular intermediário.
3. Biblioteca de qualquer espécie: Three, GSAP, Lottie, anime.js, polyfill de scroll-timeline. Zero bytes novos de JS além das ~10 linhas do IO no `visual.js`.
4. SMIL, GIF/APNG animado, `<video>` decorativo, iframe de animação.
5. Animar propriedade fora de transform/opacity; `will-change` fora das camadas animadas; animar variável CSS.
6. `perspective`, `transform-style:preserve-3d`, `translateZ` como mecanismo (desenhar perspectiva dentro do SVG é permitido e incentivado).
7. `content-visibility` em qualquer parte do sistema de cenas.
8. Mais de uma cena por página; cena fora de `figure.foto`; cena convivendo com foto na mesma figura.
9. Animação de entrada por opacity em `h1`, linha fina ou primeiro parágrafo de matéria com cena (protege o LCP de texto).
10. Publicar cena sem: `role="img"` + `aria-label` descritivo, figcaption com crédito "Ilustração animada: Santa Informa", pôster raster do tema no `og:image` e no JSON-LD, e aprovação do editor (Regra 2 do CLAUDE.md, inalterada).

Operabilidade pelo agente da nuvem (requisito do ciclo): o sistema se entrega como 10 templates de cena por tema (arquivos parciais versionados, um por editoria), cada um já dentro do orçamento, com camadas nomeadas pelas classes fixas (`corre|pulsa|sobe|paralaxe-1..3`); o agente escolhe tema, não desenha do zero. Um validador em `ferramentas/` (a criar) recusa: peso acima do teto, mais de 4 camadas animadas, hex fora da paleta legada, presença de `<animate>`, `<script>`, `<image href>` externo, ausência de aria-label ou de pôster correspondente em `imagens/`. Sem passar no validador, a cena não entra no HTML.

---

CATÁLOGO, GRAMÁTICA E REGRAS DA LINGUAGEM DE MOVIMENTO · Diretor de Motion

Base verificada no código: o sistema `.anima` (estilo.css 353-374) já dá três verbos (`corre` 20s translateX em tile de 200%, `pulsa` 6s opacity, `sobe` 9s translateY -2.5%), botão de pausa automático via visual.js (linhas 242-260) e corte total em `prefers-reduced-motion`. As cenas canônicas são a estática da matéria 04 (viewBox 1200×260, sol r46, dois planos de morro, faixa de mar com traço de onda stroke 2.4) e a animada da matéria 12 (fachada institucional, sol `pulsa`). Tudo abaixo estende isso, não substitui.

---

**0. TOKENS DE COR DE CENA (entra uma vez no estilo.css, vira vocabulário fechado)**

As matérias 04 e 12 hard-codam misturas (#16536A, #0E3646, #0A2A37, #0A2530). Novas cenas usam cinco tokens, e o agente da nuvem nunca inventa mistura:

- `--cena-ceu-alto: var(--breu)`
- `--cena-ceu-baixo: color-mix(in srgb, var(--mar) 82%, var(--espuma) 18%)`
- `--cena-morro-1: color-mix(in srgb, var(--mar) 72%, var(--breu) 28%)`
- `--cena-morro-2: color-mix(in srgb, var(--mar) 45%, var(--breu) 55%)`
- `--cena-recorte: color-mix(in srgb, var(--mar) 30%, var(--breu) 70%)`

Acentos: só `--sol`, `--coral`, `--areia`, `--espuma`, `--mar-claro` puros. Coral é raro por natureza: um ponto focal por cena, no máximo.

---

**1. CATÁLOGO POR TEMA**

Estrutura fixa de toda cena, em slots: CÉU, SOL, FUNDO (morros ou skyline), MEIO, FRENTE, ÁGUA+ONDA na base. O tema troca o miolo, a moldura é sempre a mesma. Estética das matérias 04 e 12: geométrica, flat, profundidade só por sobreposição, sem rosto, sem personagem.

**Clima-temporal.** Céu quase breu (`--cena-recorte` no topo), duas camadas de nuvens compridas em `corre`, a de trás em maré (45s), a da frente em corrente (18s), sentidos iguais. Chuva como grupos de traços diagonais 1.7 em `--mar-claro` a 45%, descendo em loop vertical (verbo novo `cai`); o mar da base ganha traço de onda mais crespo no desenho, não na animação. Personalidade: a única cena sem o sol em quadro; no lugar, uma fresta estática de `--sol` a 20% atrás da nuvem maior. Relâmpago é proibido, sem exceção (fotossensibilidade, seção 2).

**Clima-frio.** Céu invertido: `--espuma` no topo descendo para `--mar-claro`, morros em `--cena-morro-1` bem recortados (ar seco). Sol presente mas pálido: opacity .55, sem halo, `pulsa` em 9s em vez de 6s. Três traços horizontais de vento 1.7 em `--mar-claro` cruzando em corrente (16s); fumaça de chaminés dos telhados geométricos subindo com `sobe` defasado. Personalidade: a fumaça, sinal de casa habitada no frio.

**Obras.** Skyline em dois planos (`--cena-morro-1` e `--cena-morro-2` viram prédios), grua em traço 1.7 `--espuma` com a lança girando ±4 graus em maré (30s, transform-origin no eixo). Tapume listrado `--sol`/`--breu` estático na frente. Personalidade: luz de topo da grua em `--coral` com `pulsa` lento de 6s, o único coral da cena. Base: faixa de mar com onda, porque obra em Itapema termina na praia.

**Economia.** O skyline é o gráfico: barras de prédio em alturas crescentes (`--cena-morro-2`), linha 1.7 em `--sol` ligando os topos, estática e completa (dashoffset anima pintura, vetado). O movimento fica nas barras, `sobe` com amplitude 2% e delays defasados, respiração de cidade. Personalidade: o último ponto da linha é um círculo `--sol` com `pulsa`, e a linha do gráfico desce e vira o próprio traço de onda da base. Nada de moeda, nada de cifrão.

**Poder público.** A cena da matéria 12 é o cânone: fachada com frontão e colunas em `--cena-recorte`, sol `pulsa`, água na base. Acrescentar: porta com retângulo `--sol` a 20% de opacity, estático (casa acesa, aberta ao público), e mastro com bandeira triangular geométrica balançando rotate ±2 graus em 11s. Personalidade: a porta acesa.

**Saúde.** Fachada baixa de posto em `--mar-claro` sobre `--cena-morro-1`, cruz do posto em `--espuma`. Todo o ritmo da cena cai pela metade: `pulsa` do halo da cruz em 9s, amplitude de `sobe` limitada a 1.2%. É a cena da respiração calma; urgência visual em pauta de saúde é alarmismo. Personalidade: o halo que respira. Coral proibido neste tema (coral sobre saúde lê sangue).

**Esporte.** Quadra de areia (`--areia`) em trapézio flat à beira d'água, rede em traços 1.7 `--espuma`, bola como círculo `--sol` com verbo novo `quica` (translateY 3%, cubic-bezier de queda, 2.6s). É a cena mais rápida da casa: frente em espuma (7s). Personalidade: a bola é o próprio sol da marca em serviço, e ninguém a chuta (sem personagens, ela quica sozinha).

**Turismo-praia.** A matéria 04 animada: morros em dois planos, sol `pulsa`, mar com quatro traços de onda. Acrescentar faixa de `--areia` com guarda-sóis em semicírculos (`--coral`, `--sol`, `--mar-claro`) estáticos, e um veleiro triângulo `--espuma` atravessando o horizonte inteiro em maré de 60s. Personalidade: o veleiro é recompensa de leitura lenta, quem ficou na página o vê chegar do outro lado.

**Cultura.** Céu noturno `--breu` com pontos `--espuma` em `pulsa` defasado e durações que não se dividem (nunca piscam juntos). Cordão de bandeirinhas triangulares (`--sol`, `--coral`, `--mar-claro`, `--espuma`) entre dois mastros, cada bandeirinha em `sobe` com delay escalonado de -1.3s, onda de vento percorrendo o cordão. Personalidade: um cone de holofote `--sol` a 12%, estático, saindo de baixo. Sem nota musical, sem máscara de teatro.

**Educação.** Fachada de escola em `--cena-morro-1` com janelas que acendem (verbo novo `acende`, opacity 0→.25 em `--sol`, degraus defasados, ciclo de 13s). No céu, uma pipa: losango `--sol` com rabiola em traço 1.7 `--coral`, em `sobe` mais rotate ±3 graus, 9s. Personalidade: a pipa diz infância sem colocar criança em quadro, que é proibido.

**Segurança.** Farol: torre listrada `--espuma`/`--cena-morro-1` sobre pedra, facho como triângulo `--sol` a 15% varrendo ±14 graus em maré de 30s (transform-origin na lanterna). Sem viatura, sem arma, sem sirene, sem pisca. Personalidade: segurança como farol que orienta, não como ameaça. Esta cena só vale para pauta preventiva (campanha, balanço, operação sem vítima); qualquer ocorrência com pessoa envolvida cai na regra da seção 3.

---

**2. GRAMÁTICA DE MOVIMENTO**

Três velocidades nomeadas, para deslocamento em loop:

- **Maré** (fundo): 30 a 60s. Horizonte, nuvens de trás, veleiro, facho, grua.
- **Corrente** (meio): 14 a 24s. O `corre` atual (20s) vive aqui. Nuvens da frente, vento.
- **Espuma** (frente): 7 a 12s. Bola, bandeirinha, chuva. Só um elemento por cena vive nesta faixa.

Pulsos de opacidade não são velocidade de viagem: ficam sempre entre 6 e 9s (`pulsa` atual é 6).

Regras duras:

- Só `transform` e `opacity`, como já escrito no comentário do estilo.css. Nada de dashoffset, filter, background-position, cores animadas.
- **Amplitude:** deslocamento vertical máximo de 2.5% da altura da cena (o `sobe` atual é o teto), escala máxima 1.03, rotação de elemento até ±4 graus (exceções nomeadas: facho ±14, por ser luz e não objeto). Loop horizontal só via tile de 200% de largura, emenda invisível.
- **Defasagem:** irmãos nunca em fase. `animation-delay` negativo em passos ímpares (-1.3s, -2.7s, -4.1s) e durações que não se dividem entre si (o sistema atual já faz 6, 9, 20; verbos novos em 7, 11, 13, 30, 45).
- **Orçamento por cena:** máximo 6 nós animados, máximo 4 com `will-change`, markup do SVG até 8 KB. Celular intermediário 4G é o leitor padrão.
- **Pose de repouso:** o estado 0% de todo keyframe é a ilustração completa e legível. É o frame que o leitor de reduced-motion e o botão de pausa recebem; a cena nunca depende do movimento para fazer sentido.
- **Fotossensibilidade:** nada completa ciclo de opacidade em menos de 3s, nunca flash claro sobre escuro, relâmpago proibido em qualquer tema.
- **Pseudo-3D:** profundidade primária é sobreposição mais razão de velocidade entre camadas, alvo 1 : 2.5 : 6 (fundo : meio : frente). `perspective` real só como enhancement de entrada: `perspective: 1100px` no `.anima` e um tilt único de acomodação, rotateX 2.5 graus → 0 em 900ms ease-out quando a cena entra no viewport (a classe pode vir do observer que já existe no visual.js). Tilt contínuo em loop está vetado: enjoa e vira slide corporativo. Scroll-driven como camada extra: dentro de `@supports (animation-timeline: view())`, fundo desliza -2% e frente +2% ao longo da passagem pelo viewport (contra-fase é o que produz profundidade); sem suporte, nada acontece e a cena segue íntegra. Tudo isso entra no bloco de `prefers-reduced-motion` existente (371-374), incluindo os verbos novos `cai`, `quica`, `acende` e o timeline de scroll.
- **Web Vitals:** `.anima` mantém `aspect-ratio` fixo (CLS zero), SVG inline sem request. Quando a cena é a figura de topo, o `og:image` e o `image` do JSON-LD continuam apontando para um JPG estático exportado da pose de repouso, porque Discover não consome SVG.

---

**3. SOBRIEDADE: QUANDO A CENA PARA**

Regra editorial, escrita para o agente da nuvem aplicar sem julgamento fino:

- **Gatilhos lexicais que forçam cena estática** (SVG sem classe `.anima`, formato da matéria 04): morte, morre, vítima, corpo, afogamento, ferido grave, desaparecido, feminicídio, estupro, violência sexual, acidente fatal, incêndio com feridos, homicídio, luto oficial, tragédia. Basta um gatilho no título ou na linha fina.
- **Em cena sóbria:** paleta restrita a `--breu`, `--mar`, `--mar-claro`, `--suave`, `--espuma`. Sem coral (sobre tragédia, coral grita sangue). Sol parado ou fora de quadro. Sem detalhe de personalidade, sem humor, sem o veleiro.
- **A cena nunca reencena o fato.** Matéria de afogamento não ganha mar animado; se o fato envolve o mar e há vítima, o mar não se move, ponto. Crime contra pessoa não ganha cena figurativa nenhuma: usa-se a ilustração abstrata da marca ou nenhuma figura.
- Pauta policial de rotina sem vítima identificável (apreensão, balanço, campanha) usa a cena do farol, mas com o facho parado. Prisão envolve pessoa: estática.
- Na dúvida, estática. É a mesma lógica do "na dúvida, não publica".

---

**4. ASSINATURA DA MARCA EM CENA**

Três assinantes, e toda cena carrega no mínimo dois:

- **O sol.** Círculo `--sol`, r 46 no viewBox de 1200, sempre no terço superior, opacity .92, verbo `pulsa`. É o logo em cena. Sai de quadro só no temporal (vira fresta) e nas sóbrias (para de pulsar ou sai).
- **A onda.** A inegociável. Toda cena, de qualquer tema, termina na base com a faixa d'água `--mar` e pelo menos dois traços de onda no desenho canônico da matéria 04 (`c22 0 22 6 44 6s22-6 44-6`), stroke `--mar-claro` a 38%, espessura 2.4 no viewBox 1200. Obras, Câmara, educação, tanto faz: o portal é do litoral e toda pauta acaba no mar. Na cena sóbria a onda fica, parada; ela é assinatura, não efeito.
- **O traço 1.7.** Todo contorno interno (rabiola, rede, vento, grua, farol) usa `stroke-linecap: round` e o peso do sprite da casa: 1.7 na escala dos ícones 24px, o que dá 2.4 na escala do viewBox 1200×260. Nada de traço fino de 1 nem grosso de 4; o arredondado é o que faz a cena parecer da mesma mão que desenhou os ícones e os raios do sol do cabeçalho.

**Operação pelo agente da nuvem:** o tema vira uma escolha de combinação pronta nos slots (CÉU, SOL, FUNDO, MEIO, FRENTE, ÁGUA+ONDA), com validação mecânica antes do commit: só tokens de cor da seção 0, só verbos do catálogo (`corre`, `pulsa`, `sobe`, `cai`, `quica`, `acende`), até 6 nós animados, `aria-label` descritivo no contêiner, gatilho lexical de sobriedade checado contra título e linha fina, pose de repouso legível. O botão de pausa e o corte de reduced-motion vêm de graça do visual.js e do estilo.css existentes.

Arquivos de referência: /Users/viniciusdelego/Documents/santainforma/estilo.css (linhas 353-374), /Users/viniciusdelego/Documents/santainforma/materia-04-audiencia-orcamento-2027.html (linhas 136-156), /Users/viniciusdelego/Documents/santainforma/materia-12-camara-itapema-pauta.html (linhas 135-160), /Users/viniciusdelego/Documents/santainforma/visual.js (linhas 242-260).

---

PARECER DE ENGENHARIA DE PRODUÇÃO · Cenas temáticas no ciclo automático

Fatos verificados no código antes de decidir: hoje existem dois padrões de cena no ar. Estático: `svg.cena` com `role="img"` e `aria-label` direto dentro de `figure.foto` (matérias 04 e 52). Animado: `div.anima` com camadas `.fundo`/`.corre`/`.pulsa`/`.sobe`, os SVGs internos com `aria-hidden="true"` (matérias 08 e 12). O CSS está em `estilo.css` linhas 353 a 374, com pausa via classe `.pausada` e reduced-motion que congela tudo e esconde o botão. O botão de pausa é injetado por `visual.js` (linhas 244 a 261) em todo `.anima` via `fig.appendChild`, nada por página. O bloco `figure` inteiro pesa 1,4 KB (m04) e 2,2 KB (m12) crus; a matéria 12 completa comprime para 7,6 KB gzip. Nenhuma matéria do site tem `og:image` hoje, nenhuma. O raster da cena para o JSON-LD existe como `imagens/ilustracao-m04.jpg`, `-m12.jpg`, `-m52.jpg`, feitos fora do ciclo. O `checa-site.py` já valida existência em disco das imagens do JSON-LD, mas ignora completamente cenas.

---

**1. FORMATO DE ENTREGA: inline por matéria, copiado verbatim de fragmentos canônicos em `ferramentas/cenas/`**

Comparação honesta das três opções:

**(a) `cenas.svg` compartilhado com `<symbol>` + `<use href="cenas.svg#tema">`.** Rejeitado por um fato técnico que mata a opção sozinho: o conteúdo clonado por `<use>` externo vive numa shadow tree fechada que os seletores de `estilo.css` não alcançam. `.anima .corre`, `.anima.pausada .corre` e o bloco de `prefers-reduced-motion` simplesmente param de funcionar; todo o sistema de animação e de pausa teria de migrar para `<style>` dentro do próprio SVG, com controle de pausa por variável CSS herdada, uma gambiarra frágil que duplica a lógica que já existe. Além disso a busca do arquivo externo não é vista pelo preload scanner: a figura de topo é candidata a LCP, e leitor de Discover chega em visita única no 4G, então o cache entre matérias que seria a única vantagem quase nunca se realiza. E 10 temas num arquivo só significa baixar 20 KB para usar 2.

**(b) Inline completo desenhado pelo agente a cada matéria (status quo do prompt: "copie o padrão das matérias 04 e 12").** É o que existe e é o risco maior do sistema: convida o agente a "criar" geometria nova a cada execução. Deriva visual, IDs de gradiente colidindo, camada sem `aria-hidden`, aspect-ratio errado, e nenhuma validação consegue reprovar o que não tem referência.

**(c) ESCOLHIDO: inline por matéria, mas com fonte única.** Diretório novo `ferramentas/cenas/`, um arquivo por tema (`cena-clima.html`, `cena-obras.html`, `cena-economia.html`, `cena-poder.html`, `cena-saude.html`, `cena-esporte.html`, `cena-praia.html`, `cena-cultura.html`, `cena-educacao.html`, `cena-seguranca.html`, `cena-marca.html` como genérica). Cada arquivo é o bloco `<figure class="foto">…</figure>` completo e pronto: `div.anima` com `role="img"`, camadas com `aria-hidden="true"`, IDs de gradiente com namespace do tema (`id="cena-clima-ceu"`, nunca `id="cena-ceu"` genérico, porque a matéria 08 prova que duas cenas podem coexistir numa página), e dois marcadores de edição: `{{ARIA_COMPLEMENTO}}` no fim do `aria-label` e `{{FIGCAPTION}}` na legenda. O agente copia o arquivo inteiro, preenche os dois marcadores, e não toca em mais nada. Peso: 2 KB crus por matéria, que somem no gzip da página (a página inteira comprime para 7,6 KB); zero requisição extra; zero CLS porque `.anima` tem `aspect-ratio:16/7` reservando espaço; anima só `transform` e `opacity` no compositor, como hoje. A "profundidade" pedida pelo editor (parallax de camadas, `perspective`, scroll-driven) entra dentro dos fragmentos e das regras aprovadas em `estilo.css` uma vez, pelo editor, e nunca é decisão do agente da nuvem.

**Rasters: pré-renderizados uma vez, nunca gerados na nuvem.** A nuvem tem Pillow, que não rasteriza SVG, e é por isso que `ilustracao-mNN.jpg` hoje nasce fora do ciclo. Solução: renderizar localmente, uma única vez, um raster 1600x900 por tema (`imagens/cena-clima.jpg` etc.), no mesmo enquadramento da cena, e commitar. Ferramenta nova `ferramentas/aplica-cena.py --materia NN --tema clima` que (1) imprime no stdout o bloco `figure` já preenchível e (2) gera `imagens/miniaturas/mNN-card.jpg` (720x405) e `mNN-mini.jpg` (160x160) a partir do raster do tema, reaproveitando o código de corte que já existe em `foto-oficial.py`. O JSON-LD e o `og:image` da matéria apontam para `imagens/cena-<tema>.jpg`. Perde-se o raster único por matéria; ganha-se um ciclo que nunca falha por falta de rasterizador. Reuso de imagem entre matérias do mesmo tema é honesto: é ilustração de marca declarada, não registro de fato.

---

**2. REGRA DE DECISÃO DO AGENTE**

A ordem da Constituição não muda: foto própria, depois divulgação oficial, depois Pexels ilustrativa, depois ilustração. A cena temática é o degrau 4 refinado, não um atalho para pular o Pexels. Regra mecânica para o degrau 3 vs 4, porque "sem foto honesta" é vago demais para agente:

- **Assunto é coisa ou lugar fotografável** (praia, obra, estrada, geada, ginásio, feira): Pexels tende a ter imagem ilustrativa honesta. Foto vence.
- **Assunto é ato abstrato** (votação, lei, prazo, edital, inscrição, orçamento, alerta em vigor, regra nova, índice econômico): foto de banco genérica sugere documentar o que não documenta, que é proibição expressa do CLAUDE.md. Cena vence.
- Empate ou dúvida: cena, que é "a saída mais segura" já registrada nas regras.

**Escolha do tema: assunto primeiro, editoria depois.** Tabela determinística em `ferramentas/cenas/TEMAS.md`, consultada nesta ordem:

1. Palavra-chave do assunto: temporal/chuva/vendaval/frio/geada → clima; obra/pavimentação/emissário/alargamento/BR-101 → obras; Selic/imposto/Simples/Pix/preço/abono → economia; Câmara/projeto de lei/audiência/TCE/prefeitura decide → poder; vacina/UBS/carreta/obesidade/TEA → saude; campeonato/JASC/surfe/pedala → esporte; temporada/turista/atração/mirante → praia; oficina/banda/artista/desfile → cultura; escola/curso/professor/feira do conhecimento → educacao; lei seca/PM/violência/blitz → seguranca.
2. Sem palavra-chave que decida: a editoria decide (Poder Público → poder, Economia → economia, Infraestrutura → obras, Turismo → praia, Meio Ambiente → clima, Santa Catarina → o assunto manda, senão marca).
3. Nada serviu: `cena-marca.html`, o horizonte ao amanhecer da matéria 04, que é a identidade do portal e nunca é mentira.

A legenda sempre declara o que é: modelo da matéria 12, "a cena representa X, sem retratar o local real", crédito `Ilustração animada: Santa Informa`.

---

**3. O CONTRATO NO `prompt-agente-noticias.md`** (entra na seção 4, substituindo a linha "a ilustração SVG da marca, copiando o padrão das matérias 04 e 12"):

> **Cena temática no lugar de desenhar SVG.** Quando a escolha cair na ilustração (sem foto própria, sem divulgação oficial e sem foto de banco que ilustre o assunto específico com honestidade; ato abstrato como votação, prazo, edital ou índice pede cena, não banco), você NÃO desenha nada. Escolha o tema pela tabela de `ferramentas/cenas/TEMAS.md` (palavra-chave do assunto primeiro, editoria depois) e rode `python3 ferramentas/aplica-cena.py --materia NN --tema <tema>`. Cole o bloco `figure` que ele imprime e preencha só os dois marcadores: o complemento do aria-label e a figcaption, que sempre declara que é ilustração e não retrata o local real. A geometria do SVG não se toca: o `checa-site.py` reprova cena que não bate byte a byte com o fragmento canônico. Se nenhum tema servir, use `cena-marca`. No JSON-LD e no og:image entra `imagens/cena-<tema>.jpg`, que já existe no repositório; as miniaturas mNN-card e mNN-mini o próprio aplica-cena.py gera. Nunca declare imagem que não está no disco.

---

**4. VALIDAÇÃO NO `checa-site.py`**

Função nova, chamada dentro do laço por página quando `class="anima"` ou `class="cena"` aparece no HTML. O teste central é o de integridade canônica, que transforma "o agente não pode inventar geometria" de instrução em trava:

```python
CENAS_DIR = os.path.join(BASE, 'ferramentas', 'cenas')

def _nucleo(fragmento):
    """Geometria da cena sem as partes que a materia pode editar."""
    n = re.sub(r'aria-label="[^"]*"', '', fragmento)
    n = re.sub(r'<figcaption>.*?</figcaption>', '', n, flags=re.S)
    return re.sub(r'\s+', '', n)

def checa_cenas(f, s, e):
    figs = re.findall(r'<figure class="foto">.*?</figure>', s, re.S)
    cenas = [g for g in figs if 'class="anima"' in g or 'class="cena"' in g]
    if not cenas:
        return
    canonicos = {_nucleo(open(c, encoding='utf-8').read())
                 for c in glob.glob(os.path.join(CENAS_DIR, 'cena-*.html'))}
    for g in cenas:
        # 1. geometria identica a um fragmento canonico
        if _nucleo(g) not in canonicos:
            e('cena com geometria fora do canone de ferramentas/cenas/')
        # 2. acessibilidade: raiz descreve, camadas somem do leitor de tela
        raiz = re.search(r'<(?:div class="anima"|svg class="cena")[^>]*>', g).group(0)
        if 'role="img"' not in raiz: e('cena sem role="img"')
        alt = re.search(r'aria-label="([^"]*)"', raiz)
        if not alt or len(alt.group(1)) < 40:
            e('aria-label da cena curto demais, nao descreve a ilustracao')
        for svg in re.findall(r'<svg[^>]*>', g)[(0 if 'class="anima"' in g else 1):]:
            if 'aria-hidden="true"' not in svg:
                e('camada de cena sem aria-hidden="true"')
        # 3. a legenda declara o que e
        if 'Ilustração' not in g or 'Santa Informa' not in g:
            e('figcaption da cena sem credito "Ilustração ... Santa Informa"')
    # 4. ids nao colidem quando ha duas cenas na pagina (caso real: materia 08)
    ids = re.findall(r'id="(cena-[^"]+)"', s)
    for i in set(ids):
        if ids.count(i) > 1: e(f'id duplicado em cenas: {i}')
    # 5. pausa e degradacao dependem do visual.js na pagina
    if 'class="anima"' in s and 'src="visual.js"' not in s:
        e('pagina com .anima sem visual.js, botao de pausa nao nasce')
    # 6. topo em cena exige raster declarado: JSON-LD ja e conferido,
    #    falta o og:image, que hoje NAO existe em nenhuma materia do site
    ogi = re.search(r'property="og:image" content="([^"]*)"', s)
    if not ogi:
        e('materia com cena sem og:image raster')
    else:
        cam = ogi.group(1).replace('https://santainforma.com.br/', '')
        if cam.endswith('.svg'): e('og:image nao pode ser SVG')
        if not os.path.exists(cam): e(f'og:image nao existe no disco: {cam}')
```

E fora do laço por página, uma sentinela no bloco que já confere `estilo.css`: reprovar se `estilo.css` perder a linha de reduced-motion das cenas (`.anima .corre,.anima .pulsa,.anima .sobe{animation:none` e `.pausa-anima{display:none}`), porque é ela que garante a degradação para imagem estática parada.

Três consequências assumidas deste teste: as matérias 04, 08, 12 e 52 reprovam no dia em que ele entrar (geometria delas ainda não está no cânone e nenhuma tem `og:image`), então o primeiro commit do sistema precisa canonizar as cenas existentes como fragmentos, gerar os rasters de tema e pôr `og:image` nas quatro; a checagem de `og:image` deveria depois se estender a toda matéria, porque a ausência total de `og:image` no site é um buraco de Discover independente deste projeto; e o `ensaio-geral.py` precisa de um caso novo, rodar `aplica-cena.py` num tema e conferir que a saída passa no próprio `checa-site.py`, para o ciclo da nuvem não descobrir defeito de fragmento em produção.

Arquivos citados: `/Users/viniciusdelego/Documents/santainforma/estilo.css` (linhas 353 a 374), `/Users/viniciusdelego/Documents/santainforma/visual.js` (linhas 244 a 261), `/Users/viniciusdelego/Documents/santainforma/ferramentas/checa-site.py`, `/Users/viniciusdelego/Documents/santainforma/ferramentas/prompt-agente-noticias.md` (seção 4), `/Users/viniciusdelego/Documents/santainforma/materia-04-audiencia-orcamento-2027.html` e `materia-12-camara-itapema-pauta.html` (padrões atuais), diretórios novos propostos `/Users/viniciusdelego/Documents/santainforma/ferramentas/cenas/` e ferramenta nova `/Users/viniciusdelego/Documents/santainforma/ferramentas/aplica-cena.py`.

---

# Cenas prontas

CENA TEMÁTICA · CLIMA-TEMPORAL

Verificada em navegador contra o `estilo.css` real do projeto (servida por `http://localhost:8123`, botão de pausa injetado pelo `visual.js` automaticamente, clarão do raio conferido no pico do ciclo). SVG total: 3,6 KB. Camadas animadas: 4 (raio, duas nuvens, chuva). Bloco de referência salvo em `/private/tmp/claude-501/-Users-viniciusdelego-Documents-santainforma/0c959ae5-b969-4b71-8972-9a42f078e3ec/scratchpad/cena-clima-temporal.html`.

BLOCO HTML (colar no lugar da figura de topo):

```html
<figure class="foto">
  <!-- CENA TEMÁTICA · CLIMA-TEMPORAL · 4 camadas animadas
       Camada 0 (estática): céu em gradiente + teto de nuvem + mar com espuma
       Camada 1 (.pulsa.raro): raio ocasional, dentro do fundo, atrás das nuvens
       Camada 2 (.corre 80s): nuvens altas, lentas, mais claras
       Camada 3 (.corre 44s): nuvens baixas, rápidas, mais escuras
       Camada 4 (.corre 3.4s): chuva em traço diagonal, sutil
       Todo desenho fica em x ∈ [0,1200] do viewBox 2400: o <use x="1200">
       duplica e o loop de -50% fecha sem emenda. Não desenhar nada que
       ultrapasse x=1200, senão o laço "pula". -->
  <div class="anima" role="img" aria-label="Ilustração animada de um temporal no litoral: céu carregado, nuvens escuras correndo em duas velocidades, chuva fina e um raio ocasional sobre o mar, nas cores do Santa Informa.">
    <svg class="fundo" viewBox="0 0 1200 525" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <linearGradient id="tmp-ceu" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" style="stop-color:color-mix(in srgb,var(--breu) 82%,var(--mar))"/>
          <stop offset=".6" style="stop-color:color-mix(in srgb,var(--mar) 74%,var(--breu))"/>
          <stop offset="1" style="stop-color:color-mix(in srgb,var(--mar-claro) 24%,var(--mar))"/>
        </linearGradient>
      </defs>
      <rect width="1200" height="525" fill="url(#tmp-ceu)"/>
      <!-- teto de nuvem carregada, estático: ancora o raio e as nuvens que correm -->
      <path d="M0 0h1200v62c-90 26-160-8-260 10s-190-26-300-8-200 24-320 6S90 90 0 72z" style="fill:color-mix(in srgb,var(--breu) 68%,var(--mar))"/>
      <!-- raio: invisível quase o ciclo todo (regra .raro); sem a regra, degrada para brilho suave do .pulsa -->
      <g class="pulsa raro">
        <path d="M764 72 706 236l40-10-64 168" fill="none" stroke-linejoin="round" stroke-linecap="round" stroke-width="16" opacity=".35" style="stroke:var(--sol)"/>
        <path d="M764 72 706 236l40-10-64 168" fill="none" stroke-linejoin="round" stroke-linecap="round" stroke-width="5" opacity=".95" style="stroke:var(--sol)"/>
      </g>
      <!-- mar de fundo, escuro de temporal, com faixa de luz no horizonte e espuma estática -->
      <rect y="398" width="1200" height="127" style="fill:color-mix(in srgb,var(--breu) 46%,var(--mar))"/>
      <path d="M0 398c150-14 250 16 400 4s250-20 400-6 250 18 400 4v20H0z" opacity=".8" style="fill:color-mix(in srgb,var(--mar-claro) 22%,var(--mar))"/>
      <g fill="none" stroke-linecap="round" stroke-width="3" opacity=".3" style="stroke:var(--espuma)">
        <path d="M90 448c24 0 24 8 48 8s24-8 48-8"/>
        <path d="M420 476c24 0 24 8 48 8s24-8 48-8"/>
        <path d="M700 452c24 0 24 8 48 8s24-8 48-8"/>
        <path d="M960 484c24 0 24 8 48 8s24-8 48-8"/>
        <path d="M250 500c24 0 24 8 48 8s24-8 48-8"/>
      </g>
    </svg>
    <!-- nuvens altas: lentas, mais claras, meio transparentes -->
    <div class="corre" style="--dur:80s;top:0">
      <svg viewBox="0 0 2400 170" aria-hidden="true">
        <defs><g id="tmp-nuvem-a">
          <ellipse cx="230" cy="66" rx="170" ry="44"/><ellipse cx="128" cy="44" rx="88" ry="30"/><ellipse cx="330" cy="40" rx="100" ry="32"/>
          <ellipse cx="880" cy="80" rx="200" ry="50"/><ellipse cx="762" cy="54" rx="98" ry="34"/><ellipse cx="988" cy="52" rx="108" ry="36"/>
        </g></defs>
        <g opacity=".55" style="fill:color-mix(in srgb,var(--mar-claro) 34%,var(--mar))">
          <use href="#tmp-nuvem-a"/><use href="#tmp-nuvem-a" x="1200"/>
        </g>
      </svg>
    </div>
    <!-- nuvens baixas: quase o dobro da velocidade, mais escuras -->
    <div class="corre" style="--dur:44s;top:0">
      <svg viewBox="0 0 2400 210" aria-hidden="true">
        <defs><g id="tmp-nuvem-b">
          <ellipse cx="520" cy="70" rx="210" ry="54"/><ellipse cx="392" cy="44" rx="110" ry="36"/><ellipse cx="648" cy="46" rx="118" ry="38"/>
          <ellipse cx="1020" cy="88" rx="168" ry="46"/><ellipse cx="912" cy="60" rx="90" ry="32"/>
        </g></defs>
        <g opacity=".9" style="fill:color-mix(in srgb,var(--breu) 62%,var(--mar))">
          <use href="#tmp-nuvem-b"/><use href="#tmp-nuvem-b" x="1200"/>
        </g>
      </svg>
    </div>
    <!-- chuva: traço diagonal correndo rápido; opacidade baixa, nunca briga com o conteúdo -->
    <div class="corre" style="--dur:3.4s;top:0">
      <svg viewBox="0 0 2400 525" aria-hidden="true">
        <defs><path id="tmp-chuva" d="M60 90l22 46M210 200l22 46M340 60l22 46M470 300l22 46M600 140l22 46M730 380l22 46M860 96l22 46M980 250l22 46M1100 160l22 46M150 420l22 46M420 458l22 46M690 240l22 46M940 430l22 46M300 330l22 46"/></defs>
        <g fill="none" stroke-width="3" stroke-linecap="round" stroke-opacity=".28" style="stroke:var(--mar-claro)">
          <use href="#tmp-chuva"/><use href="#tmp-chuva" x="1200"/>
        </g>
      </svg>
    </div>
  </div>
  <figcaption>Céu fechado, vento e mar mexido: a cena é uma ilustração de tema, não o registro de um temporal específico.
    <span class="credito">Ilustração animada: Santa Informa</span></figcaption>
</figure>
```

CSS NOVO (aditivo, 3 linhas + comentário, colar em `estilo.css` logo depois do bloco de CENAS ANIMADAS, antes da media query de reduced-motion):

```css
/* Raio da cena de temporal: escondido quase o ciclo inteiro, um clarão rápido
   perto do fim. Herda will-change e a pausa do .pulsa; só troca nome e duração. */
.anima .pulsa.raro{animation-name:raio-raro;animation-duration:9s;animation-timing-function:linear}
@keyframes raio-raro{0%,84%,89%,93%,100%{opacity:0}86%{opacity:1}91%{opacity:.7}}
```

DECISÕES QUE O PLANO PRECISA SABER:

- Crédito grafado como "Ilustração animada: Santa Informa", seguindo o precedente da matéria 12 (o pedido dizia "Ilustração:"; a forma longa é mais honesta sobre haver movimento e já é a convenção da casa).
- Cores 100% via `color-mix` das 8 variáveis, sempre em atributo `style` (SVG não aceita `var()` em atributo de apresentação como `fill=""`, só em CSS inline; quem for gerar variações precisa manter esse padrão).
- Degradações verificadas por herança das regras existentes: `prefers-reduced-motion` congela tudo e força `opacity:1` no `.pulsa`, então o quadro parado mostra o raio fixo (bom, quadro estático ainda diz "temporal"); se o agente esquecer a regra `.raro`, o raio vira brilho suave do `.pulsa` padrão, sem quebrar nada; o botão "Pausar animação" é injetado sozinho pelo `visual.js` (linha 246, seletor `.anima`). Ressalva menor: com a cena pausada no botão, o raio provavelmente congela em opacidade 0 e some, porque fica invisível 96% do ciclo.
- Ids com prefixo `tmp-` (tmp-ceu, tmp-nuvem-a, tmp-nuvem-b, tmp-chuva) para não colidir com o sprite de ícones `#i-*` da página; uma cena por página, ids únicos garantidos.
- Regra de emenda do loop documentada no comentário do bloco: nenhum desenho pode passar de x=1200 no viewBox de 2400, senão o salto de -50% fica visível. É a regra número um para o agente de notícias gerar variações sem estragar o laço.
- Aspect-ratio 16/7 vem do próprio `.anima` no CSS; o `viewBox 1200x525` do fundo bate com essa proporção e o `slice` cobre folgas de arredondamento.

POR QUE A CENA FUNCIONA (3 frases):

A profundidade nasce de paralaxe real de três velocidades (nuvens a 80 s atrás, 44 s na frente, chuva a 3,4 s por cima de tudo), que é o mesmo truque de multiplane dos estúdios de animação clássicos, e roda inteiro no compositor porque só transform e opacity mudam. O raio via `.pulsa.raro` dá o "momento" da cena com custo zero de layout: 96% do tempo é um grupo invisível, e o clarão de meio segundo cria a sensação de temporal de verdade sem laço epilético nem disputa com AdSense. E a degradação é honesta em todas as pontas: sem motion vira um quadro parado que ainda comunica temporal (raio fixo, céu carregado, mar escuro), sem a regra nova o raio vira brilho suave, e os 3,6 KB inline chegam junto com o HTML, sem requisição extra e sem tocar LCP.

---

Li o que existe antes de desenhar: `.anima/.corre/.pulsa/.sobe` em `/Users/viniciusdelego/Documents/santainforma/estilo.css` (bloco "CENAS ANIMADAS", linhas ~353-374), a cena estática da matéria 04 e a cena animada da matéria 12 (padrão real: `div.anima[role=img]` + `svg.fundo` estático + `div.corre` com `--dur` inline). A cena abaixo segue esse padrão à risca. O botão de pausa vem de graça: `visual.js` (linha ~246) varre todo `.anima` e injeta o `.pausa-anima` sozinho.

## CENA TEMÁTICA "OBRAS", pronta para colar

Quatro camadas animadas, no teto: sol em `.pulsa`, braço do guindaste em `.gira` (keyframe novo, abaixo), poeira em `.pulsa`, rolo compressor em `.corre` lento. Todo o resto é estático. Nenhum hex novo: tons intermediários nascem de `color-mix` das variáveis, declarados uma vez como custom properties inline no `div.anima`. SVG total: ~3,8 KB, folga dentro dos 6 KB.

```html
<figure class="foto">
  <!-- CENA OBRAS · padrão da materia-12: div.anima é a imagem acessível,
       os SVGs internos são decorativos (aria-hidden). Aspect-ratio 16/7 já
       vem da classe .anima no estilo.css, não repetir aqui. -->
  <div class="anima" role="img"
    aria-label="Ilustração animada de um canteiro de obras: guindaste amarelo gira devagar sobre um prédio em estrutura, com o skyline de Itapema ao fundo e um rolo compressor passando lentamente na frente, nas cores do Santa Informa."
    style="--t0:color-mix(in srgb,var(--mar) 55%,var(--breu));--t1:color-mix(in srgb,var(--breu) 60%,var(--mar));--t2:color-mix(in srgb,var(--breu) 80%,var(--mar));--chao:color-mix(in srgb,var(--breu) 90%,var(--mar));--maq:color-mix(in srgb,var(--coral) 62%,var(--breu))">

    <!-- CAMADA 1 · fundo estático. O céu é o gradiente da própria .anima. -->
    <svg class="fundo" viewBox="0 0 1200 525" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <!-- sol da marca, animado por opacidade (.pulsa) -->
      <circle class="pulsa" cx="150" cy="110" r="44" style="fill:var(--sol)"/>
      <!-- morro ao fundo, à esquerda -->
      <path d="M0 300Q150 205 320 300L320 525H0Z" style="fill:var(--t0)"/>
      <!-- skyline de Itapema: torres da Meia Praia, estáticas -->
      <g style="fill:var(--t1)">
        <rect x="235" y="240" width="46" height="285"/><rect x="295" y="190" width="52" height="335"/>
        <rect x="360" y="255" width="42" height="270"/><rect x="415" y="215" width="50" height="310"/>
        <rect x="478" y="270" width="40" height="255"/><rect x="905" y="230" width="48" height="295"/>
        <rect x="965" y="265" width="44" height="260"/><rect x="1085" y="290" width="40" height="235"/>
        <rect x="1130" y="250" width="46" height="275"/>
      </g>
      <!-- janelas acesas, sol com opacidade baixa, estáticas -->
      <g style="fill:var(--sol)" opacity=".35">
        <rect x="305" y="215" width="10" height="6"/><rect x="325" y="245" width="10" height="6"/>
        <rect x="305" y="285" width="10" height="6"/><rect x="425" y="235" width="10" height="6"/>
        <rect x="447" y="268" width="10" height="6"/><rect x="915" y="255" width="10" height="6"/>
        <rect x="975" y="292" width="10" height="6"/>
      </g>
      <!-- prédio em obra: esqueleto de lajes e pilares, o tom mais escuro da cena -->
      <g style="fill:var(--t2)">
        <rect x="610" y="245" width="9" height="225"/><rect x="665" y="245" width="9" height="225"/>
        <rect x="720" y="245" width="9" height="225"/><rect x="775" y="245" width="9" height="225"/>
        <rect x="830" y="245" width="9" height="225"/><rect x="690" y="245" width="26" height="225"/>
        <rect x="600" y="245" width="248" height="9"/><rect x="600" y="287" width="248" height="9"/>
        <rect x="600" y="329" width="248" height="9"/><rect x="600" y="371" width="248" height="9"/>
        <rect x="600" y="413" width="248" height="9"/><rect x="600" y="455" width="248" height="9"/>
      </g>
      <!-- andaime: traços finos sobre a fachada -->
      <path d="M604 470V245M844 470V245M604 430l240-40M604 350l240-40" fill="none"
        style="stroke:var(--mar-claro)" stroke-opacity=".3" stroke-width="2.5"/>
      <!-- chão do canteiro -->
      <rect y="468" width="1200" height="57" style="fill:var(--chao)"/>
      <!-- tapume e cones, à esquerda, estáticos -->
      <g style="fill:var(--areia)" opacity=".45"><rect x="34" y="428" width="240" height="40"/><rect x="34" y="422" width="240" height="6" opacity=".7"/></g>
      <g style="fill:var(--coral)"><path d="M382 468l12-30 12 30z"/><path d="M552 468l12-30 12 30z"/></g>
      <g style="fill:var(--espuma)" opacity=".7"><rect x="388" y="452" width="12" height="4"/><rect x="558" y="452" width="12" height="4"/></g>

      <!-- CAMADA 2 · poeira do canteiro, respira por opacidade (.pulsa).
           A opacidade baixa fica nos filhos: o grupo anima entre .62 e .92
           e multiplica, então a poeira nunca passa de um véu. -->
      <g class="pulsa" style="fill:var(--areia)">
        <ellipse cx="580" cy="452" rx="46" ry="14" opacity=".22"/>
        <ellipse cx="642" cy="462" rx="60" ry="16" opacity=".16"/>
        <ellipse cx="880" cy="458" rx="42" ry="13" opacity=".2"/>
      </g>

      <!-- guindaste: torre estática... -->
      <rect x="1010" y="140" width="14" height="330" style="fill:var(--sol)"/>
      <path d="M1010 150l14 26-14 26 14 26-14 26 14 26-14 26 14 26-14 26 14 26-14 26 14 26-14 26"
        fill="none" style="stroke:var(--breu)" stroke-opacity=".35" stroke-width="3"/>
      <rect x="996" y="458" width="42" height="12" style="fill:var(--sol)"/>

      <!-- CAMADA 3 · ...e braço que gira devagar (.gira, keyframe novo).
           O eixo é o topo da torre, em coordenadas do viewBox. -->
      <g class="gira" style="--eixo:1017px 150px">
        <polygon points="1017,96 1005,140 1029,140" style="fill:var(--sol)"/>
        <path d="M1017 100L800 150M1017 100L1092 148" style="stroke:var(--sol)" stroke-width="3" stroke-opacity=".8" fill="none"/>
        <polygon points="1029,142 770,150 770,160 1029,158" style="fill:var(--sol)"/>
        <rect x="1029" y="144" width="70" height="10" style="fill:var(--sol)"/>
        <rect x="1078" y="154" width="24" height="26" style="fill:var(--areia)"/>
        <rect x="1000" y="126" width="32" height="16" style="fill:var(--sol)"/>
        <rect x="1004" y="129" width="14" height="10" style="fill:var(--espuma)" opacity=".6"/>
        <rect x="812" y="158" width="16" height="8" style="fill:var(--sol)"/>
        <line x1="820" y1="166" x2="820" y2="238" style="stroke:var(--mar-claro)" stroke-width="2.5"/>
        <rect x="800" y="238" width="40" height="22" style="fill:var(--mar-claro)"/>
      </g>
    </svg>

    <!-- CAMADA 4 · rolo compressor em .corre lento. A faixa tem o dobro da
         largura e o desenho se repete em x+1200 via use: o loop de -50%
         fecha sem emenda. Com o kill switch (reduced-motion), congela com o
         rolo visível em quadro, porque a cópia base está entre x=200 e 420. -->
    <div class="corre" style="--dur:56s;bottom:0">
      <svg viewBox="0 0 2400 120" preserveAspectRatio="none" aria-hidden="true">
        <g id="obra-rolo">
          <ellipse cx="310" cy="114" rx="120" ry="7" style="fill:var(--breu)" opacity=".3"/>
          <rect x="278" y="46" width="122" height="40" rx="6" style="fill:var(--maq)"/>
          <rect x="240" y="34" width="52" height="20" rx="6" style="fill:var(--maq)"/>
          <rect x="340" y="12" width="54" height="46" rx="5" style="fill:var(--maq)"/>
          <rect x="348" y="20" width="28" height="20" style="fill:var(--sol)" opacity=".55"/>
          <rect x="334" y="0" width="6" height="16" style="fill:var(--maq)"/>
          <circle cx="250" cy="78" r="38" style="fill:var(--mar-claro)"/>
          <circle cx="250" cy="78" r="13" style="fill:var(--t2)"/>
          <circle cx="374" cy="92" r="25" style="fill:var(--t2)"/>
          <circle cx="374" cy="92" r="8" style="fill:var(--mar-claro)"/>
        </g>
        <use href="#obra-rolo" x="1200"/>
      </svg>
    </div>
  </div>
  <figcaption>A cena não retrata um canteiro específico: é a ilustração símbolo da editoria de Obras, com guindaste, prédio em estrutura e o skyline da cidade ao fundo.
    <span class="credito">Ilustração animada: Santa Informa</span></figcaption>
</figure>
```

Nota sobre o crédito: o pedido dizia "Ilustração: Santa Informa", mas a cena animada em produção (materia-12) usa "Ilustração animada: Santa Informa" e mantive a convenção da casa; trocar é uma palavra.

## CSS aditivo (estilo.css, colar logo após o @keyframes sobe, linha ~371)

```css
/* CENA OBRAS: braço do guindaste oscila poucos graus. So transform, compositor puro. */
.anima .gira{transform-box:view-box;transform-origin:var(--eixo,50% 50%);will-change:transform;animation:gira 16s ease-in-out infinite}
@keyframes gira{0%,100%{transform:rotate(-3.5deg)}50%{transform:rotate(3.5deg)}}
```

Três linhas. `transform-box:view-box` é obrigatório: sem ele o `transform-origin` do SVG mede a partir do canto do viewport e o braço orbitaria em vez de girar no eixo da torre. Duas emendas em seletores que já existem (não são linhas novas, são vírgulas):

1. Linha ~373: `.anima.pausada .corre,.anima.pausada .pulsa,.anima.pausada .sobe` ganha `,.anima.pausada .gira` — o botão de pausa do visual.js passa a congelar o braço também.
2. Linha ~378, dentro do `@media(prefers-reduced-motion:reduce)`: `.anima .corre,.anima .pulsa,.anima .sobe` ganha `,.anima .gira` — o kill switch global zera o giro e a cena degrada para imagem estática correta (braço nivelado, rolo em quadro).

Para o agente da nuvem: o único id interno é `obra-rolo`; se duas cenas de obras coexistirem numa mesma página (não acontece em matéria), renomear. Os `color-mix` ficam todos no `style` do `div.anima`, então o template é parametrizável sem tocar no estilo.css.

## Por que funciona

O giro de ±3,5° do braço com a carga pendurada é o movimento que o olho associa a canteiro vivo, e custa uma única animação de `transform` num grupo SVG, resolvida no compositor sem layout nem paint, exatamente como as camadas já auditadas da materia-12. A leitura em profundidade vem de graça pela escala tonal (morro claro, torres médias, esqueleto escuro, máquina saturada na frente), então o "3D" percebido não depende de perspective nem de scroll, e a cena congelada pelo reduced-motion continua sendo uma ilustração completa e honesta. Tudo reusa a infraestrutura existente (pausa automática do visual.js, kill switch global, `--dur` inline), então o agente de notícias só precisa colar o bloco e, uma vez, aplicar as três linhas e duas vírgulas no estilo.css.