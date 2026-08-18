# -*- coding: utf-8 -*-
"""Monta a pagina anuncie.html a partir da tabela. Fonte unica de preco."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tabela import ESPACOS, PATROCINIOS, EDITORIAIS, COTAS, MATERIA_A_PARTIR, tudo, diario, brl

BASE = '/Users/viniciusdelego/Documents/santainforma'
MODELO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modelo')
cab = open(f'{MODELO}/tpl-cab.txt', encoding='utf-8').read()
topo = open(f'{MODELO}/tpl-topo.txt', encoding='utf-8').read()
rod = open(f'{MODELO}/tpl-rod.txt', encoding='utf-8').read()

# O Open Graph entra aqui, e nao no modelo: assim ele acompanha a pagina
# mesmo que o cabecalho seja trocado por outro.
if 'og:title' not in cab:
    import re as _re
    _m = _re.search(r'( *)<link rel="canonical"[^>]*>\n', cab)
    if _m:
        _og = ('<meta property="og:title" content="Anuncie no Santa Informa">\n'
               '  <meta property="og:description" content="Formatos, tamanhos em pixels e preços do Santa Informa. '
               'Banner, retângulo, patrocínio de seção e publieditorial, com valor mensal e diário.">\n'
               '  <meta property="og:type" content="website">\n'
               '  <meta property="og:url" content="https://santainforma.com.br/anuncie.html">\n')
        cab = cab[:_m.end()] + _m.group(1) + _og + cab[_m.end():]
d = tudo()

def linhas_espacos():
    o = ''
    for _id, nome, onde, w, h, wm, hm, mensal in ESPACOS:
        movel = f'{wm} &times; {hm}' if (wm, hm) != (w, h) else 'mesmo tamanho'
        o += (f'      <tr><th scope="row">{nome}</th>'
              f'<td><b>{w} &times; {h}</b></td><td>{movel}</td>'
              f'<td>{onde}</td><td class="n">{brl(mensal)}</td><td class="n">{brl(diario(mensal))}</td></tr>\n')
    return o

def linhas(itens, colunas=3):
    o = ''
    for it in itens:
        if colunas == 3:
            _id, nome, desc, v = it
            o += f'      <tr><th scope="row">{nome}</th><td>{desc}</td><td class="n">{brl(v)}</td></tr>\n'
        else:
            _id, nome, qtd, desc, v = it
            o += f'      <tr><th scope="row">{nome} &middot; {qtd}</th><td>{desc}</td><td class="n">{brl(v)}</td></tr>\n'
    return o

MAIN = f'''<main id="conteudo" class="com-capa">

<section class="editoria-topo">
  <div class="wrap">
    <p class="trilha"><a href="index.html">Início</a><i>&rsaquo;</i>Comercial</p>
    <h1><svg class="icone" aria-hidden="true"><use href="#i-moeda"></use></svg>Anuncie no Santa Informa</h1>
    <p>Formatos, tamanhos em pixels e preços. Sem letra miúda.</p>
    <p class="conta">Tabela vigente &middot; agosto a dezembro de 2026</p>
  </div>
</section>
<div class="onda" aria-hidden="true"><svg viewBox="0 0 1200 40" preserveAspectRatio="none"><path d="M0 40V18c120 0 180 14 300 14s180-22 300-22 180 18 300 18 180-12 300-12v24z"/></svg></div>

<div class="wrap estreito texto">

  <h2><svg class="icone" aria-hidden="true"><use href="#i-predio"></use></svg><span>Espaços de anúncio</span></h2>
  <p>Todo espaço tem área reservada no layout, então o anúncio não empurra o texto quando carrega. O tamanho de celular é o que aparece em tela de até 760 px de largura.</p>
  <p>A arte é entregue no tamanho da coluna Desktop, e é assim que ela aparece em tela larga. Entre 760 px e 1120 px a peça é reduzida proporcionalmente, sem cortar nada. Abaixo de 760 px entra a arte de celular.</p>

  <div class="tabela-rolagem" tabindex="0" role="region" aria-labelledby="cap-espacos">
    <table class="preco">
      <caption id="cap-espacos" class="so-leitor">Espaços de anúncio, com tamanho em pixels e preço mensal e diário</caption>
      <thead><tr><th scope="col">Espaço</th><th scope="col">Desktop</th><th scope="col">Celular</th><th scope="col">Onde aparece</th><th scope="col">Mensal</th><th scope="col">Diário</th></tr></thead>
      <tbody>
{linhas_espacos()}      </tbody>
    </table>
  </div>

</div>

<section class="escuro">
  <div class="wrap">
    <div class="titulo"><h2><svg class="icone" aria-hidden="true"><use href="#i-predio"></use></svg><span>Veja o tamanho de verdade</span></h2><em>Tamanho real em tela larga</em></div>
    <p class="linhafina">Cada bloco abaixo tem a medida exata do espaço no site. Em tela larga aparece o formato de desktop. No celular aparece o formato de celular, que é o que a maioria dos seus clientes vê.</p>

    <div class="anuncio a-super escuro">
      <span class="rotulo">Super Banner, Billboard e Banner de editoria</span>
      <b class="medida">970 &times; 250 px</b>
      <span class="onde">Topo e meio da página inicial, e no alto das editorias.</span>
    </div>

    <div class="anuncio a-faixa escuro">
      <span class="rotulo">Banner de matéria e Banner do arquivo</span>
      <b class="medida">728 &times; 90 px</b>
      <span class="onde">Meio do texto das matérias.</span>
    </div>

    <div class="formatos">
      <div class="anuncio a-ret escuro">
        <span class="rotulo">Retângulo</span>
        <b class="medida">300 &times; 250 px</b>
        <span class="onde">Home e fim de matéria.</span>
      </div>
      <div class="anuncio a-selo escuro">
        <span class="rotulo">Selo de apoio</span>
        <b class="medida">300 &times; 90 px</b>
      </div>
    </div>
  </div>
</section>
<div class="onda" aria-hidden="true"><svg viewBox="0 0 1200 40" preserveAspectRatio="none"><path d="M0 40V18c120 0 180 14 300 14s180-22 300-22 180 18 300 18 180-12 300-12v24z"/></svg></div>

<div class="wrap estreito texto">

  <h2><svg class="icone" aria-hidden="true"><use href="#i-estrela"></use></svg><span>Patrocínio de seção</span></h2>
  <p>Aqui não é banner. Sua marca assina a seção, com exclusividade, e aparece junto do conteúdo.</p>
  <div class="tabela-rolagem" tabindex="0" role="region" aria-labelledby="cap-patrocinio">
    <table class="preco">
      <caption id="cap-patrocinio" class="so-leitor">Patrocínios de seção e preço mensal</caption>
      <thead><tr><th scope="col">Seção</th><th scope="col">O que inclui</th><th scope="col">Mensal</th></tr></thead>
      <tbody>
{linhas(PATROCINIOS)}      </tbody>
    </table>
  </div>

  <h2><svg class="icone" aria-hidden="true"><use href="#i-livro"></use></svg><span>Publieditorial</span></h2>
  <p>Conteúdo escrito pela nossa redação, no nosso jeito de contar, sobre o que você quer mostrar. Sai sempre com <strong>selo de Publieditorial e o nome de quem pagou</strong>, e fica em área separada da cobertura. Link permanente.</p>
  <div class="tabela-rolagem" tabindex="0" role="region" aria-labelledby="cap-publieditorial">
    <table class="preco">
      <caption id="cap-publieditorial" class="so-leitor">Publieditorial por quantidade e preço</caption>
      <thead><tr><th scope="col">Formato</th><th scope="col">O que inclui</th><th scope="col">Valor</th></tr></thead>
      <tbody>
{linhas(EDITORIAIS, 4)}      </tbody>
    </table>
  </div>

  <h2><svg class="icone" aria-hidden="true"><use href="#i-sol"></use></svg><span>Cotas fechadas</span></h2>
  <p>Para quem quer o site inteiro, ou a temporada inteira.</p>
  <div class="tabela-rolagem" tabindex="0" role="region" aria-labelledby="cap-cotas">
    <table class="preco">
      <caption id="cap-cotas" class="so-leitor">Cotas fechadas e preço</caption>
      <thead><tr><th scope="col">Cota</th><th scope="col">O que inclui</th><th scope="col">Valor</th></tr></thead>
      <tbody>
{linhas(COTAS)}      </tbody>
    </table>
  </div>

  <h2><svg class="icone" aria-hidden="true"><use href="#i-escudo"></use></svg><span>Incluído em qualquer contratação</span></h2>
  <div class="dados">
    <div class="d"><svg class="icone" aria-hidden="true"><use href="#i-livro"></use></svg><b>Uma matéria por mês</b><small>A partir de {brl(MATERIA_A_PARTIR)} mensais. Escrita pela nossa redação, sobre o seu negócio ou sobre um assunto que interessa a você.</small></div>
    <div class="d"><svg class="icone" aria-hidden="true"><use href="#i-relogio"></use></svg><b>Troca de arte</b><small>Sem custo, até duas vezes por mês.</small></div>
    <div class="d"><svg class="icone" aria-hidden="true"><use href="#i-balanca"></use></svg><b>Área separada</b><small>Fora da cobertura editorial, sempre com identificação clara.</small></div>
    <div class="d"><svg class="icone" aria-hidden="true"><use href="#i-escudo"></use></svg><b>Um espaço, um dono</b><small>Enquanto o espaço for seu, não é de mais ninguém.</small></div>
  </div>

  <h2><svg class="icone" aria-hidden="true"><use href="#i-carta"></use></svg><span>Falar com a gente</span></h2>
  <p>Escreva para <a href="mailto:vl7producoes@gmail.com">vl7producoes@gmail.com</a> dizendo qual espaço interessa e por quanto tempo. Respondemos com a proposta e a arte de exemplo.</p>
  <p class="fonte">Santa Informa &middot; CNPJ 51.087.731/0001-57 &middot; Itapema, Santa Catarina. Valores em reais, por mês, sem reajuste durante a vigência do contrato. Tabela sujeita a alteração mediante aviso prévio.</p>

</div>
</main>'''

pagina = cab + '</head>\n' + topo + MAIN + rod
import re
err = [t for t in ['div','section','main','p','ul','li','h1','h2','table','thead','tbody','tr','th','td','span','b','em','a','nav','header','footer','script']
       if len(re.findall(f'<{t}[ >]', pagina)) != pagina.count(f'</{t}>')]
if err: raise SystemExit(f'RECUSADO: {err}')
open(f'{BASE}/anuncie.html','w',encoding='utf-8').write(pagina)
print('  anuncie.html gerado')
