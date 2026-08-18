# -*- coding: utf-8 -*-
"""Instala o Google AdSense no site, em duas etapas.

Etapa 1, assim que a conta existir (o ID ca-pub sai do painel do AdSense):
    python3 ferramentas/adsense.py base ca-pub-XXXXXXXXXXXXXXXX

    Escreve o ads.txt, poe o script do AdSense no <head> das paginas e liga o
    modo nao personalizado, que e o que a Politica de Privacidade promete.

Etapa 2, depois de criar a unidade de anuncio no painel (sai o data-ad-slot):
    python3 ferramentas/adsense.py unidade NNNNNNNNNN

    Insere o bloco de publicidade nas materias, antes de "Os numeros que
    importam". So nas materias: home, editorias, Raio-X, horoscopo e arquivo
    sao inventario da tabela de precos e nao recebem Google.

Regras que este script cobra:
  - Auto Ads nunca: o bloco e manual e rotulado "Publicidade".
  - Nenhum espaco .anuncio da tabela e tocado.
  - Roda duas vezes sem duplicar (confere antes de inserir).
"""
import glob, re, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def paginas():
    return sorted(glob.glob(f'{BASE}/*.html'))

def base(pub):
    assert re.fullmatch(r'ca-pub-\d{16}', pub), f'ID estranho: {pub!r} (esperado ca-pub- e 16 digitos)'
    # ads.txt: e o registro publico de quem pode vender anuncio no dominio
    with open(f'{BASE}/ads.txt', 'w', encoding='utf-8') as f:
        f.write(f'google.com, {pub[3:]}, DIRECT, f08c47fec0942fa0\n')
    print('  ads.txt escrito')

    tag = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={pub}"\n'
           f'        crossorigin="anonymous"></script>\n'
           f'<script>\n'
           f'/* PUBLICIDADE\n'
           f'   Modo nao personalizado: o anuncio segue o assunto da pagina, nao um\n'
           f'   perfil do leitor. E a promessa da Politica de Privacidade virando codigo. */\n'
           f'(adsbygoogle = window.adsbygoogle || []).requestNonPersonalizedAds = 1;\n'
           f'</script>\n')
    feitas = puladas = 0
    for p in paginas():
        s = open(p, encoding='utf-8').read()
        if 'adsbygoogle.js' in s: puladas += 1; continue
        assert '</head>' in s, p
        s = s.replace('</head>', tag + '</head>', 1)
        open(p, 'w', encoding='utf-8').write(s)
        feitas += 1
    print(f'  script no <head> de {feitas} páginas' + (f' ({puladas} já tinham)' if puladas else ''))

def unidade(slot):
    assert re.fullmatch(r'\d{10}', slot), f'slot estranho: {slot!r} (esperado 10 digitos)'
    # o ca-pub vem do ads.txt para nao pedir duas vezes
    ads = open(f'{BASE}/ads.txt', encoding='utf-8').read()
    pub = 'ca-' + re.search(r'pub-\d{16}', ads).group(0)
    bloco = (f'  <div class="pub-google">\n'
             f'    <span class="pub-rotulo">Publicidade</span>\n'
             f'    <ins class="adsbygoogle" style="display:block"\n'
             f'         data-ad-client="{pub}" data-ad-slot="{slot}"\n'
             f'         data-ad-format="horizontal" data-full-width-responsive="false"></ins>\n'
             f'    <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>\n'
             f'  </div>\n\n')
    ANCORA = '  <h3>Os números que importam</h3>'
    feitas = puladas = 0
    for p in sorted(glob.glob(f'{BASE}/materia-*.html')):
        s = open(p, encoding='utf-8').read()
        if 'pub-google' in s: puladas += 1; continue
        assert ANCORA in s, p
        s = s.replace(ANCORA, bloco + ANCORA, 1)
        open(p, 'w', encoding='utf-8').write(s)
        feitas += 1
    print(f'  unidade nas {feitas} matérias' + (f' ({puladas} já tinham)' if puladas else ''))

if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == 'base':
        base(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == 'unidade':
        unidade(sys.argv[2])
    else:
        raise SystemExit(__doc__)
