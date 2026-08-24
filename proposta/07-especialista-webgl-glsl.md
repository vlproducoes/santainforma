## Módulo Mar Vivo, WebGL 2 vanilla para o topo do Santa Informa

Proposta técnica completa. Nada disso entra em `main` sem aprovação do editor. Pontos de integração: shaders e boilerplate entram no fim de `/Users/viniciusdelego/Documents/santainforma/visual.js`, três linhas de CSS entram em `/Users/viniciusdelego/Documents/santainforma/estilo.css`, o HTML aproveita a estrutura `.anima` que já existe nas matérias 04 e 05.

Filosofia demoscene do módulo: 1 programa, 1 draw call, 0 buffers, 0 texturas, 0 dependências. Todo o mar é um único fragment shader num triângulo que cobre a tela.

---

### 1. Shaders GLSL completos

**Vertex shader** (triângulo único via `gl_VertexID`, sem buffer, sem atributo):

```glsl
#version 300 es
/* Um triangulo gigante cobre a tela inteira: (-1,-1),(3,-1),(-1,3).
   Sem VBO, sem atributo: o indice do vertice gera a posicao. */
void main() {
  vec2 v = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2);
  gl_Position = vec4(v * 2.0 - 1.0, 0.0, 1.0);
}
```

**Fragment shader** (mar completo: céu por hora do dia, ondas por soma de senos + ruído, reflexo do sol, espuma):

```glsl
#version 300 es
/* MAR VIVO · Santa Informa
   Mar estilizado em 2,5D: plano com pseudo-perspectiva, sem raymarching,
   sem loop, sem textura. Custo fixo e baixo por pixel.
   highp de proposito: ES 3.0 garante highp no fragment, e mediump
   degradaria o sin() depois de meia hora de u_tempo acumulado. */
precision highp float;

uniform vec2  u_res;      /* resolucao real do canvas, em pixels */
uniform float u_tempo;    /* segundos, relogio proprio do modulo */
uniform vec2  u_ponteiro; /* ponteiro 0..1, origem embaixo a esquerda */
uniform float u_hora;     /* hora local 0..24, com fracao de minutos */

out vec4 corFinal;

/* Paleta do site, os mesmos hex de estilo.css convertidos para 0..1 */
const vec3 BREU     = vec3(0.039, 0.122, 0.157); /* --breu      #0A1F28 */
const vec3 MAR      = vec3(0.067, 0.282, 0.357); /* --mar       #11485B */
const vec3 SOL      = vec3(1.000, 0.714, 0.153); /* --sol       #FFB627 */
const vec3 ESPUMA   = vec3(0.945, 0.961, 0.953); /* --espuma    #F1F5F3 */
const vec3 MARCLARO = vec3(0.561, 0.690, 0.725); /* --mar-claro #8FB0B9 */

const float HORIZONTE = 0.62;  /* altura do horizonte em uv.y */

/* hash sem seno: estavel em qualquer GPU, nao estoura em coordenada grande */
float hash21(vec2 p) {
  p = fract(p * vec2(127.1, 311.7));
  p += dot(p, p + 19.19);
  return fract(p.x * p.y);
}

/* ruido de valor com interpolacao suave (2 octavas custam ~40 ALU) */
float ruido(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  float a = hash21(i);
  float b = hash21(i + vec2(1.0, 0.0));
  float c = hash21(i + vec2(0.0, 1.0));
  float d = hash21(i + vec2(1.0, 1.0));
  return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}

/* Altura do mar por soma de senos, com derivada analitica em x.
   Frequencias fora de razao inteira: o padrao nunca "fecha" e repete.
   Devolve vec2(altura, inclinacao). A inclinacao alimenta o sombreado
   e o cintilar do reflexo, de graca, sem segunda amostragem. */
vec2 onda(vec2 p, float t) {
  float h = 0.0, dx = 0.0;
  float a, k, f;

  a = 0.34; k = 0.9;  f = k * p.x + p.y * 0.5 + t * 0.9;
  h += a * sin(f);  dx += a * k * cos(f);

  a = 0.21; k = 2.3;  f = k * p.x - p.y * 0.8 - t * 1.4;
  h += a * sin(f);  dx += a * k * cos(f);

  a = 0.13; k = 4.1;  f = k * p.x + p.y * 1.7 + t * 2.2;
  h += a * sin(f);  dx += a * k * cos(f);

  a = 0.08; k = 7.3;  f = k * p.x - p.y * 2.9 + t * 3.1;
  h += a * sin(f);  dx += a * k * cos(f);

  /* o ruido quebra a regularidade dos senos: mar, nao senoide */
  h += (ruido(p * 1.7 + t * 0.25) - 0.5) * 0.30;
  h += (ruido(p * 5.3 - t * 0.40) - 0.5) * 0.12;

  return vec2(h, dx);
}

void main() {
  vec2 uv = gl_FragCoord.xy / u_res;
  float aspecto = u_res.x / u_res.y;
  float t = u_tempo;

  /* LUZ DO DIA a partir da hora local do leitor.
     elev: -1 madrugada, +1 meio-dia. dia: 0 noite, 1 dia pleno.
     ouro: pico curto no nascer e no por do sol. */
  float elev = cos((u_hora - 12.5) / 12.0 * 3.14159265);
  float dia  = smoothstep(-0.10, 0.35, elev);
  float ouro = smoothstep(-0.18, 0.02, elev) * (1.0 - smoothstep(0.10, 0.45, elev));

  /* de dia o brilho e o sol; de noite vira lua, na cor da espuma */
  vec3 corBrilho = mix(ESPUMA, SOL, clamp(dia + ouro, 0.0, 1.0));

  /* posicao do sol: levemente atraida pelo ponteiro, nunca colada nele */
  float solX = mix(0.66, u_ponteiro.x, 0.12);
  float solY = HORIZONTE + 0.06 + max(elev, 0.0) * 0.26;

  /* CEU: degrade vertical que muda com a hora, dourado so no horizonte */
  vec3 ceuAlto  = mix(BREU, mix(MAR, MARCLARO, 0.55), dia);
  vec3 ceuBaixo = mix(mix(BREU, MAR, 0.45), mix(MARCLARO, ESPUMA, 0.6), dia);
  ceuBaixo = mix(ceuBaixo, SOL, ouro * 0.45);
  vec3 ceu = mix(ceuBaixo, ceuAlto, smoothstep(HORIZONTE, 1.0, uv.y));

  /* disco do sol (ou lua), com halo curto; correcao de aspecto para ficar redondo */
  vec2 dif = uv - vec2(solX, solY);
  dif.x *= aspecto;
  float d = length(dif);
  float disco = 1.0 - smoothstep(0.030, 0.046, d);
  ceu += corBrilho * (disco * 0.85 + exp(-d * 8.0) * 0.20) * (0.55 + 0.45 * dia);

  /* MAR: pseudo-perspectiva. ph e a distancia abaixo do horizonte,
     prof cresce ao se aproximar do horizonte, comprimindo as ondas. */
  float ph   = max(HORIZONTE - uv.y, 0.0);
  float prof = 1.0 / (ph * 3.0 + 0.06);
  vec2  p    = vec2((uv.x - 0.5) * aspecto * prof, prof);
  p.y -= t * 0.7;                              /* a mare corre para a praia */

  vec2 o = onda(p, t);
  o *= smoothstep(0.0, 0.20, ph);              /* amplitude some no horizonte,
                                                  senao vira ruido serrilhado */

  /* base: escurece com a distancia e funde com o ceu; noite escurece tudo */
  vec3 corMar = mix(MAR, BREU, clamp(prof * 0.09, 0.0, 0.72));
  corMar = mix(corMar, BREU, (1.0 - dia) * 0.5);

  /* face da onda voltada para a luz clareia, a oposta escurece */
  float luzFace = clamp(0.5 - o.y * 0.6, 0.0, 1.0);
  corMar = mix(corMar * 0.85, mix(corMar, MARCLARO, 0.30), luzFace);

  /* REFLEXO DO SOL: coluna que abre conforme desce para a praia.
     Cintila onde a faceta da onda esta quase plana (|inclinacao| pequena),
     que e como reflexo especular funciona de verdade. */
  float faixa  = 1.0 - smoothstep(0.0, 0.10 + ph * 0.55, abs(uv.x - solX));
  float faceta = pow(clamp(1.0 - abs(o.y) * 1.4, 0.0, 1.0), 3.0);
  corMar += corBrilho * faixa * faceta * (0.18 + 0.45 * max(dia, ouro));

  /* ESPUMA: crista alta rendada por ruido, mais a espuma da beira embaixo */
  float renda = ruido(p * 9.0 + t * 0.8);
  float esp = smoothstep(0.50, 0.85, o.x) * smoothstep(0.45, 0.75, renda);
  esp += (1.0 - smoothstep(0.0, 0.09, uv.y)) * smoothstep(0.35, 0.8, renda) * 0.6;
  corMar = mix(corMar, ESPUMA * (0.45 + 0.55 * dia), clamp(esp, 0.0, 1.0) * 0.75);

  /* horizonte com 2px de fusao, para nao serrilhar a linha */
  vec3 cor = mix(corMar, ceu, smoothstep(HORIZONTE - 0.003, HORIZONTE + 0.003, uv.y));

  /* dithering de 1 bit: mata as faixas de banding do degrade escuro,
     que em AMOLED barato aparecem feias. Substitui o MSAA desligado. */
  cor += (hash21(gl_FragCoord.xy) - 0.5) / 255.0;

  corFinal = vec4(clamp(cor, 0.0, 1.0), 1.0);
}
```

---

### 2. Boilerplate JS (entra no fim de visual.js)

Os dois shaders acima ficam em constantes `MAR_VERT` e `MAR_FRAG` (template literals) logo acima deste bloco.

```js
/* MAR VIVO · WebGL 2 progressivo
   O HTML ja traz a cena SVG dentro de .anima.mar-vivo. Este modulo so a
   cobre com o canvas quando todas as condicoes permitem. Falhou qualquer
   uma, em qualquer ponto, o SVG fica e ninguem percebe. */
(function () {
  var cena = document.querySelector('.mar-vivo');
  if (!cena) return;

  /* deteccao honesta: preferencia, economia de dados, memoria, contexto */
  var reduzido = matchMedia('(prefers-reduced-motion: reduce)');
  if (reduzido.matches) return;
  if (navigator.connection && navigator.connection.saveData) return;
  if ((navigator.deviceMemory || 4) < 4) return;  /* Safari nao expoe: passa */

  var cv = document.createElement('canvas');
  var gl = cv.getContext('webgl2', {
    alpha: false, antialias: false, depth: false, stencil: false,
    powerPreference: 'low-power'
  });
  if (!gl) return;

  function compilar(tipo, fonte) {
    var s = gl.createShader(tipo);
    gl.shaderSource(s, fonte); gl.compileShader(s);
    return gl.getShaderParameter(s, gl.COMPILE_STATUS) ? s : null;
  }
  var vs = compilar(gl.VERTEX_SHADER, MAR_VERT);
  var fs = compilar(gl.FRAGMENT_SHADER, MAR_FRAG);
  if (!vs || !fs) return;                    /* driver ruim compila errado: SVG */
  var pg = gl.createProgram();
  gl.attachShader(pg, vs); gl.attachShader(pg, fs); gl.linkProgram(pg);
  if (!gl.getProgramParameter(pg, gl.LINK_STATUS)) return;
  gl.useProgram(pg);

  var uRes  = gl.getUniformLocation(pg, 'u_res');
  var uTmp  = gl.getUniformLocation(pg, 'u_tempo');
  var uPnt  = gl.getUniformLocation(pg, 'u_ponteiro');
  var uHora = gl.getUniformLocation(pg, 'u_hora');

  /* resolucao reduzida: teto de 1.5x. Num degrade em movimento ninguem
     enxerga a diferenca para 3x, e o custo cai pela metade ou mais. */
  var DPR = Math.min(window.devicePixelRatio || 1, 1.5);
  function medir() {
    var w = (cena.clientWidth * DPR) | 0, h = (cena.clientHeight * DPR) | 0;
    if (cv.width !== w || cv.height !== h) {
      cv.width = w; cv.height = h;
      gl.viewport(0, 0, w, h);
      gl.uniform2f(uRes, w, h);
    }
  }

  var px = 0.66, py = 0.5;   /* ponteiro em repouso: onde o sol mora */
  cena.addEventListener('pointermove', function (e) {
    var r = cena.getBoundingClientRect();
    px = (e.clientX - r.left) / r.width;
    py = 1 - (e.clientY - r.top) / r.height;
  }, { passive: true });

  /* relogio proprio acumulado: a pausa nao da salto, a retomada continua */
  var QUADRO = 1000 / 30, antes = 0, tempo = 0, raf = 0, visivel = false;
  function quadro(t) {
    raf = requestAnimationFrame(quadro);
    if (t - antes < QUADRO - 1) return;      /* 30 qps de proposito */
    tempo += Math.min(t - antes, 100);       /* aba dormiu: nao salta */
    antes = t;
    medir();
    var agora = new Date();
    gl.uniform1f(uTmp, tempo / 1000);
    gl.uniform2f(uPnt, px, py);
    gl.uniform1f(uHora, agora.getHours() + agora.getMinutes() / 60);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
  function ligar() {
    if (raf || !visivel || document.hidden) return;
    if (cena.classList.contains('pausada')) return;  /* botao do site vale aqui */
    antes = performance.now();
    raf = requestAnimationFrame(quadro);
  }
  function desligar() { cancelAnimationFrame(raf); raf = 0; }
  function desmontar() { desligar(); cv.remove(); }  /* volta a valer o SVG */

  /* fora da tela nao roda; aba escondida nao roda */
  new IntersectionObserver(function (e) {
    visivel = e[0].isIntersecting;
    if (visivel) ligar(); else desligar();
  }).observe(cena);
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) desligar(); else ligar();
  });

  /* o botao "Pausar animacao" que ja existe alterna .pausada na cena */
  new MutationObserver(function () {
    if (cena.classList.contains('pausada')) desligar(); else ligar();
  }).observe(cena, { attributes: true, attributeFilter: ['class'] });

  /* mudou a preferencia no meio da sessao: desmonta de vez */
  reduzido.addEventListener('change', function () {
    if (reduzido.matches) desmontar();
  });
  gl.canvas.addEventListener('webglcontextlost', function (e) {
    e.preventDefault(); desmontar();
  });

  cv.appendChild ? cena.appendChild(cv) : 0;
})();
```

Correção na última linha ao integrar: é só `cena.appendChild(cv);`.

CSS a acrescentar em `estilo.css` (usa o box `.anima` existente, que já reserva `aspect-ratio:16/7`, então CLS é zero):

```css
/* MAR VIVO: o canvas cobre a cena SVG quando o WebGL entra */
.mar-vivo{position:relative}
.mar-vivo canvas{position:absolute;inset:0;width:100%;height:100%}
@media(prefers-reduced-motion:reduce){.mar-vivo canvas{display:none}}
```

Início do módulo: embrulhar a chamada em `requestIdleCallback(iniciar, {timeout: 2000})` com fallback `setTimeout(iniciar, 1200)`. O shader nunca compila durante a disputa pelo LCP (título do hero e fonte). Compilar dois shaders custa 5 a 30 ms de driver, isso não pode cair dentro da janela do LCP.

---

### 3. Orçamento

**Custo por pixel.** O shader custa aproximadamente 220 operações ALU por fragmento (4 senos com derivada ≈ 40, 3 chamadas de ruído ≈ 120, resto ≈ 60). Zero leituras de textura, zero branches divergentes, zero loops.

**Área pintada com DPR 1.5.** Celular (hero 390×171 CSS): 585×256 ≈ 150 mil pixels. Desktop (1440×630): ≈ 2,0 milhões de pixels.

**Vazão a 30 fps.** Celular: 4,5 M fragmentos/s ≈ 1 GOP/s, abaixo de 4% de um Mali-G52/G57 de celular intermediário. Desktop: 61 M fragmentos/s ≈ 13 GOPs, poucos por cento de qualquer iGPU de 2018 em diante. `powerPreference:'low-power'` garante a iGPU em notebook com duas GPUs.

**Bateria.** A conta real não é ALU, é manter GPU e compositor acordados. Estimativa honesta em Android intermediário: 0,3 a 0,7 W extras enquanto o hero está visível (a tela sozinha consome 1 a 2 W). Como o loop é cancelado, não apenas pulado, fora da viewport e com aba oculta, e o leitor típico passa 10 a 20 segundos no hero antes de rolar, o custo por sessão é desprezível. Sem o gate de viewport o mesmo efeito custaria bateria a página inteira, e é aí que sites erram.

**Por que 30 fps de propósito.** Água é movimento lento e não interativo, o olho não cobra 60 fps de conteúdo ambiente (cobra de scroll e de cursor, que continuam a 60 ou mais porque não passam por esse loop). Metade dos frames é metade das acordadas de GPU e metade das composições. E durante o scroll o compositor fica com folga, protegendo INP. **Como:** gate de timestamp dentro do rAF (`t - antes < 33.3 - 1`), nunca `setInterval` (deriva do vsync e provoca frame rasgado). O `-1` de folga evita pular frame por jitter do vsync. O relógio próprio acumulado (`tempo += dt` com teto de 100 ms) mantém a velocidade da animação independente do fps e sem salto ao retomar.

**Core Web Vitals.** LCP: intocado (início adiado para idle, canvas não é candidato a LCP). CLS: zero (o box `.anima` já reserva a área por aspect-ratio). INP: pointermove é passivo e só escreve duas variáveis, todo o trabalho pesado mora na GPU.

---

### 4. Degradação em 3 camadas

O HTML entrega a camada 2 pronta. As camadas de cima são aplicadas por cima, nunca no lugar.

**Camada 1, WebGL 2 (o canvas).** Só entra quando tudo isso for verdade: contexto WebGL2 criado, shaders compilados e linkados, sem `prefers-reduced-motion`, sem `saveData`, `deviceMemory` ausente ou ≥ 4.

**Camada 2, SVG animado (o padrão).** A cena `.anima` que já existe nas matérias 04 e 05: duas faixas de onda SVG transladando via keyframe `corre`, sol com `pulsa`. Anima só `transform` e `opacity`, roda no compositor, funciona sem uma linha de JS e já obedece o botão de pausa e o `prefers-reduced-motion` do CSS atual. É a espinha dorsal, não um plano B.

**Camada 3, gradiente estático.** O background que `.anima` já tem: `linear-gradient(180deg, var(--breu), #16536A)`. É o que aparece sem SVG renderizado, e é o que o leitor com `prefers-reduced-motion` vê, porque a regra global do CSS já mata as animações SVG e a media query acima esconde o canvas.

**Detecção honesta, cheque a cheque:**

- `getContext('webgl2')` nulo: ausência real (WebView antiga, driver na blocklist). Não vale fazer fallback para WebGL1: complexidade dobrada para servir exatamente os aparelhos que não deveriam rodar shader nenhum.
- Falha de compile ou link: retorno silencioso. Driver que compila errado existe, e o leitor nunca deve ver um retângulo preto.
- `prefers-reduced-motion`: nem monta. Mudou no meio da sessão, desmonta (o listener está no boilerplate).
- `navigator.connection.saveData`: quem pediu economia de dados pediu economia de bateria também.
- `navigator.deviceMemory < 4`: só existe em navegador Chromium. Safari devolve `undefined` e passa, correto, porque GPU da Apple aguenta.
- `webglcontextlost`: `preventDefault` e desmonta. Não tenta restaurar, o SVG embaixo já está lá.
- Sem sniffing de user-agent em hipótese nenhuma. Refinamento opcional de segunda versão: medir o tempo dos primeiros 90 frames e se autodemitir para o SVG se o p95 passar de 8 ms. Medir é mais honesto que adivinhar o aparelho.

---

### 5. Veredito WebGPU em 2026

Não entra. Suporte hoje: Chrome e Edge maduros (desktop desde 2023, Android desde 2024), Safari só a partir do 26 (setembro de 2025), Firefox a partir do 141 e ainda desigual entre sistemas. Para o público deste portal, celular intermediário no Brasil, com parque grande de Android antigo e iPhone que nunca verá iOS 26, a cobertura real fica bem abaixo dos ~97% do WebGL2. E o decisivo: para um efeito de um único pass de fragment shader, WebGPU não oferece nenhuma capacidade visual ou de desempenho que o WebGL2 não tenha. A vantagem dele aparece em compute shader (oceano por FFT, partículas em massa), exatamente o tipo de custo que este módulo rejeita de propósito. Adotar agora significaria manter dois caminhos de render num repositório cuja Constituição exige um único JS sem dependências. Reavaliar apenas se um dia o efeito virar simulação, o que num portal que vive de Core Web Vitals não deve acontecer.

**Nota de honestidade sobre a lista de tecnologias citada.** Three.js (~150 kB gzip) é um scene graph para gerenciar milhares de objetos, aqui há um triângulo e um programa, seria peso morto além de violar a regra de dependências. React Three Fiber exige React, que o site não tem nem precisa. GSAP e Lenis fazem o que o CSS já faz neste repositório (a barra de progresso em `estilo.css` já usa `animation-timeline: scroll()`, que é a versão nativa do que essas libs vendem). Framer Motion é para React. WebAssembly/Rust adicionariam build a um projeto sem build para acelerar uma conta que já roda na GPU. SVG entra, e entra como protagonista: é a camada 2, não a muleta.