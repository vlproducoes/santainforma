#!/usr/bin/env python3
"""Gera os icones do site a partir da mesma geometria do favicon.svg.

    python3 ferramentas/icone.py

Escreve favicon.ico (16, 32, 48 e 64), favicon-16.png, favicon-32.png e
apple-touch-icon.png na raiz. Desenha em 16x o tamanho final e reduz com
LANCZOS, para o sol e os fios do mar sairem limpos em 16px.

O icone e REDONDO: um disco branco com o sol nascendo na linha d'agua, fio de
mar em volta, e transparente fora do disco. A excecao e o apple-touch-icon,
que fica QUADRADO e opaco de proposito: o iOS aplica a propria mascara e
transforma area transparente em preto, entao mandar um PNG redondo para la
devolve um icone com quatro cantos pretos.

As cores sao as do logo no cabecalho: fundo branco (--superficie), sol em
--sol-logo, mar em --mar-logo. Mudou a cor da marca no estilo.css? Mude as
tres constantes aqui e no favicon.svg, e rode de novo. O favicon.svg e escrito
a mao; este script e a mesma geometria em pixel.
"""
import os
import sys

from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUNDO = (255, 255, 255)
SOL = (240, 168, 30)          # --sol-logo #F0A81E
MAR = (44, 124, 155)          # --mar-logo #2C7C9B
ANEL = 120                    # opacidade do fio em volta do disco, de 0 a 255
ESC = 16                      # desenha 16x maior e reduz


def desenha(lado, redondo=True):
    """Uma tela quadrada de `lado` px, na geometria de 64 do favicon.svg."""
    g = lado * ESC
    k = g / 64.0                                    # de unidade do SVG para pixel
    im = Image.new('RGBA', (g, g), FUNDO + (255,))
    d = ImageDraw.Draw(im)

    def linha(x1, y1, x2, y2, largura):
        d.line([(x1 * k, y1 * k), (x2 * k, y2 * k)], fill=SOL, width=int(round(largura * k)))
        r = largura * k / 2                          # ponta redonda nas duas pontas
        for x, y in ((x1, y1), (x2, y2)):
            d.ellipse([x * k - r, y * k - r, x * k + r, y * k + r], fill=SOL)

    def barra(x, y, larg, alt, cor, opacidade=1.0):
        camada = Image.new('RGBA', im.size, cor + (255,))
        mascara = Image.new('L', im.size, 0)
        ImageDraw.Draw(mascara).rectangle(
            [x * k, y * k, (x + larg) * k, (y + alt) * k], fill=int(round(255 * opacidade)))
        im.alpha_composite(Image.composite(camada, Image.new('RGBA', im.size, (0, 0, 0, 0)), mascara))

    linha(32, 9, 32, 15, 3.4)                        # os tres raios
    linha(14.5, 16.5, 18.8, 20.8, 3.4)
    linha(49.5, 16.5, 45.2, 20.8, 3.4)
    d.ellipse([(32 - 14) * k, (36 - 14) * k, (32 + 14) * k, (36 + 14) * k], fill=SOL)
    d.rectangle([0, 36 * k, g, g], fill=FUNDO + (255,))   # corta a metade de baixo do sol
    barra(0, 36, 64, 3.4, SOL)                       # a linha d'agua
    barra(8, 45, 48, 3.2, MAR, .90)                  # o mar, em dois fios que somem
    barra(16, 53, 32, 3.2, MAR, .62)

    if redondo:
        mascara = Image.new('L', im.size, 0)
        ImageDraw.Draw(mascara).ellipse([0, 0, g - 1, g - 1], fill=255)
        im.putalpha(mascara)
        # o fio em volta: sem ele o disco branco some em aba clara e o icone
        # volta a parecer quadrado
        ImageDraw.Draw(im).ellipse([k * .6, k * .6, g - 1 - k * .6, g - 1 - k * .6],
                                   outline=MAR + (ANEL,), width=int(round(1.2 * k)))
    return im.resize((lado, lado), Image.LANCZOS)


def principal():
    desenha(16).save(os.path.join(RAIZ, 'favicon-16.png'))
    desenha(32).save(os.path.join(RAIZ, 'favicon-32.png'))
    # quadrado e sem alfa: ver o aviso sobre o iOS no topo do arquivo
    desenha(180, redondo=False).convert('RGB').save(os.path.join(RAIZ, 'apple-touch-icon.png'))
    desenha(64).save(os.path.join(RAIZ, 'favicon.ico'),
                     sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print('icones gerados em', RAIZ)
    return 0


if __name__ == '__main__':
    sys.exit(principal())
