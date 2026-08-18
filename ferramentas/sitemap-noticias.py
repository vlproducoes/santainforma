# -*- coding: utf-8 -*-
"""Gera o sitemap de noticias do Google.

    python3 ferramentas/sitemap-noticias.py

O Google News so aceita materia publicada nas ULTIMAS 48 HORAS neste
sitemap. Materia mais velha que isso precisa sair, senao o Google reclama.
Por isso este script roda a cada publicacao, junto do deploy.

Le a data direto do JSON-LD de cada materia, que e a fonte da verdade.
"""
import glob, json, re, os
from datetime import datetime, timedelta, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://santainforma.com.br'
NOME = 'Santa Informa'
JANELA_HORAS = 48

def escapa(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))

def monta():
    agora = datetime.now(timezone.utc)
    corte = agora - timedelta(hours=JANELA_HORAS)
    recentes = []
    for f in sorted(glob.glob(f'{BASE}/materia-*.html')):
        s = open(f, encoding='utf-8').read()
        m = re.search(r'ld\+json">\n(.*?)\n</script>', s, re.S)
        if not m: continue
        d = json.loads(m.group(1))
        if d.get('@type') != 'NewsArticle': continue
        try:
            quando = datetime.fromisoformat(d['datePublished'])
        except ValueError:
            continue
        if quando.tzinfo is None:
            quando = quando.replace(tzinfo=timezone(timedelta(hours=-3)))
        if quando >= corte:
            recentes.append((quando, os.path.basename(f), d['headline']))
    recentes.sort(reverse=True)

    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
         '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    for quando, arq, titulo in recentes:
        o += ['', '  <url>',
              f'    <loc>{SITE}/{arq}</loc>',
              '    <news:news>',
              '      <news:publication>',
              f'        <news:name>{NOME}</news:name>',
              '        <news:language>pt</news:language>',
              '      </news:publication>',
              f'      <news:publication_date>{quando.isoformat()}</news:publication_date>',
              f'      <news:title>{escapa(titulo)}</news:title>',
              '    </news:news>',
              '  </url>']
    o += ['', '</urlset>', '']
    open(f'{BASE}/sitemap-noticias.xml', 'w', encoding='utf-8').write('\n'.join(o))
    return recentes

if __name__ == '__main__':
    r = monta()
    print(f'  sitemap-noticias.xml: {len(r)} matérias das últimas {JANELA_HORAS}h')
    for quando, arq, titulo in r:
        print(f'    {quando:%d/%m %Hh%M}  {titulo[:58]}')
