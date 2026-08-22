/* GET /clima
   Funcao do Cloudflare Pages, sem build: este arquivo em functions/ vira a
   rota /clima sozinho. Ela existe para o ceu da capa refletir o tempo da
   regiao de quem le, discretamente, como o app de clima do celular.

   Privacidade, nas regras da casa: a posicao aproximada vem do request.cf,
   dado que a Cloudflare ja tem por entregar o site. A coordenada e
   arredondada para 1 casa decimal (celula de ~11 km) antes de qualquer
   consulta. O IP do leitor nunca sai daqui; nada e gravado; nada se liga
   ao leitor. A fonte meteorologica e o instituto noruegues MET Norway
   (api.met.no), gratuito tambem para uso comercial, mediante User-Agent
   identificado e atribuicao (feita na privacidade.html).

   Regra dura de degradacao: SEM COORDENADA, SEM CLIMA. Qualquer falha
   responde 204 sem corpo, e o site fica com o ceu por hora de sempre.
   Proibido cair para uma cidade padrao: temporal de Itapema na tela de
   um leitor de Chapeco seria mentira visual.

   O ciclo automatico de noticias NAO toca neste arquivo. */

var TTL = 900; /* 15 min de cache, por celula de coordenada */

/* symbol_code do met.no -> vocabulario minimo do site.
   O sufixo _day/_night/_polartwilight e descartado: quem manda em
   dia/noite e o relogio do ceu que o site ja tem (um dono so). */
function traduz(simbolo) {
  if (!simbolo) return null;
  var s = String(simbolo).split('_')[0];
  if (s === 'clearsky' || s === 'fair') return 'limpo';
  if (s === 'partlycloudy' || s === 'cloudy') return 'nublado';
  if (s === 'fog') return 'neblina';
  if (s.indexOf('thunder') >= 0) return 'temporal';
  if (s.indexOf('snow') >= 0) return 'neve';
  if (s.indexOf('rain') >= 0 || s.indexOf('sleet') >= 0 || s.indexOf('drizzle') >= 0) return 'chuva';
  return null;
}

function nada() { return new Response(null, { status: 204 }); }

export async function onRequestGet(context) {
  try {
    var cf = context.request.cf;
    var lat = cf && parseFloat(cf.latitude);
    var lon = cf && parseFloat(cf.longitude);
    if (!isFinite(lat) || !isFinite(lon)) return nada();
    lat = lat.toFixed(1);
    lon = lon.toFixed(1);

    /* cache de borda por celula; a chave e uma URL sintetica que nunca e
       servida a ninguem, so identifica a celula de 0,1 grau */
    var cache = caches.default;
    var chave = new Request('https://cache-clima.santainforma.com.br/v1/' + lat + ',' + lon);
    var guardado = await cache.match(chave);
    var estado;

    if (guardado) {
      estado = (await guardado.json()).estado;
    } else {
      var corte = new AbortController();
      var relogio = setTimeout(function () { corte.abort(); }, 4000);
      var r = await fetch(
        'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=' + lat + '&lon=' + lon,
        {
          signal: corte.signal,
          headers: {
            /* exigencia de uso do met.no: identificar quem consulta */
            'User-Agent': 'santainforma.com.br ceu-da-capa vl7producoes@gmail.com'
          }
        }
      );
      clearTimeout(relogio);
      if (!r.ok) return nada();
      var dado = await r.json();
      var serie = dado && dado.properties && dado.properties.timeseries && dado.properties.timeseries[0];
      var passo = serie && serie.data;
      var resumo = passo && ((passo.next_1_hours && passo.next_1_hours.summary) ||
                            (passo.next_6_hours && passo.next_6_hours.summary));
      estado = traduz(resumo && resumo.symbol_code);
      if (!estado) return nada();
      context.waitUntil(cache.put(chave, new Response(JSON.stringify({ estado: estado }), {
        headers: { 'Cache-Control': 'public, max-age=' + TTL }
      })));
    }
    if (!estado) return nada();
    /* a cidade sai do request de quem pediu, nunca do cache: a celula de
       11 km pode abracar Itapema e Porto Belo ao mesmo tempo */
    return new Response(JSON.stringify({ estado: estado, cidade: (cf && cf.city) || null }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, s-maxage=' + TTL + ', max-age=600'
      }
    });
  } catch (e) {
    return nada();
  }
}
