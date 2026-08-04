/* SANTA INFORMA | movimento discreto | v1.1
   Regra de ouro: o conteudo nunca depende do efeito para aparecer.
   Sem JS, sem IntersectionObserver ou com ele falhando, tudo fica visivel. */
document.documentElement.classList.add('rv-on');

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
