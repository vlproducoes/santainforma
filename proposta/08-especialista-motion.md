# Sistema de Movimento · Santa Informa (vanilla, sem dependência)

Nota honesta sobre o cardápio pedido: GSAP, Framer Motion, Lenis, Three.js e R3F são bibliotecas, e a Constituição barra dependência externa. A boa notícia: o que um portal de notícias usaria delas hoje é recurso de plataforma. ScrollTrigger vira CSS scroll-driven animation (compositor, zero main thread), o spring do Framer vira 40 linhas de física, o FLIP do GSAP vira View Transition nativa. WebGL, WebGPU, GLSL, WASM e Rust não têm papel no shell de um portal lido em celular intermediário: custam LCP e INP, que aqui são receita, e não geram uma page view a mais. As cenas SVG animadas (`.anima`) já são a resposta certa para efeito de marca e continuam.

---

## 1. Tokens de movimento

Entra no topo de `/Users/viniciusdelego/Documents/santainforma/estilo.css`, dentro do `:root` existente:

```css
/* MOVIMENTO | tokens. Toda duracao e curva nova sai daqui. */
--dur-toque:.15s;    /* resposta a mao */
--dur-troca:.3s;     /* mesmo elemento mudando de estado */
--dur-chegada:.55s;  /* conteudo novo entrando na tela */
--curva-chegada:cubic-bezier(.2,.7,.3,1);   /* desacelera ate parar */
--curva-troca:cubic-bezier(.45,0,.2,1);     /* simetrica, vai e volta igual */
--curva-mola:cubic-bezier(.34,1.56,.64,1);  /* passa 10% do alvo e assenta */
```

Regras de uso:

- **toque + linear ou chegada**: hover, foco, cor, borda, sublinhado. Nunca mais que isso para feedback de ponteiro.
- **troca + curva-troca**: o mesmo elemento trocando de conteúdo ou estado. Painel do Modo de Leitura, abas do horóscopo, signo selecionado.
- **chegada + curva-chegada**: coisa nova entrando. Reveal, intro do hero, view transition. Entrada sempre desacelera; elemento que chega acelerando parece estar indo embora.
- **curva-mola**: só em `transform` (scale, translate) de micro-interação. Nunca em opacity (overshoot de opacidade lê como flicker), nunca em bloco de texto, nunca em coisa maior que um botão.
- **Mola física JS** (seção 3): quando o gesto pode ser interrompido no meio (apertar e soltar chip). CSS não re-alveja no meio do caminho sem pulo; a mola sim.
- Só se anima `transform`, `opacity` e `filter` curto. Duração fora dos três tokens é proibida; o hero pode encadear tokens (`.45s` + delay), não inventar valores.

Refatoração: os valores fixos das linhas 64, 89, 92 e 421-422 do `estilo.css` passam a usar os tokens (a curva da casa já é `--curva-chegada`, só ganha nome).

---

## 2. Receitas

### 2.1 Reveal on scroll sem JS (substitui o IntersectionObserver)

Apaga o bloco de reveal do `visual.js` (linhas 67-118), a linha 4 (`rv-on`), e as regras `.rv` do `estilo.css` (linhas 421-422 e a menção na linha 498). Entra no lugar, em `estilo.css`:

```css
/* REVELACAO POR ROLAGEM | sem timeline de rolagem, sem efeito: o conteudo
   ja e visivel por padrao. Estado invisivel mora SO no from do keyframe:
   com animation:none (reduced motion, navegador antigo) tudo aparece. */
@supports (animation-timeline:view()){
  article.card,.d,.item,.destaque,.patro,figure.foto{
    animation:entra linear both;
    animation-timeline:view();
    animation-range:entry 0% entry 55%;
  }
  /* escalonamento na grade: cada coluna comeca um pouco depois */
  .grade article.card:nth-child(3n+2){animation-range:entry 8% entry 63%}
  .grade article.card:nth-child(3n){animation-range:entry 16% entry 71%}
}
@keyframes entra{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
```

Por que assim: o reveal fica atrelado ao dedo (scrub), roda no compositor, e reverte sozinho se o leitor voltar. `linear` de propósito: em animação scrubada a suavidade vem do range, não da curva, senão o movimento descola do gesto. Quem está na primeira dobra já passou do range e nasce pronto (`both`), sem flash e sem custo de LCP. Chrome, Edge e Safari 26 animam; Firefox só mostra o conteúdo parado, que é exatamente a regra de ouro. O reduced motion global da linha 494 (`*{animation:none!important}`) já cobre, e como o estado invisível está no keyframe, não precisa de lista de restauração.

### 2.2 Parallax de capa de card

```css
@supports (animation-timeline:view()){
  article.card{overflow:hidden}
  article.card .capa{
    animation:capa-flutua linear both;
    animation-timeline:view();
    animation-range:cover 0% cover 100%;
  }
  /* a escala mora no keyframe: sem animacao, imagem inteira, sem corte */
  @keyframes capa-flutua{
    from{scale:1.12;translate:0 -5%}
    to{scale:1.12;translate:0 5%}
  }
}
```

Deslocamento máximo de 5%: parallax de portal de notícia é temperinho, não atração. Só `translate` e `scale` (compositor). Vale para `.capa` de card, nunca para a foto de topo da matéria (candidata a LCP não ganha escala). Reduced motion: coberto pelo kill switch global, e o `from` no keyframe garante imagem sem zoom.

### 2.3 Contador numérico que anima ao entrar

HTML do dado: `<i>R$ <span data-conta="740">740</span> mil</i>`. O valor verdadeiro fica no HTML; sem JS nada muda. Entra em `visual.js`:

```js
/* CONTADOR | o numero sobe quando o bloco entra. ~20 linhas. */
document.addEventListener('DOMContentLoaded', function () {
  var alvos = document.querySelectorAll('[data-conta]');
  if (!alvos.length || !('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var obs = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      obs.unobserve(e.target);
      var el = e.target, fim = parseInt(el.getAttribute('data-conta'), 10);
      var t0 = performance.now(), DUR = 900;
      (function quadro(agora) {
        var t = Math.min((agora - t0) / DUR, 1);
        var p = 1 - Math.pow(1 - t, 3);   /* desacelera no fim */
        el.textContent = Math.round(fim * p).toLocaleString('pt-BR');
        if (t < 1) requestAnimationFrame(quadro);
      })(t0);
    });
  }, { threshold: 0.6 });
  for (var i = 0; i < alvos.length; i++) obs.observe(alvos[i]);
});
```

E no CSS: `.d i{font-variant-numeric:tabular-nums}` para o número não sacudir a caixa enquanto conta. Existe a variante 100% CSS com `@property --n{syntax:"<integer>"}` + `counter()` num pseudo-elemento, mas ela exige duplicar o valor (um escondido para leitor de tela, um no `content`) e o leitor de tela pode anunciar os dois; num site que leva WCAG a sério, o JS mínimo acima é a versão certa. Reduced motion: sai cedo, número já está lá.

### 2.4 Manchete com entrada por palavra (CSS only)

Marcação, gerada na autoria da matéria (só o h1 do hero, nunca em card):

```html
<h1 class="cascata">
  <span style="--i:0">Meia</span> <span style="--i:1">Praia</span>
  <span style="--i:2">ganha</span> <span style="--i:3">150</span>
  <span style="--i:4">metros</span> <span style="--i:5">de</span>
  <span style="--i:6">faixa</span> <span style="--i:7">nova</span>
</h1>
```

```css
.cascata span{
  display:inline-block;
  animation:palavra .45s var(--curva-chegada) both;
  animation-delay:min(calc(var(--i) * .05s), .35s); /* teto: manchete longa nao vira novela */
}
@keyframes palavra{from{opacity:0;transform:translateY(.35em)}to{opacity:1;transform:none}}
```

Estado invisível no `from`, então o `animation:none` do reduced motion global entrega o título inteiro parado, sem regra extra. Regra de LCP: a última palavra fica visível em no máximo 0,8s (teto de delay + duração). Onde o h1 disputa LCP sem imagem acima (matéria sem foto), não usa cascata. O texto continua nó de texto real: seleção, busca na página e SEO intactos. `text-wrap:balance` da linha 32 segue funcionando com os spans.

### 2.5 View transition nomeada: capa do card vira foto da matéria

O site já tem `@view-transition{navigation:auto}` e o desligamento por reduced motion (linhas 21-26). Falta o morph. Cada par recebe o mesmo nome, único por página. Na home:

```html
<img class="capa" style="view-transition-name:capa-m07" src="..." ...>
```

Na matéria, na foto de topo:

```html
<figure class="foto"><img style="view-transition-name:capa-m07" ...>
```

Tuning em `estilo.css`. O pseudo-elemento que faz o morph de posição e tamanho é o `::view-transition-group()`; os `old/new` só precisam parar de fazer crossfade esticado:

```css
/* a classe permite estilizar todos os pares de uma vez */
article.card .capa,figure.foto img{view-transition-class:capa}

::view-transition-group(.capa){
  animation-duration:var(--dur-troca);
  animation-timing-function:var(--curva-troca);
}
/* mesmo assunto nas duas pontas: sem crossfade, a foto so viaja e recorta */
::view-transition-old(.capa),
::view-transition-new(.capa){
  animation:none;
  mix-blend-mode:normal;
  height:100%;
  overflow:clip;
  object-fit:cover;
}
/* o resto da pagina troca num fade curto, cabecalho e rodape ja ficam parados */
::view-transition-old(root),::view-transition-new(root){animation-duration:var(--dur-troca)}
```

Detalhes que importam: o nome vai na `<img>`, não no card, para o morph ser foto com foto. Nome duplicado na mesma página cancela a transição inteira, então a convenção é `capa-` + número da matéria. Card sem par na página de destino apenas sai no fade da raiz, sem custo visível. Funciona em Chrome, Edge e Safari 18.2+; Firefox navega normal. Reduced motion: já resolvido pelo `@view-transition{navigation:none}` existente, nenhuma linha a mais.

---

## 3. Mola física em JS puro

Uma mola para o portal inteiro: rigidez 220, amortecimento 26 (fator 0,88, um leve overshoot e assenta em ~300ms). API de uma função: `mola(elemento, escalaAlvo)`. Re-alvejar no meio do movimento não pula, que é o motivo de existir. Entra em `visual.js`:

```js
/* MOLA | mola(el, alvo) leva scale ate o alvo com fisica de mola.
   Interrompivel no meio sem pulo. Reduced motion: vai direto, sem animar. */
var mola = (function () {
  var RIGIDEZ = 220, AMORTECIMENTO = 26, ativas = new WeakMap();
  var reduzido = window.matchMedia('(prefers-reduced-motion: reduce)');
  return function (el, alvo) {
    if (reduzido.matches) {
      el.style.transform = alvo === 1 ? '' : 'scale(' + alvo + ')';
      return;
    }
    var s = ativas.get(el);
    if (!s) { s = { x: 1, v: 0, alvo: alvo, quadro: 0, antes: 0 }; ativas.set(el, s); }
    s.alvo = alvo;
    if (s.quadro) return;                     /* ja esta andando: so muda o alvo */
    s.antes = performance.now();
    s.quadro = requestAnimationFrame(function anda(agora) {
      var dt = Math.min((agora - s.antes) / 1000, 1 / 30);
      s.antes = agora;
      var forca = -RIGIDEZ * (s.x - s.alvo) - AMORTECIMENTO * s.v;
      s.v += forca * dt;
      s.x += s.v * dt;
      if (Math.abs(s.x - s.alvo) < .001 && Math.abs(s.v) < .001) {
        s.x = s.alvo; s.v = 0; s.quadro = 0;
        el.style.transform = s.alvo === 1 ? '' : 'scale(' + s.alvo + ')';
        return;
      }
      el.style.transform = 'scale(' + s.x + ')';
      s.quadro = requestAnimationFrame(anda);
    });
  };
})();

/* fiacao: aperto encolhe, soltura volta com a mola */
(function () {
  var ALVOS = '.chip,.signo,.carrossel-btn,.carrossel-pontos button,.carrossel-pausa,.pausa-anima';
  var preso = null;
  document.addEventListener('pointerdown', function (e) {
    preso = e.target.closest(ALVOS);
    if (preso) mola(preso, .94);
  });
  function solta() { if (preso) { mola(preso, 1); preso = null; } }
  document.addEventListener('pointerup', solta);
  document.addEventListener('pointercancel', solta);
})();
```

Só `transform: scale`, nunca opacity nem layout. O `WeakMap` deixa o coletor limpar molas de elementos removidos. Teclado não precisa da mola: `:focus-visible` já responde por CSS.

---

## 4. Por que Lenis (e qualquer smooth scroll) é a escolha errada aqui

Leitor de notícia rola para escanear, e scroll sequestrado põe latência entre o dedo e o texto em cada gesto da visita. Lenis reimplementa a rolagem no main thread via rAF, exatamente a thread que anúncio e imagem já disputam num celular intermediário: o resultado é jitter onde hoje há compositor liso. Quebra de graça o que é nativo: momentum do iOS, buscar na página, âncora, barra do sistema, leitor de tela. É dependência externa, vetada pela Constituição, e uma versão caseira herda todos os defeitos sem a manutenção. Todo movimento de rolagem que o site quer já sai das scroll-driven animations sobre rolagem nativa, com custo zero de main thread.

---

## 5. Consolidação do prefers-reduced-motion

Três mecanismos cobrem tudo, e cada receita acima já nasceu dentro deles:

1. **Kill switch global** (estilo.css linha 494): `*{animation:none!important;transition:none!important}` derruba reveal, parallax e cascata. Princípio novo que torna isso seguro sem lista de restauração: **estado inicial invisível mora sempre no `from` do keyframe, nunca na regra do elemento**. Com a migração da receita 2.1, a lista da linha 498 encolhe (`.rv-on .rv` sai).
2. **View transitions**: `@view-transition{navigation:none}` já existe (linha 24). Nada a acrescentar.
3. **JS**: contador e mola consultam `matchMedia('(prefers-reduced-motion: reduce)')` e entregam o estado final direto, como o carrossel já faz.

Arquivos tocados: `/Users/viniciusdelego/Documents/santainforma/estilo.css` (tokens no `:root`, receitas 2.1, 2.2, 2.5, regra `.cascata`, `tabular-nums`, remoção das regras `.rv`) e `/Users/viniciusdelego/Documents/santainforma/visual.js` (remoção das linhas 4 e 67-118, entrada do contador e da mola). Nenhum arquivo novo, nenhuma dependência, e sem JS ou sem suporte o site fica idêntico ao de hoje: tudo visível, nada esperando efeito.