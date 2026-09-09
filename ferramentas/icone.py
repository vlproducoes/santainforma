#!/usr/bin/env python3
"""Gera os icones do site a partir da mesma geometria do favicon.svg.

    python3 ferramentas/icone.py

Escreve favicon.ico (16, 32, 48 e 64), favicon-16.png, favicon-32.png e
apple-touch-icon.png na raiz. Desenha em 16x o tamanho final e reduz com
LANCZOS, para o sol e os fios do mar sairem limpos em 16px.

As cores sao as do logo no cabecalho: fundo branco (--superficie), sol em
--sol-logo, mar em --mar-logo. Mudou a cor da marca no estilo.css? Mude as
tres constantes aqui e no favicon.svg, e rode de novo. O favicon.svg e escrito
a mao; este script e a mesma geometria em pixel.
"""
from PIL import Image, ImageDraw

FUNDO = (255, 255, 255)
SOL = (240, 168, 30)          # --sol-logo #F0A81E
MAR = (44, 124, 155)          # --mar-logo #2C7C9B
ESC = 16                      # desenha 16x maior e reduz


def desenha(lado):
    """Uma tela quadrada de `lado` px, na geometria de 64 do favicon.svg."""
    g = lado * ESC
    k = g / 64.0                                    # de unidade do SVG para pixel
    im = Image.new('RGB', (g, g), FUNDO)
    d = ImageDraw.Draw(im)

    def linha(x1, y1, x2, y2, largura):
        d.line([(x1 * k, y1 * k), (x2 * k, y2 * k)], fill=SOL,
               width=int(round(largura * k)), joint='curve')
        r = largura * k / 2                          # ponta redonda nas duas pontas
        for x, y in ((x1, y1), (x2, y2)):
            d.ellipse([x * k - r, y * k - r, x * k + r, y * k + r], fill=SOL)

    def barra(x, y, larg, alt, cor, opacidade=1.0):
        camada = Image.new('RGB', im.size, cor)
        mascara = Image.new('L', im.size, 0)
        ImageDraw.Draw(mascara).rectangle(
            [x * k, y * k, (x + larg) * k, (y + alt) * k], fill=int(round(255 * opacidade)))
        im.paste(Image.composite(camada, im, mascara), (0, 0))

    linha(32, 9, 32, 15, 3.4)                        # os tres raios
    linha(14.5, 16.5, 18.8, 20.8, 3.4)
    linha(49.5, 16.5, 45.2, 20.8, 3.4)
    d.ellipse([(32 - 14) * k, (36 - 14) * k, (32 + 14) * k, (36 + 14) * k], fill=SOL)
    d.rectangle([0, 36 * k, g, g], fill=FUNDO)       # corta a metade de baixo do sol
    barra(0, 36, 64, 3.4, SOL)                       # a linha d'agua
    barra(8, 45, 48, 3.2, MAR, .90)                  # o mar, em dois fios que somem
    barra(16, 53, 32, 3.2, MAR, .62)
    return im.resize((lado, lado), Image.LANCZOS)


if __name__ == '__main__':
    import os
    raiz = '/home/user/santainforma'
    desenha(16).save(os.path.join(raiz, 'favicon-16.png'))
    desenha(32).save(os.path.join(raiz, 'favicon-32.png'))
    desenha(180).save(os.path.join(raiz, 'apple-touch-icon.png'))
    grande = desenha(64)
    grande.save(os.path.join(raiz, 'favicon.ico'),
                sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print('icones gerados')
