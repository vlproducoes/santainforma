# -*- coding: utf-8 -*-
"""TESTE B. Ensaio geral do ciclo de noticias, sem publicar nada.

    python3 ferramentas/ensaio-geral.py

O Teste A (checa-ambiente.py) diz se o painel foi configurado direito.
Este aqui vai adiante e percorre o ciclo de ponta a ponta, do jeito que a
rotina automatica faz, so que sem escrever materia e sem commitar:

  1. apura: abre a fonte oficial e confirma que veio texto de noticia
  2. imagem: baixa uma foto de verdade e corta no padrao 16:9 do site
  3. sitemap: roda o gerador do Google Noticias
  4. checagem: roda checa-site.py nas paginas todas
  5. no ar: le o site publicado com cache-busting, como manda o passo 10
  6. segredo: confere que nenhuma chave vazou para o Git

Nada do que ele cria fica no repositorio. Sai com 0 se o ciclo pode rodar
sozinho, e com 1 se ainda nao pode.
"""
import os, re, subprocess, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://santainforma.com.br'
UA = 'Santa Informa/1.0 (ensaio geral)'

VERDE, VERMELHO, AMARELO, FIM = '\033[32m', '\033[31m', '\033[33m', '\033[0m'
if not sys.stdout.isatty():
    VERDE = VERMELHO = AMARELO = FIM = ''

bloqueios, avisos = [], []


def titulo(n, t):
    print(f'\n{n}. {t}\n' + '-' * (len(t) + 3))


def ok(msg):
    print(f'  {VERDE}ok{FIM}      {msg}')


def falha(msg, motivo):
    print(f'  {VERMELHO}FALHOU{FIM}  {msg}')
    bloqueios.append(motivo)


def aviso(msg, motivo):
    print(f'  {AMARELO}aviso {FIM}  {msg}')
    avisos.append(motivo)


def baixa(url, destino=None, extra=None):
    """Devolve (codigo_http, corpo_ou_caminho). Corpo vazio quando falha."""
    cmd = ['curl', '-sSL', '--max-time', '40', '-A', UA,
           '-w', '\n%{http_code}']
    if extra:
        cmd += extra
    if destino:
        cmd += ['-o', destino, url]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '', destino
    cmd += [url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not r.stdout:
        return '', ''
    partes = r.stdout.rsplit('\n', 1)
    return (partes[1].strip(), partes[0]) if len(partes) == 2 else ('', r.stdout)


# ------------------------------------------------------- 1. apurar
titulo(1, 'Apuracao: a fonte oficial abre e traz noticia?')
codigo, corpo = baixa('https://www.itapema.sc.gov.br/noticia/')
if codigo != '200' or len(corpo) < 2000:
    falha(f'Prefeitura de Itapema nao entregou a pagina de noticias (HTTP {codigo or "sem resposta"})',
          'sem acesso a fonte municipal, o ciclo nao tem o que apurar')
else:
    manchetes = re.findall(r'<h[23][^>]*>\s*(?:<a[^>]*>)?\s*([^<]{25,140})', corpo)
    manchetes = [m.strip() for m in manchetes if m.strip()]
    if len(manchetes) < 3:
        aviso('a pagina abriu mas nao deu para ler manchete, confira o seletor',
              'a pagina da Prefeitura abriu mas o formato mudou')
    else:
        ok(f'Prefeitura de Itapema respondeu com {len(manchetes)} manchetes')
        for m in manchetes[:3]:
            print(f'          . {m[:78]}')

codigo, _ = baixa('https://site.itapema.sc.leg.br/')
if codigo == '200':
    ok('Camara de Itapema respondeu')
else:
    falha(f'Camara de Itapema nao respondeu (HTTP {codigo or "sem resposta"})',
          'sem acesso a Camara, some o nivel legislativo da pauta')

# ------------------------------------------------------- 2. imagem
titulo(2, 'Imagem: da para baixar e cortar no padrao do site?')
try:
    from PIL import Image, ImageOps
except ImportError:
    falha('Pillow nao instalado, nenhuma imagem pode ser gerada',
          'Pillow ausente, ponha "pip install --quiet pillow" no Setup script')
else:
    with tempfile.TemporaryDirectory() as tmp:
        bruto = os.path.join(tmp, 'teste.bin')
        # favicon do proprio site: arquivo pequeno, licenca nossa, serve de cobaia
        codigo, _ = baixa(f'{SITE}/apple-touch-icon.png', destino=bruto)
        if codigo != '200' or not os.path.getsize(bruto):
            falha(f'nao deu para baixar imagem de teste (HTTP {codigo or "sem resposta"})',
                  'sem baixar imagem, foto-oficial.py e buscar-imagem.py nao funcionam')
        else:
            try:
                im = Image.open(bruto)
                im.load()
                grande = ImageOps.fit(im.convert('RGB'), (1600, 900), Image.LANCZOS,
                                      centering=(0.5, 0.42))
                grande.save(os.path.join(tmp, 't.jpg'), 'JPEG', quality=86,
                            optimize=True, progressive=True)
                grande.save(os.path.join(tmp, 't.webp'), 'WEBP', quality=78, method=6)
                ok('baixou, cortou em 16:9, salvou JPEG e WebP')
            except Exception as ex:
                falha(f'Pillow quebrou ao processar: {ex}',
                      'Pillow instalado mas sem suporte a JPEG ou WebP')

    for pasta in ('imagens/webp', 'imagens/miniaturas'):
        if os.path.isdir(os.path.join(BASE, pasta)):
            ok(f'pasta {pasta} existe')
        else:
            aviso(f'pasta {pasta} nao existe', f'{pasta} faltando, as ferramentas de imagem podem quebrar')

# ------------------------------------------------------- 3. sitemap
titulo(3, 'Sitemap de noticias: o gerador roda?')
r = subprocess.run([sys.executable, os.path.join(BASE, 'ferramentas/sitemap-noticias.py')],
                   capture_output=True, text=True, cwd=BASE)
if r.returncode != 0:
    falha(f'sitemap-noticias.py falhou: {(r.stderr or r.stdout).strip()[:120]}',
          'o gerador do sitemap de noticias quebrou')
else:
    print('  ' + (r.stdout.strip().splitlines() or ['sem saida'])[0])
    ok('sitemap-noticias.xml regenerado')

# ------------------------------------------------------- 4. checagem
titulo(4, 'Checagem das paginas')
r = subprocess.run([sys.executable, os.path.join(BASE, 'ferramentas/checa-site.py')],
                   capture_output=True, text=True, cwd=BASE)
print('  ' + r.stdout.strip().replace('\n', '\n  '))
if r.returncode != 0:
    falha('checa-site.py reprovou o site', 'o site tem problema de HTML ou SEO a corrigir')
else:
    ok('todas as paginas passaram')

# ------------------------------------------------------- 5. no ar
titulo(5, 'No ar: o site publicado responde?')
alvos = [('/', 'a home'), ('/sitemap-noticias.xml', 'o sitemap de noticias')]
for caminho, nome in alvos:
    achou = False
    for tentativa in range(1, 4):
        cb = os.urandom(4).hex()
        codigo, corpo = baixa(f'{SITE}{caminho}?cb={cb}',
                              extra=['-H', 'Cache-Control: no-cache'])
        if codigo == '200' and corpo:
            achou = True
            break
    if not achou:
        falha(f'{nome} nao respondeu em 3 leituras (HTTP {codigo or "sem resposta"})',
              f'nao da para conferir {nome} no ar depois do deploy')
        continue
    if caminho == '/':
        ligacoes = len(re.findall(r'href="materia-\d+', corpo))
        ok(f'{nome} respondeu, com {ligacoes} chamadas para materia')
    else:
        n = corpo.count('<loc>')
        ok(f'{nome} respondeu, com {n} entradas')

# ------------------------------------------------------- 6. segredo
titulo(6, 'Varredura de chave, o repositorio e publico')
r = subprocess.run(['git', 'ls-files'], capture_output=True, text=True, cwd=BASE)
versionados = [x for x in r.stdout.split() if x == '.env' or x.endswith('/.env')]
if versionados:
    falha(f'.env versionado: {versionados}', 'ARQUIVO .env NA ARVORE DO GIT, nao publique')
else:
    ok('nenhum .env na arvore')

r = subprocess.run(['git', 'grep', '-lIE',
                    r'PEXELS_API_KEY *= *[A-Za-z0-9]{20,}', 'HEAD'],
                   capture_output=True, text=True, cwd=BASE)
if r.stdout.strip():
    falha(f'chave literal versionada em: {r.stdout.strip()}', 'CHAVE REAL NO GIT, nao publique')
else:
    ok('nenhuma chave literal no conteudo versionado')

# ------------------------------------------------------- veredito
print('\n' + '=' * 62)
if bloqueios:
    print(f'{VERMELHO}O ciclo ainda NAO pode rodar sozinho.{FIM}\n')
    for b in bloqueios:
        print(f'  trava: {b}')
    for a in avisos:
        print(f'  aviso: {a}')
    print('\nRode antes: python3 ferramentas/checa-ambiente.py')
    sys.exit(1)

print(f'{VERDE}Ensaio geral aprovado. O ciclo pode rodar no automatico.{FIM}\n')
print('  Apurou na fonte, montou imagem, gerou sitemap, passou na checagem,')
print('  leu o site no ar e nao achou chave vazada.')
for a in avisos:
    print(f'  aviso: {a}')
sys.exit(0)
