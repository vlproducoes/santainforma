#!/usr/bin/env python3
"""
Santa Informa · buscador de imagem de banco gratuito (Pexels)

Busca no Pexels, baixa, redimensiona para o padrao do site, salva em imagens/
e imprime o bloco <figure> pronto para colar na materia.

Toda imagem baixada por aqui entra como IMAGEM ILUSTRATIVA. Ela nunca pode ser
apresentada como registro do fato noticiado. Regra da secao 11 e 16 da
Constituicao Editorial.

Uso:
    python3 ferramentas/buscar-imagem.py "praia aerea santa catarina"
    python3 ferramentas/buscar-imagem.py "obra construcao civil" --nome obra-generica
    python3 ferramentas/buscar-imagem.py "camara municipal" --altura 415 --listar

Opcoes:
    --nome NOME      nome do arquivo final, sem extensao (padrao: gerado da busca)
    --largura N      largura final em px (padrao 1600)
    --altura N       altura final em px (padrao 900). Use 415 para faixa estreita.
    --listar         so mostra os candidatos, nao baixa nada
    --escolher N     baixa o candidato de numero N da lista (padrao 1)
"""

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PASTA_IMAGENS = RAIZ / "imagens"
MANIFESTO = RAIZ / "imagens" / "creditos.json"
API = "https://api.pexels.com/v1/search"


def carregar_chave():
    """Le a chave do ambiente ou do arquivo .env na raiz. Nunca do Git."""
    chave = os.environ.get("PEXELS_API_KEY")
    if chave:
        return chave.strip()

    env = RAIZ / ".env"
    if env.exists():
        for linha in env.read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if linha.startswith("PEXELS_API_KEY="):
                return linha.split("=", 1)[1].strip().strip('"').strip("'")

    sys.exit(
        "Chave do Pexels nao encontrada.\n"
        "Crie um arquivo .env na raiz do projeto com esta linha:\n"
        "    PEXELS_API_KEY=sua_chave_aqui\n"
        "O .env ja esta no .gitignore, entao ele nao vai pro GitHub."
    )


def escorregar(texto):
    """Transforma texto em slug de arquivo: sem acento, minusculo, com hifen."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii").lower()
    texto = re.sub(r"[^a-z0-9]+", "-", texto).strip("-")
    return texto[:60] or "imagem"


def buscar(chave, termo, quantidade=8):
    url = f"{API}?" + urllib.parse.urlencode(
        {"query": termo, "per_page": quantidade, "orientation": "landscape"}
    )
    # O Pexels responde 403 para o User-Agent padrao do urllib. Precisa declarar um.
    req = urllib.request.Request(
        url, headers={"Authorization": chave, "User-Agent": "SantaInforma/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("photos", [])


def baixar(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": "SantaInforma/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        destino.write_bytes(r.read())


def ajustar(caminho, largura, altura):
    """Corta pelo centro e redimensiona. Sem Pillow, mantem o arquivo original."""
    try:
        from PIL import Image
    except ImportError:
        print("  Aviso: Pillow nao instalado, imagem salva no tamanho original.")
        print("  Para cortar automatico: pip3 install Pillow")
        return None

    with Image.open(caminho) as img:
        img = img.convert("RGB")
        alvo = largura / altura
        atual = img.width / img.height

        if atual > alvo:
            nova_largura = int(img.height * alvo)
            corte = (img.width - nova_largura) // 2
            img = img.crop((corte, 0, corte + nova_largura, img.height))
        else:
            nova_altura = int(img.width / alvo)
            corte = (img.height - nova_altura) // 2
            img = img.crop((0, corte, img.width, corte + nova_altura))

        img = img.resize((largura, altura), Image.LANCZOS)
        img.save(caminho, "JPEG", quality=82, optimize=True, progressive=True)
    return caminho.stat().st_size


def registrar(nome_arquivo, foto, termo):
    """Guarda a origem de cada imagem. Trilha de auditoria da equipe Riscos."""
    dados = {}
    if MANIFESTO.exists():
        dados = json.loads(MANIFESTO.read_text(encoding="utf-8"))

    dados[nome_arquivo] = {
        "banco": "Pexels",
        "licenca": "Pexels License (uso comercial livre, atribuicao nao obrigatoria)",
        "uso": "imagem ilustrativa",
        "fotografo": foto["photographer"],
        "url_fotografo": foto["photographer_url"],
        "url_original": foto["url"],
        "id_pexels": foto["id"],
        "termo_de_busca": termo,
        "baixada_em": date.today().isoformat(),
    }
    MANIFESTO.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def bloco_figure(nome_arquivo, largura, altura, foto):
    return f"""  <figure class="foto">
    <img src="imagens/{nome_arquivo}" width="{largura}" height="{altura}" loading="lazy" decoding="async"
         alt="ESCREVA AQUI o que a imagem mostra, em uma frase, para quem nao enxerga.">
    <figcaption>ESCREVA AQUI a legenda de contexto.
      <span class="credito">Imagem ilustrativa · {foto['photographer']}/Pexels</span></figcaption>
  </figure>"""


def main():
    p = argparse.ArgumentParser(description="Busca imagem gratuita no Pexels")
    p.add_argument("termo", help="o que procurar, entre aspas")
    p.add_argument("--nome", help="nome do arquivo final, sem extensao")
    p.add_argument("--largura", type=int, default=1600)
    p.add_argument("--altura", type=int, default=900)
    p.add_argument("--listar", action="store_true", help="so lista, nao baixa")
    p.add_argument("--escolher", type=int, default=1, help="qual candidato baixar")
    a = p.parse_args()

    chave = carregar_chave()
    fotos = buscar(chave, a.termo)

    if not fotos:
        sys.exit(f"Nenhum resultado para: {a.termo}")

    print(f"\n{len(fotos)} resultados para \"{a.termo}\":\n")
    for i, f in enumerate(fotos, 1):
        marca = "->" if i == a.escolher and not a.listar else "  "
        print(f"{marca} {i}. {f['alt'][:70] or '(sem descricao)'}")
        print(f"      {f['photographer']} · {f['width']}x{f['height']} · {f['url']}")

    if a.listar:
        print("\nRode de novo com --escolher N para baixar um deles.")
        return

    if not 1 <= a.escolher <= len(fotos):
        sys.exit(f"\nEscolha invalida. Use um numero de 1 a {len(fotos)}.")

    foto = fotos[a.escolher - 1]
    nome = escorregar(a.nome or a.termo) + ".jpg"
    destino = PASTA_IMAGENS / nome
    PASTA_IMAGENS.mkdir(exist_ok=True)

    print(f"\nBaixando candidato {a.escolher}...")
    baixar(foto["src"]["original"], destino)
    tamanho = ajustar(destino, a.largura, a.altura)

    registrar(nome, foto, a.termo)

    kb = (tamanho or destino.stat().st_size) // 1024
    print(f"Salvo: imagens/{nome} ({kb} KB)")
    print(f"Origem registrada em imagens/creditos.json")
    print("\nCole este bloco na materia e preencha o alt e a legenda:\n")
    print(bloco_figure(nome, a.largura, a.altura, foto))
    print()


if __name__ == "__main__":
    main()
