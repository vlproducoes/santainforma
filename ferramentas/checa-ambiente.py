# -*- coding: utf-8 -*-
"""TESTE A. Confere se o ambiente da nuvem esta configurado direito.

    python3 ferramentas/checa-ambiente.py

Olha as tres coisas que o editor configura no painel da rotina, em
claude.ai/code/routines, no dialogo "Update cloud environment":

  1. Network access em Custom (ou Full), com os dominios das fontes liberados
  2. PEXELS_API_KEY na caixa Environment variables
  3. "pip install pillow" na caixa Setup script

Sai com codigo 0 se o essencial passou, 1 se faltou alguma coisa.
Nao publica nada e nao toca em arquivo do site.
"""
import os, subprocess, sys

# Dominio, para que serve, e se a falta dele trava o ciclo.
# O nivel MUNICIPAL e o coracao do portal: sem ele nao ha o que apurar.
FONTES = [
    ('www.itapema.sc.gov.br',      'Prefeitura de Itapema',        True),
    ('site.itapema.sc.leg.br',     'Camara de Itapema',            True),
    ('www.mpsc.mp.br',             'Ministerio Publico de SC',     True),
    ('agenciabrasil.ebc.com.br',   'Agencia Brasil, nacional',     True),
    ('www.defesacivil.sc.gov.br',  'Defesa Civil de SC',           True),
    ('portobelo.sc.gov.br',        'Porto Belo, regional',        False),
    ('bombinhas.sc.gov.br',        'Bombinhas, regional',         False),
    ('santainforma.com.br',        'o proprio site, no ar',        True),
    ('api.pexels.com',             'busca de imagem no Pexels',   False),
]

VERDE, VERMELHO, AMARELO, FIM = '\033[32m', '\033[31m', '\033[33m', '\033[0m'
if not sys.stdout.isatty():
    VERDE = VERMELHO = AMARELO = FIM = ''

falhas_graves, avisos = [], []


def titulo(t):
    print(f'\n{t}\n' + '-' * len(t))


def alcanca(host):
    """Devolve (ok, explicacao, culpa).

    Separa duas coisas que o editor resolve de jeito diferente:
      culpa 'politica'  o proxy da Anthropic barrou, e isso se arruma no painel
      culpa 'site'      o proxy deixou passar e o servidor da fonte e que recusou

    O sinal e a linha "200 Connection Established", que so aparece quando o
    tunel CONNECT do proxy foi aberto, ou seja, o dominio esta liberado.
    """
    r = subprocess.run(
        ['curl', '-sS', '-o', '/dev/null', '-D', '-', '--max-time', '25',
         '-A', 'Santa Informa/1.0 (checagem de ambiente)', f'https://{host}/'],
        capture_output=True, text=True)
    cabecalhos, erro = r.stdout, r.stderr.strip()

    liberado = 'Connection Established' in cabecalhos
    if 'host_not_allowed' in cabecalhos.lower() or 'x-deny-reason' in cabecalhos.lower():
        return False, 'bloqueado pela politica de rede', 'politica'
    if not liberado:
        if r.returncode == 56 and '403' in erro:
            return False, 'bloqueado pela politica de rede', 'politica'
        return False, f'nao respondeu ({erro[:60] or "erro " + str(r.returncode)})', 'site'

    codigos = [l.split()[1] for l in cabecalhos.splitlines()
               if l.startswith('HTTP/') and 'Connection Established' not in l]
    codigo = codigos[-1] if codigos else ''
    if codigo.startswith(('2', '3')):
        return True, f'HTTP {codigo}', ''
    return False, f'liberado no proxy, mas o servidor da fonte respondeu {codigo or "nada"}', 'site'


# ---------------------------------------------------------------- 1. rede
titulo('1. Rede: as fontes abrem?')
liberados, barrados_pela_politica = 0, 0
for host, para_que, essencial in FONTES:
    passou, porque, culpa = alcanca(host)
    if passou:
        liberados += 1
        print(f'  {VERDE}ok{FIM}      {host:<28} {para_que} ({porque})')
        continue
    if culpa == 'politica':
        barrados_pela_politica += 1
    marca = f'{VERMELHO}FALHOU{FIM}' if essencial else f'{AMARELO}aviso {FIM}'
    print(f'  {marca}  {host:<28} {para_que}: {porque}')
    recado = (f'{host}: {porque}' if culpa == 'politica'
              else f'{host} recusa a nossa leitura, nao e coisa que o painel resolva')
    (falhas_graves if essencial else avisos).append(recado)

print(f'\n  {liberados} de {len(FONTES)} dominios abriram.')
if barrados_pela_politica:
    print(f'  {barrados_pela_politica} barrados pela politica de rede, isso se arruma no painel.')
else:
    print('  Nenhum barrado pela politica de rede: a lista de dominios esta certa.')

# ------------------------------------------------------------- 2. a chave
titulo('2. Chave do Pexels')
chave = os.environ.get('PEXELS_API_KEY', '').strip()
if not chave:
    print(f'  {AMARELO}aviso {FIM}  PEXELS_API_KEY nao esta no ambiente')
    avisos.append('sem PEXELS_API_KEY: o ciclo fica so com foto oficial e SVG da marca')
else:
    r = subprocess.run(
        ['curl', '-sS', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '25',
         '-H', f'Authorization: {chave}',
         'https://api.pexels.com/v1/search?query=praia&per_page=1'],
        capture_output=True, text=True)
    codigo = r.stdout.strip()
    if codigo == '200':
        print(f'  {VERDE}ok{FIM}      chave presente e aceita pelo Pexels')
    elif codigo == '401':
        print(f'  {VERMELHO}FALHOU{FIM}  chave presente mas o Pexels recusou (401)')
        avisos.append('PEXELS_API_KEY invalida, confira o valor no painel')
    else:
        print(f'  {AMARELO}aviso {FIM}  nao deu para testar a chave (HTTP {codigo or "sem resposta"})')
        avisos.append('nao deu para validar a chave do Pexels')

# ------------------------------------------------------------- 3. Pillow
titulo('3. Pillow, para cortar e converter imagem')
try:
    import PIL
    from PIL import Image, ImageOps  # noqa: F401
    print(f'  {VERDE}ok{FIM}      Pillow {PIL.__version__} instalado')
except ImportError:
    print(f'  {VERMELHO}FALHOU{FIM}  Pillow nao instalado')
    print('          ponha "pip install --quiet pillow" no campo Setup script')
    falhas_graves.append('Pillow ausente: nenhuma imagem pode ser gerada')

# ------------------------------------------------------------- veredito
titulo('Veredito')
if falhas_graves:
    print(f'  {VERMELHO}O ambiente ainda NAO esta pronto.{FIM}\n')
    for f in falhas_graves:
        print(f'    falta: {f}')
    for a in avisos:
        print(f'    aviso: {a}')
    print('\n  Onde arrumar: claude.ai/code/routines, abra a rotina, lapis para')
    print('  editar, clique no icone de nuvem do ambiente, engrenagem, e ajuste')
    print('  Network access, Environment variables e Setup script. A mudanca')
    print('  so vale a partir da proxima execucao.')
    sys.exit(1)

print(f'  {VERDE}Configuracao aceita.{FIM} As fontes essenciais abrem e o Pillow esta no lugar.')
for a in avisos:
    print(f'    aviso: {a}')
print('\n  Proximo passo: python3 ferramentas/ensaio-geral.py')
sys.exit(0)
