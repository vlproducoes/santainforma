"""Instala foto de divulgacao oficial numa materia ja publicada.

Regra da casa (Constituicao, secao 6): divulgacao oficial entra com credito
completo, com o orgao e o ano. Nunca so "Divulgacao". Foto de portal de
noticia nunca entra.

Registra a origem em imagens/creditos.json igual ao script do Pexels, para
a procedencia de toda imagem do site ficar num lugar so.
"""
import json, os, re, subprocess, sys
from PIL import Image, ImageOps

BASE = '/Users/viniciusdelego/Documents/santainforma'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Santa Informa/1.0'


def baixa(url, destino, referer=None):
    cmd = ['curl', '-sL', '--max-time', '60', '-A', UA]
    if referer:
        cmd += ['-e', referer]
    cmd += [url, '-o', destino, '-w', '%{http_code}']
    cod = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
    if cod != '200':
        raise SystemExit(f'{url}: HTTP {cod}')
    return destino


def instala(nome, url, orgao, ano, referer=None, pagina=None, corte=(0.5, 0.42), autor=None):
    """Baixa, recorta para 16:9, gera webp e miniaturas, registra a origem."""
    bruto = f'/tmp/_of_{nome}.bin'
    baixa(url, bruto, referer)
    im = Image.open(bruto)
    im.load()
    orig = im.size
    im = im.convert('RGB')

    grande = ImageOps.fit(im, (1600, 900), Image.LANCZOS, centering=corte)
    grande.save(f'{BASE}/imagens/{nome}.jpg', 'JPEG', quality=86, optimize=True, progressive=True)
    grande.save(f'{BASE}/imagens/webp/{nome}.webp', 'WEBP', quality=78, method=6)
    grande.resize((800, 450), Image.LANCZOS).save(
        f'{BASE}/imagens/webp/{nome}-800.webp', 'WEBP', quality=78, method=6)

    cred = f'Foto: {orgao}/Divulgação, {ano}'
    if autor:
        cred = f'Foto: {autor}/{orgao}, {ano}'

    p = f'{BASE}/imagens/creditos.json'
    reg = json.load(open(p, encoding='utf-8'))
    reg[f'{nome}.jpg'] = {
        'origem': 'divulgacao oficial',
        'orgao': orgao,
        'autor': autor,
        'ano': ano,
        'licenca': 'material de divulgacao de orgao publico, reproduzido com credito',
        'uso': 'registro do fato',
        'url_original': url,
        'pagina_da_fonte': pagina,
        'dimensao_original': f'{orig[0]}x{orig[1]}',
        'baixada_em': subprocess.run(['date', '+%Y-%m-%d'], capture_output=True, text=True).stdout.strip(),
    }
    json.dump(reg, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    os.remove(bruto)
    print(f'  {nome}: {orig[0]}x{orig[1]} -> 1600x900 · crédito "{cred}"')
    return cred


def miniaturas(n, nome):
    """Gera o card e a miniatura quadrada da materia numero n."""
    im = Image.open(f'{BASE}/imagens/{nome}.jpg').convert('RGB')
    ImageOps.fit(im, (720, 405), Image.LANCZOS).save(
        f'{BASE}/imagens/miniaturas/m{n:02d}-card.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
    ImageOps.fit(im, (160, 160), Image.LANCZOS, centering=(.5, .42)).save(
        f'{BASE}/imagens/miniaturas/m{n:02d}-mini.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
    print(f'  miniaturas m{n:02d} regeradas')


def troca(arquivo, nome_novo, alt, legenda, credito):
    """Substitui a figura de topo da materia, preservando o resto."""
    p = f'{BASE}/{arquivo}'
    s = open(p, encoding='utf-8').read()
    m = re.search(r'  <figure class="foto">.*?</figure>\n', s, re.S)
    if not m:
        raise SystemExit(f'{arquivo}: sem figura de topo')
    nova = (f'  <figure class="foto">\n'
            f'    <picture><source type="image/webp" '
            f'srcset="imagens/webp/{nome_novo}-800.webp 800w, imagens/webp/{nome_novo}.webp 1600w" '
            f'sizes="(max-width: 760px) 100vw, 720px">'
            f'<img src="imagens/{nome_novo}.jpg" width="1600" height="900" '
            f'loading="eager" fetchpriority="high" decoding="async"\n'
            f'         alt="{alt}"></picture>\n'
            f'    <figcaption>{legenda}\n'
            f'      <span class="credito">{credito}</span></figcaption>\n'
            f'  </figure>\n')
    s = s[:m.start()] + nova + s[m.end():]

    err = [t for t in ['div', 'p', 'figure', 'picture', 'section', 'main', 'h1', 'h2', 'h3', 'span']
           if len(re.findall(f'<{t}[ >]', s)) != s.count(f'</{t}>')]
    if err or 'alt=""' in s:
        raise SystemExit(f'RECUSADO {arquivo}: {err}')
    open(p, 'w', encoding='utf-8').write(s)
    print(f'  ok  {arquivo}: figura trocada')
