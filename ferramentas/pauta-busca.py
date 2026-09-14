# -*- coding: utf-8 -*-
"""Descobre o que a gente da regiao digita no Google, para pautar pagina atemporal.

O QUE ISTO E, E O QUE NAO E
---------------------------
Isto le o autocompletar do Google (suggestqueries), que devolve as consultas
reais que as pessoas digitam, na ordem em que o Google considera mais provaveis.
E o melhor sinal publico e gratuito que temos.

NAO e volume de busca. Ninguem aqui tem numero de busca por mes: isso exige
Keyword Planner com conta de Google Ads ativa, ou o Search Console do proprio
site. O que sai daqui e ORDEM e RECORRENCIA, que sao proxy de demanda, nao
medida dela. Nunca escreva no site, nem no relatorio, que uma pagina foi feita
"segundo o volume de buscas". Escreva que saiu do autocompletar.

Se o editor ligar o Search Console e exportar as consultas, aquilo sim e dado
real do nosso proprio publico, e passa na frente disto aqui.

COMO USAR
---------
    python3 ferramentas/pauta-busca.py                 # varredura padrao
    python3 ferramentas/pauta-busca.py --alfabeto      # varredura funda, mais lenta
    python3 ferramentas/pauta-busca.py --salvar pauta.md

Sai uma lista ordenada, ja limpa do que o site tem, com a pontuacao de cada
consulta e onde ela apareceu.
"""
import argparse, glob, html, json, os, re, sys, time, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PONTA = 'https://suggestqueries.google.com/complete/search'
PAUSA = 0.35   # gentileza com o servidor do Google

CIDADES = ['itapema', 'porto belo', 'bombinhas', 'meia praia itapema']

# Termos de servico: o que alguem resolve, paga, agenda ou precisa achar.
SERVICOS = [
    'iptu', 'onibus', 'coleta de lixo', 'telefone', 'posto de saude',
    'matricula', 'creche', 'alvara', 'praia', 'feriado', 'concurso',
    'emprego', 'cartorio', 'nota fiscal', 'iss', 'defesa civil',
    'farmacia de plantao', 'hospital', 'escola', 'aluguel de temporada',
    'camping', 'estacionamento', 'ciclovia', 'feira', 'mercado publico',
]

# Perguntas: quem digita pergunta esta procurando explicacao, nao noticia.
PERGUNTAS = ['como', 'onde', 'quanto custa', 'quando', 'qual', 'quem', 'o que fazer em']

RUIDO = re.compile(
    r'\b(fm|radio|r[aá]dio|ao vivo|playlist|m[uú]sica|musicas|whatsapp do|'
    r'porto alegre|curitiba|s[aã]o paulo|rio de janeiro|letra|cifra|'
    r'itapema park|onlyfans|acompanhante|garota)\b', re.I)


def sugerir(consulta):
    p = urllib.parse.urlencode({
        'client': 'firefox', 'hl': 'pt-BR', 'gl': 'br',
        'ie': 'utf-8', 'oe': 'utf-8', 'q': consulta,
    })
    req = urllib.request.Request(f'{PONTA}?{p}', headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            dados = json.loads(r.read().decode('utf-8', 'replace'))
        return [s.strip().lower() for s in dados[1]]
    except Exception as ex:
        print(f'  falhou "{consulta}": {ex}', file=sys.stderr)
        return []


def ja_temos():
    """Titulo e slug do que ja esta publicado, para nao repetir assunto."""
    texto = []
    for f in glob.glob(f'{BASE}/*.html'):
        texto.append(os.path.basename(f).replace('-', ' '))
        s = open(f, encoding='utf-8').read(4000)
        m = re.search(r'<title>(.*?)</title>', s, re.S)
        if m:
            texto.append(html.unescape(m.group(1)).lower())
    return ' | '.join(texto).lower()


def coberto(consulta, tudo):
    """Heuristica simples: se as palavras fortes da consulta ja aparecem juntas."""
    fortes = [p for p in re.findall(r'\w{4,}', consulta) if p not in
              ('itapema', 'porto', 'belo', 'bombinhas', 'praia', 'santa', 'catarina')]
    return bool(fortes) and all(p in tudo for p in fortes)


def varrer(alfabeto=False):
    sementes = []
    for c in CIDADES:
        sementes.append(c + ' ')
        for s in SERVICOS:
            sementes.append(f'{s} {c}')
        for q in PERGUNTAS:
            sementes.append(f'{q} {c}')
        if alfabeto:
            sementes += [f'{c} {letra}' for letra in 'abcdefghijklmnopqrstuvwxyz']

    pontos, origem = {}, {}
    for i, semente in enumerate(sementes, 1):
        print(f'  [{i}/{len(sementes)}] {semente}', file=sys.stderr)
        for pos, sug in enumerate(sugerir(semente)):
            # posicao 0 vale 10, posicao 9 vale 1: o topo do autocompletar pesa mais
            pontos[sug] = pontos.get(sug, 0) + max(1, 10 - pos)
            origem.setdefault(sug, set()).add(semente.strip())
        time.sleep(PAUSA)
    return pontos, origem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--alfabeto', action='store_true', help='varredura funda (lenta)')
    ap.add_argument('--salvar', metavar='ARQUIVO', help='grava a lista em markdown')
    ap.add_argument('--minimo', type=int, default=6, help='pontuacao minima')
    a = ap.parse_args()

    pontos, origem = varrer(a.alfabeto)
    tudo = ja_temos()

    linhas = []
    for sug, p in sorted(pontos.items(), key=lambda kv: -kv[1]):
        if p < a.minimo or RUIDO.search(sug):
            continue
        if not any(c.split()[0] in sug for c in CIDADES):
            continue
        marca = 'JA COBERTO' if coberto(sug, tudo) else 'LIVRE'
        linhas.append((p, sug, marca, sorted(origem[sug])[:3]))

    livres = [l for l in linhas if l[2] == 'LIVRE']
    print(f'\n{len(pontos)} consultas colhidas, {len(linhas)} acima do corte, '
          f'{len(livres)} ainda sem pagina nossa.\n')
    print('pontos | consulta | situacao')
    print('-' * 72)
    for p, sug, marca, _ in linhas[:80]:
        print(f'{p:6d} | {sug[:52]:52s} | {marca}')

    if a.salvar:
        with open(a.salvar, 'w', encoding='utf-8') as f:
            f.write('# Pauta de busca, saida do autocompletar do Google\n\n')
            f.write('Ordem e recorrencia do autocompletar. **Nao e volume de busca.**\n\n')
            f.write('| pontos | consulta | situacao | apareceu em |\n|---|---|---|---|\n')
            for p, sug, marca, ond in linhas:
                f.write(f'| {p} | {sug} | {marca} | {", ".join(ond)} |\n')
        print(f'\ngravado em {a.salvar}')


if __name__ == '__main__':
    main()
