/* SANTA INFORMA | movimento discreto e relogio | v1.2
   Regra de ouro: o conteudo nunca depende do efeito para aparecer.
   Sem JS, sem IntersectionObserver ou com ele falhando, tudo fica visivel. */
document.documentElement.classList.add('rv-on');

/* RELOGIO DO SITE
   So marca com data-agora o que significa "neste momento". Data de
   publicacao de materia e data de versao de documento legal ficam fixas
   no HTML de proposito: elas nao podem andar sozinhas.
   O fuso e fixado em Brasilia para que a hora exibida seja sempre a da
   redacao, e nao a do aparelho de quem le de fora do Brasil. */
(function () {
  var ZONA = 'America/Sao_Paulo';

  function temIntl() {
    try { return !!(window.Intl && Intl.DateTimeFormat().resolvedOptions().timeZone); }
    catch (e) { return false; }
  }

  function maiuscula(t) { return t.charAt(0).toUpperCase() + t.slice(1); }

  function texto(modo, agora) {
    var opc = { timeZone: ZONA, day: 'numeric', month: 'long', year: 'numeric' };
    if (modo === 'completo') opc.weekday = 'long';
    var data = maiuscula(new Intl.DateTimeFormat('pt-BR', opc).format(agora));
    if (modo !== 'completo') return data;
    var hora = new Intl.DateTimeFormat('pt-BR', {
      timeZone: ZONA, hour: '2-digit', minute: '2-digit', hour12: false
    }).format(agora).replace(':', 'h');
    return data + ' · ' + hora;
  }

  function pintar() {
    var alvos = document.querySelectorAll('[data-agora]');
    if (!alvos.length) return;
    var agora = new Date();
    for (var i = 0; i < alvos.length; i++) {
      var el = alvos[i];
      var novo = texto(el.getAttribute('data-agora'), agora);
      if (el.textContent !== novo) el.textContent = novo;   /* evita repintura a toa */
      if (el.tagName === 'TIME') el.setAttribute('datetime', agora.toISOString());
    }
  }

  /* acerta no virar do minuto, para nao exibir hora atrasada */
  function agendar() {
    setTimeout(function () { pintar(); agendar(); }, 60000 - (Date.now() % 60000) + 60);
  }

  function iniciar() {
    if (!temIntl()) return;            /* sem Intl, fica o valor escrito no HTML */
    pintar();
    agendar();
    /* voltou para a aba depois de horas: acerta na hora, sem esperar o minuto */
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) pintar();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', iniciar);
  } else {
    iniciar();
  }
})();

document.addEventListener('DOMContentLoaded', function () {
  var alvos = [].slice.call(
    document.querySelectorAll('article.card,figure.foto,.d,.item,.destaque,.patro'));
  if (!alvos.length) return;

  function revelar(el, atraso) {
    if (el.classList.contains('vis')) return;
    if (atraso) el.style.transitionDelay = atraso + 'ms';
    el.classList.add('vis');
  }
  function revelarTudo() {
    for (var i = 0; i < alvos.length; i++) revelar(alvos[i]);
  }

  var reduzido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduzido || !('IntersectionObserver' in window)) { revelarTudo(); return; }

  for (var j = 0; j < alvos.length; j++) alvos[j].classList.add('rv');

  /* o que ja esta na primeira tela entra sem esperar rolagem */
  function revelarVisiveis() {
    var alt = window.innerHeight || 800, algum = false;
    for (var i = 0; i < alvos.length; i++) {
      var r = alvos[i].getBoundingClientRect();
      if (r.top < alt * 0.92 && r.bottom > 0) { revelar(alvos[i]); algum = true; }
    }
    return algum;
  }
  revelarVisiveis();

  var obs = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (!e.isIntersecting) return;
      var irmaos = [].slice.call(e.target.parentNode.children);
      revelar(e.target, Math.min(irmaos.indexOf(e.target), 5) * 70);
      obs.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });

  for (var k = 0; k < alvos.length; k++) obs.observe(alvos[k]);

  /* rede 1: se a rolagem acontecer e o observer nao responder, resolvemos na mao */
  var pendente = false;
  window.addEventListener('scroll', function () {
    if (pendente) return;
    pendente = true;
    requestAnimationFrame(function () { pendente = false; revelarVisiveis(); });
  }, { passive: true });

  /* rede 2: em qualquer cenario, nada fica escondido depois de 2s */
  setTimeout(revelarTudo, 2000);
});

/* CARROSSEL
   Progressivo: sem este script a faixa ja rola no dedo e no teclado.
   Ele so acrescenta setas e marcacao de posicao. */
document.addEventListener('DOMContentLoaded', function () {
  var caixa = document.querySelector('.carrossel');
  if (!caixa) return;
  var trilho = caixa.querySelector('.carrossel-trilho');
  var slides = [].slice.call(trilho.children);
  if (slides.length < 2) return;
  caixa.classList.add('js-carrossel');

  var ant = caixa.querySelector('.carrossel-btn.ant');
  var pro = caixa.querySelector('.carrossel-btn.pro');
  var pontos = caixa.querySelector('.carrossel-pontos');

  /* quem pediu menos movimento nao deve receber rolagem deslizante */
  var suave = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';

  slides.forEach(function (s, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.setAttribute('aria-label', 'Ir para o destaque ' + (i + 1));
    b.addEventListener('click', function () {
      trilho.scrollTo({ left: s.offsetLeft - trilho.offsetLeft, behavior: suave });
    });
    pontos.appendChild(b);
  });
  var bolinhas = [].slice.call(pontos.children);

  function passo() { return slides[0].getBoundingClientRect().width + 22; }
  ant.addEventListener('click', function () { trilho.scrollBy({ left: -passo(), behavior: suave }); });
  pro.addEventListener('click', function () { trilho.scrollBy({ left: passo(), behavior: suave }); });

  var pendente = false;
  function situacao() {
    var i = Math.round(trilho.scrollLeft / passo());
    for (var k = 0; k < bolinhas.length; k++)
      bolinhas[k].setAttribute('aria-current', k === i ? 'true' : 'false');
    /* desabilitar em vez de esconder: escondido tira o foco do teclado */
    ant.disabled = trilho.scrollLeft < 8;
    pro.disabled = trilho.scrollLeft + trilho.clientWidth >= trilho.scrollWidth - 8;
  }
  trilho.addEventListener('scroll', function () {
    if (pendente) return;
    pendente = true;
    requestAnimationFrame(function () { pendente = false; situacao(); });
  }, { passive: true });
  situacao();

  /* AVANCO AUTOMATICO
     Conteudo que anda sozinho por mais de cinco segundos precisa de um jeito de
     parar (WCAG 2.2.2). Aqui sao quatro: o botao, o mouse em cima, o foco do
     teclado dentro e qualquer toque na faixa. Quem pediu menos movimento nunca
     ve o carrossel andar. */
  var reduzido = window.matchMedia('(prefers-reduced-motion: reduce)');
  var INTERVALO = 6000;
  var relogio = null;
  var parado = reduzido.matches;   /* comeca parado para quem pediu menos movimento */
  var desistiu = false;            /* o leitor mexeu: nao volta a andar sozinho */

  function proximo() {
    /* chegou no fim: volta ao comeco em vez de travar */
    var fim = trilho.scrollLeft + trilho.clientWidth >= trilho.scrollWidth - 8;
    trilho.scrollTo({ left: fim ? 0 : trilho.scrollLeft + passo(), behavior: 'smooth' });
  }
  function toca() {
    if (relogio || parado || desistiu || reduzido.matches) return;
    relogio = setInterval(proximo, INTERVALO);
  }
  function pausa() {
    if (relogio) { clearInterval(relogio); relogio = null; }
  }

  var bp = document.createElement('button');
  bp.type = 'button';
  bp.className = 'carrossel-pausa';
  function rotulo() {
    var andando = !!relogio;
    bp.setAttribute('aria-pressed', andando ? 'false' : 'true');
    bp.textContent = andando ? 'Pausar' : 'Reproduzir';
    bp.setAttribute('aria-label', andando ? 'Pausar o giro dos destaques' : 'Reproduzir o giro dos destaques');
  }
  bp.addEventListener('click', function () {
    parado = !parado;
    desistiu = false;              /* pedir play desfaz a desistencia */
    if (parado) pausa(); else toca();
    rotulo();
  });
  pontos.parentNode.insertBefore(bp, pontos.nextSibling);

  /* mouse e teclado seguram o giro sem cancelar a preferencia */
  caixa.addEventListener('mouseenter', pausa);
  caixa.addEventListener('mouseleave', function () { if (!parado) toca(); });
  caixa.addEventListener('focusin', pausa);
  caixa.addEventListener('focusout', function () {
    if (!caixa.contains(document.activeElement) && !parado) toca();
  });

  /* mexeu na faixa com o dedo ou clicou numa seta: o leitor assumiu o controle */
  function assumiu() { desistiu = true; pausa(); rotulo(); }
  trilho.addEventListener('pointerdown', assumiu);
  trilho.addEventListener('wheel', assumiu, { passive: true });
  ant.addEventListener('click', assumiu);
  pro.addEventListener('click', assumiu);
  bolinhas.forEach(function (b) { b.addEventListener('click', assumiu); });

  /* aba escondida nao precisa girar */
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) pausa(); else if (!parado) toca();
  });

  /* mudou a preferencia no sistema no meio da sessao */
  var ouvir = reduzido.addEventListener ? 'addEventListener' : 'addListener';
  reduzido[ouvir]('change', function () {
    if (reduzido.matches) { parado = true; pausa(); } else { parado = false; toca(); }
    rotulo();
  });

  toca();
  rotulo();
});

/* PAUSAR CENA ANIMADA
   A 2.2.2 pede um controle no proprio conteudo, e nao so a preferencia do
   sistema. Aparece somente onde ha cena animada. */
document.addEventListener('DOMContentLoaded', function () {
  var cenas = document.querySelectorAll('.anima');
  for (var i = 0; i < cenas.length; i++) {
    (function (cena) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'pausa-anima';
      b.setAttribute('aria-pressed', 'false');
      b.textContent = 'Pausar animação';
      b.addEventListener('click', function () {
        var parado = cena.classList.toggle('pausada');
        b.setAttribute('aria-pressed', parado ? 'true' : 'false');
        b.textContent = parado ? 'Retomar animação' : 'Pausar animação';
      });
      var fig = cena.closest('figure') || cena.parentNode;
      fig.appendChild(b);
    })(cenas[i]);
  }
});

/* PUBLICIDADE
   O AdSense marca o <ins> com data-ad-status quando decide o que fazer:
   "filled" quando serviu anuncio, "unfilled" quando nao tinha o que servir.
   Antes da conta ser aprovada ele nao marca nada. O rotulo "Publicidade" so
   faz sentido quando ha anuncio, entao ele espera esse sinal.
   Sem JS o rotulo nao aparece, e o anuncio aparece do mesmo jeito: o
   conteudo nunca depende do efeito. */
document.addEventListener('DOMContentLoaded', function () {
  var blocos = document.querySelectorAll('.pub-google');
  if (!blocos.length) return;

  function conferir() {
    var pendentes = 0;
    for (var i = 0; i < blocos.length; i++) {
      var ins = blocos[i].querySelector('ins.adsbygoogle');
      if (!ins) continue;
      var st = ins.getAttribute('data-ad-status');
      if (st === 'filled') blocos[i].classList.add('tem-anuncio');
      else if (st !== 'unfilled') pendentes++;
    }
    return pendentes;
  }

  if (!conferir()) return;
  /* o anuncio chega depois do carregamento: olha de novo por 10 segundos */
  var voltas = 0;
  var relogio = setInterval(function () {
    if (!conferir() || ++voltas > 20) clearInterval(relogio);
  }, 500);
});

/* CEU POR HORA
   A classe no <html> vale em toda pagina: e ela que faz o sol da marca
   virar lua a noite em todo o site. O FUNDO de ceu, esse sim, so aparece
   onde existe header.ceu (a capa). Sem Intl ou com erro, nada muda. */
document.addEventListener('DOMContentLoaded', function () {
  var ZONA = 'America/Sao_Paulo';

  function horaBrasilia() {
    try {
      return parseInt(new Intl.DateTimeFormat('pt-BR', {
        timeZone: ZONA, hour: 'numeric', hour12: false
      }).format(new Date()), 10);
    } catch (e) { return null; }
  }
  function estadoDaHora(h) {
    if (h === null) return null;
    if (h >= 19 || h < 5) return 'noite';
    if (h < 8) return 'amanhecer';
    if (h < 17) return 'dia';
    return 'entardecer';
  }
  function aplicar() {
    var estado = estadoDaHora(horaBrasilia());
    if (!estado) return;
    var raiz = document.documentElement;
    raiz.className = raiz.className.replace(/\bceu-\S+/g, '').trim();
    raiz.classList.add('ceu-' + estado);
  }
  function tique() {
    aplicar();
    setTimeout(tique, 60000 - (Date.now() % 60000) + 120);
  }
  tique();
});

/* PAUSA DAS ONDAS DO HORIZONTE
   Conteudo que anda sozinho tem botao de parar (WCAG 2.2.2). */
document.addEventListener('DOMContentLoaded', function () {
  var faixa = document.querySelector('.horizonte');
  var botao = faixa && faixa.querySelector('.onda-pausa');
  if (!botao) return;
  botao.addEventListener('click', function () {
    var parou = faixa.classList.toggle('pausada');
    botao.setAttribute('aria-pressed', parou ? 'true' : 'false');
    botao.textContent = parou ? 'Retomar ondas' : 'Pausar ondas';
  });
});

/* MOLA FISICA
   mola(el, alvo) leva scale ate o alvo com fisica de mola, interrompivel
   no meio sem pulo. Menos movimento: vai direto ao estado final. */
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
    if (s.quadro) return;                    /* ja anda: so muda o alvo */
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

/* fiacao da mola: aperto encolhe, soltura devolve. Botoes de interface
   encolhem mais; chamadas de materia, quase nada. Teclado nao precisa:
   o :focus-visible ja responde por CSS. */
(function () {
  var BOTOES = '.chip,.signo,.carrossel-btn,.carrossel-pontos button,.carrossel-pausa,.pausa-anima,.onda-pausa';
  var CARTOES = '.manchete,.sub,.lider-sec,.pilha article,article.card.v2';
  var preso = null;
  document.addEventListener('pointerdown', function (e) {
    var b = e.target.closest(BOTOES);
    if (b) { preso = b; mola(b, .94); return; }
    var c = e.target.closest(CARTOES);
    if (c) { preso = c; mola(c, .985); }
  });
  function solta() { if (preso) { mola(preso, 1); preso = null; } }
  document.addEventListener('pointerup', solta);
  document.addEventListener('pointercancel', solta);
})();

/* VOO DE CAPA
   No clique rumo a uma materia, a imagem da chamada ganha o nome de
   view transition daquela materia. Quando o modelo de materia nomear a
   foto de topo com o mesmo capa-mNN (fase 2), a imagem viaja de uma
   pagina a outra. Ate la, nada muda: o fade atual continua. */
document.addEventListener('click', function (e) {
  var a = e.target.closest('a[href*="materia-"]');
  if (!a || !('startViewTransition' in document)) return;
  var bloco = a.closest('article,aside,li,div');
  var img = bloco && bloco.querySelector('img');
  var n = (a.getAttribute('href').match(/materia-(\d+)/) || [])[1];
  if (img && n) img.style.viewTransitionName = 'capa-m' + n;
});

/* TEMPO DA REGIAO
   Depois que a pagina carrega, pergunta ao /clima (funcao no edge; ver
   functions/clima.js) como esta o ceu de quem le e aplica tempo-<estado>
   no <html>. O CSS faz o resto: veu no gradiente, fios de chuva, nevoa.
   Em QUALQUER erro, silencio absoluto: o site fica com o ceu por hora.
   O editor testa com ?tempo=chuva (limpo, nublado, neblina, chuva, neve,
   temporal); o modo de teste carimba um selo "simulacao" no horizonte,
   para print de temporal forcado nunca circular como se fosse real. */
window.addEventListener('load', function () {
  var ESTADOS = ['limpo', 'nublado', 'neblina', 'chuva', 'neve', 'temporal'];
  function aplicar(estado) {
    if (ESTADOS.indexOf(estado) < 0) return;   /* invalido: nada muda */
    var raiz = document.documentElement;
    raiz.className = raiz.className.replace(/\btempo-(?!simulado)\S+/g, '').trim();
    raiz.classList.add('tempo-' + estado);
  }
  var teste = new URLSearchParams(location.search).get('tempo');
  if (teste) {
    aplicar(teste);
    document.documentElement.classList.add('tempo-simulado');
    var faixa = document.querySelector('.horizonte');
    if (faixa && !faixa.querySelector('.selo-simulacao')) {
      var selo = document.createElement('span');
      selo.className = 'selo-simulacao';
      selo.textContent = 'simulação';
      faixa.appendChild(selo);
    }
    return;
  }
  /* lembra so a PALAVRA do estado por 30 min, nunca coordenada */
  try {
    var guardado = JSON.parse(sessionStorage.getItem('clima') || 'null');
    if (guardado && Date.now() - guardado.quando < 1800000) {
      aplicar(guardado.estado);
      return;
    }
  } catch (e) { /* storage bloqueado: segue para a rede */ }
  var corte = new AbortController();
  setTimeout(function () { corte.abort(); }, 3000);
  fetch('/clima', { signal: corte.signal })
    .then(function (r) { return r.status === 200 ? r.json() : null; })
    .then(function (d) {
      if (!d || !d.estado) return;
      try {
        sessionStorage.setItem('clima', JSON.stringify({ estado: d.estado, quando: Date.now() }));
      } catch (e) { /* sem storage, so nao lembra */ }
      aplicar(d.estado);
    })
    .catch(function () { /* sem clima, sem drama */ });
});

/* NAVEGACAO ROLAVEL
   As barras de menu e a paginacao abrem em scrollLeft 0, entao quem
   entra em Meio Ambiente ve so as tres primeiras editorias e nunca o
   destaque de onde esta. Rola SO a barra, nunca a pagina, e sem
   animacao: nada de CLS, nada de rolagem inesperada.
   Usa getBoundingClientRect de proposito: o li da barra e position
   relative (camada de clique do celular), entao offsetLeft daria zero. */
document.addEventListener('DOMContentLoaded', function () {
  function centraliza(caixa, alvo) {
    if (!caixa || !alvo || caixa.scrollWidth <= caixa.clientWidth) return;
    var a = alvo.getBoundingClientRect(), c = caixa.getBoundingClientRect();
    var antes = caixa.style.scrollBehavior;
    caixa.style.scrollBehavior = 'auto';     /* o html tem scroll-behavior smooth */
    caixa.scrollLeft += (a.left - c.left) - (caixa.clientWidth - a.width) / 2;
    caixa.style.scrollBehavior = antes;
  }
  var barras = document.querySelectorAll('nav ul');
  for (var i = 0; i < barras.length; i++) {
    centraliza(barras[i], barras[i].querySelector('a.ativo'));
  }
  var nums = document.querySelector('.paginacao .numeros');
  if (nums) centraliza(nums, nums.querySelector('[aria-current]'));
});
