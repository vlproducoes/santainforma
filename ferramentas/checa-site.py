# -*- coding: utf-8 -*-
"""Checagem de sanidade das paginas do site. Nao altera nada.

    python3 ferramentas/checa-site.py

E a lista do passo 7 do ciclo de noticias virando codigo: se algo aqui
reprova, a materia nao vai ao ar. Sai com codigo 1 quando acha problema.
"""
import glob, json, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANALYTICS = 'G-PQKY68PE07'

# Tags que precisam abrir e fechar na conta certa.
PARES = ['main', 'section', 'div', 'article', 'figure', 'ul', 'table',
         'time', 'ins', 'script']
# Estas o HTML permite fechar sozinho em alguns casos, entao so reprova
# quando fecha mais do que abre, que e erro de verdade.
FROUXAS = ['p', 'li', 'a', 'span']

CAMPOS_JSONLD = ['headline', 'description', 'datePublished', 'dateModified',
                 'author', 'image', 'publisher', 'mainEntityOfPage']


def checa():
    os.chdir(BASE)
    erros = []
    paginas = sorted(glob.glob('*.html'))

    for f in paginas:
        s = open(f, encoding='utf-8').read()
        def e(msg):
            erros.append(f'{f}: {msg}')

        # cabecalho obrigatorio de toda pagina
        if '<title>' not in s: e('sem <title>')
        if 'name="description"' not in s: e('sem meta description')
        if 'rel="canonical"' not in s: e('sem canonical')
        if 'property="og:title"' not in s: e('sem Open Graph')
        if ANALYTICS not in s: e(f'sem Analytics {ANALYTICS}')
        if 'anuncie.html' not in s: e('sem link para anuncie.html')

        n = len(re.findall(r'<h1[\s>]', s))
        if n != 1: e(f'{n} <h1> na pagina, tem que ser exatamente 1')

        for t in PARES:
            ab, fe = len(re.findall(r'<%s[\s>]' % t, s)), len(re.findall(r'</%s>' % t, s))
            if ab != fe: e(f'<{t}> desbalanceada ({ab} abre / {fe} fecha)')
        for t in FROUXAS:
            ab, fe = len(re.findall(r'<%s[\s>]' % t, s)), len(re.findall(r'</%s>' % t, s))
            if fe > ab: e(f'</{t}> fecha mais do que abre ({ab}/{fe})')

        # travessao e proibido no conteudo (CLAUDE.md, secao 3)
        corpo = re.sub(r'<script.*?</script>', '', s, flags=re.S)
        corpo = re.sub(r'<style.*?</style>', '', corpo, flags=re.S)
        if '\u2014' in corpo or '&mdash;' in corpo: e('travessao no conteudo')

        for bloco in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                d = json.loads(bloco)
            except Exception as ex:
                e(f'JSON-LD invalido: {ex}')
                continue
            if not (isinstance(d, dict) and d.get('@type') == 'NewsArticle'):
                continue
            for c in CAMPOS_JSONLD:
                if not d.get(c): e(f'JSON-LD sem {c}')
            for c in ('datePublished', 'dateModified'):
                v = d.get(c)
                if v and not re.match(r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d-03:00$', v):
                    e(f'{c} sem hora ou fuso: {v}')
            for u in (d.get('image') or []):
                cam = u.replace('https://santainforma.com.br/', '')
                if not os.path.exists(cam): e(f'imagem do JSON-LD nao existe no disco: {cam}')

        for tag in re.findall(r'<img\b[^>]*>', s):
            for at in ('width=', 'height=', 'loading=', 'alt='):
                if at not in tag: e(f'<img> sem {at[:-1]}: {tag[:70]}')
            m = re.search(r'alt="([^"]*)"', tag)
            if m and len(m.group(1)) < 15:
                e(f'alt curto demais, nao descreve a foto: {m.group(1)!r}')

        # data de publicacao e fixa, nunca relogio
        for q in re.findall(r'<span class="quando">.*?</span>', s, re.S):
            if 'data-agora' in q: e('data-agora dentro de span.quando')

        if 'class="pub-google"' in s and not f.startswith('materia-'):
            e('bloco .pub-google fora de pagina de materia')

        for href in re.findall(r'href="([^"#?][^"]*?)"', s):
            if href.startswith(('http', 'mailto:', 'tel:', '//')):
                continue
            alvo = href.split('#')[0].split('?')[0]
            if alvo and not os.path.exists(alvo): e(f'link interno quebrado: {href}')

    css = open('estilo.css', encoding='utf-8').read()
    if css.count('{') != css.count('}'):
        erros.append(f'estilo.css: chaves desbalanceadas ({css.count("{")}/{css.count("}")})')

    return paginas, erros


if __name__ == '__main__':
    paginas, erros = checa()
    print(f'{len(paginas)} páginas checadas')
    if erros:
        print(f'{len(erros)} PROBLEMAS:')
        for x in erros:
            print('  -', x)
        sys.exit(1)
    print('tudo certo')
