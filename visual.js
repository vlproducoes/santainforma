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
