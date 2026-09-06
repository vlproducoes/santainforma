#!/usr/bin/env python3
"""Mede o contraste do leque editorial do estilo.css.

Le a paleta direto do CSS, calcula o contraste de cada tom nos fundos em que
ele de fato aparece e reprova se algum par cair abaixo do piso. Serve para
conferir tom novo antes de commitar, do jeito que manda o CLAUDE.md 9.5:
tom entra medido, nunca "no olho".

    python3 ferramentas/contraste.py          # tabela e codigo de saida
    python3 ferramentas/contraste.py "#8356C7" "#FFFFFF"   # um par avulso

Piso: 4,5:1 para texto (AA), medido tambem sobre o fundo da pagina, sobre a
espuma e sobre o proprio tint, porque o chapeu vive nos quatro. O tom -claro
responde pelo breu e pelo modo escuro.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CSS = RAIZ / 'estilo.css'
PISO_TEXTO = 4.5
PISO_ESCURO = 4.5


def luminancia(hexa):
    h = hexa.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    canais = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canais]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    claro, escuro = max(la, lb), min(la, lb)
    return (claro + 0.05) / (escuro + 0.05)


def mistura(a, b, parte):
    """parte de a sobre b, em sRGB. Mesma conta do color-mix do CSS."""
    a, b = a.lstrip('#'), b.lstrip('#')
    saida = '#'
    for i in (0, 2, 4):
        saida += '%02X' % round(int(a[i:i + 2], 16) * parte + int(b[i:i + 2], 16) * (1 - parte))
    return saida


def le_variaveis():
    """Todas as --var:valor do CSS, com var(--outra) resolvido."""
    texto = CSS.read_text(encoding='utf-8')
    bruto = {}
    for nome, valor in re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;}]+)', texto):
        bruto.setdefault(nome, valor.strip())          # a primeira definicao e a do modo claro

    def resolve(valor, fundo=0):
        if fundo > 8:
            return valor
        alvo = re.fullmatch(r'var\((--[a-z0-9-]+)\)', valor.strip())
        if alvo and alvo.group(1) in bruto:
            return resolve(bruto[alvo.group(1)], fundo + 1)
        return valor.strip()

    return {n: resolve(v) for n, v in bruto.items()}


def editorias(v):
    nomes = sorted({m.group(1) for m in
                    (re.fullmatch(r'--ed-([a-z-]+?)(?:-claro|-tint)?', n) for n in v)
                    if m and m.group(1) not in ('texto', 'claro', 'tint')})
    return [n for n in nomes if f'--ed-{n}' in v and v[f'--ed-{n}'].startswith('#')]


def principal():
    if len(sys.argv) == 3:
        a, b = sys.argv[1], sys.argv[2]
        print('%s sobre %s: %.2f:1' % (a, b, contraste(a, b)))
        return 0 if contraste(a, b) >= PISO_TEXTO else 1

    v = le_variaveis()
    branco = v.get('--superficie', '#FFFFFF')
    fundo = v.get('--fundo', '#F5F7F6')
    espuma = v.get('--espuma', '#F1F5F3')
    breu = v.get('--breu', '#0A1F28')
    escuro = '#0E2630'                                  # --superficie do bloco 13
    falhas = []

    print('%-16s %-8s branco fundo espuma  tint | %-8s breu  escuro' % ('editoria', 'tom', 'claro'))
    print('-' * 74)
    for nome in editorias(v):
        tom = v['--ed-%s' % nome]
        claro = v.get('--ed-%s-claro' % nome, tom)
        tint = v.get('--ed-%s-tint' % nome, branco)
        if not tint.startswith('#'):
            tint = branco
        medidas = {
            'branco': contraste(tom, branco),
            'fundo': contraste(tom, fundo),
            'espuma': contraste(tom, espuma),
            'tint': contraste(tom, tint),
        }
        no_breu = contraste(claro, breu)
        no_escuro = contraste(claro, escuro)
        tint_escuro = mistura(claro, escuro, 0.14)
        no_tint_escuro = contraste(claro, tint_escuro)
        for onde, valor in medidas.items():
            if valor < PISO_TEXTO:
                falhas.append('%s: tom %s sobre %s da %.2f:1' % (nome, tom, onde, valor))
        for onde, valor in (('breu', no_breu), ('superficie escura', no_escuro),
                            ('tint escuro', no_tint_escuro)):
            if valor < PISO_ESCURO:
                falhas.append('%s: claro %s sobre %s da %.2f:1' % (nome, claro, onde, valor))
        print('%-16s %-8s %5.2f %5.2f  %5.2f %5.2f | %-8s %5.2f %5.2f' % (
            nome, tom, medidas['branco'], medidas['fundo'], medidas['espuma'],
            medidas['tint'], claro, no_breu, no_escuro))

    print()
    if falhas:
        print('reprovado, piso de %.1f:1' % PISO_TEXTO)
        for f in falhas:
            print(' -', f)
        return 1
    print('leque inteiro acima de %.1f:1 nos dois modos' % PISO_TEXTO)
    return 0


if __name__ == '__main__':
    sys.exit(principal())
