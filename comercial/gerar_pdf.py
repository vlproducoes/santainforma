# -*- coding: utf-8 -*-
"""Monta o PDF comercial a partir da mesma tabela que alimenta o site."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tabela import ESPACOS, PATROCINIOS, EDITORIAIS, COTAS, MATERIA_A_PARTIR, tudo, diario, brl
d = tudo()

def esp():
    o=''
    for _i,nome,onde,w,h,wm,hm,m in ESPACOS:
        mv = f'{wm}&times;{hm}'  # sempre explicito: travessao lia como "nao tem versao movel"
        o+=(f'<tr><th>{nome}</th><td class="px">{w}&times;{h}</td><td class="px s">{mv}</td>'
            f'<td class="o">{onde}</td><td class="n">{brl(m)}</td><td class="n s">{brl(diario(m))}</td></tr>')
    return o
def tr3(itens):
    return ''.join(f'<tr><th>{i[1]}</th><td class="o">{i[2]}</td><td class="n">{brl(i[3])}</td></tr>' for i in itens)
def tr4(itens):
    return ''.join(f'<tr><th>{i[1]} &middot; {i[2]}</th><td class="o">{i[3]}</td><td class="n">{brl(i[4])}</td></tr>' for i in itens)
HTML = f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<style>
@page{{size:A4;margin:14mm 13mm}}
*{{box-sizing:border-box}}
body{{font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;color:#0A1F28;margin:0;font-size:9.6pt;line-height:1.45;print-color-adjust:exact;-webkit-print-color-adjust:exact}}
h1,h2,h3{{margin:0;letter-spacing:-.02em}}
.capa{{background:#0A1F28;color:#F1F5F3;padding:15mm 16mm;margin:-14mm -13mm 7mm;break-after:avoid}}
.capa .marca{{font-size:26pt;font-weight:800;letter-spacing:-.02em}}
.capa .marca em{{font-style:normal;color:#FFB627}}
.capa .tag{{font-size:8pt;letter-spacing:.28em;text-transform:uppercase;color:#8FB0B9;margin-top:3mm}}
.capa h1{{font-size:20pt;font-weight:800;margin-top:12mm;max-width:15cm;line-height:1.15}}
.capa p{{color:#CFE0E5;margin-top:4mm;max-width:15cm;font-size:10pt}}
.capa .val{{margin-top:10mm;font-size:8pt;letter-spacing:.2em;text-transform:uppercase;color:#FFB627}}
h2{{font-size:13pt;font-weight:800;color:#11485B;margin:6mm 0 2mm;padding-bottom:1.5mm;border-bottom:2px solid #FFB627}}
.sub{{color:#5A7078;margin:0 0 3mm;font-size:9pt}}
table{{width:100%;border-collapse:collapse;margin-bottom:3mm}}
th,td{{padding:2.1mm 2.4mm;text-align:left;border-bottom:.5pt solid #9F8A6A;vertical-align:top}}
thead th{{background:#11485B;color:#F1F5F3;font-size:7.4pt;letter-spacing:.07em;text-transform:uppercase;border:0;white-space:nowrap}}
tbody th{{font-weight:700;white-space:nowrap;width:1%}}
td.px{{font-weight:700;color:#11485B;white-space:nowrap}}
td.n{{text-align:right;font-weight:800;color:#11485B;white-space:nowrap}}
td.o{{color:#5A7078;font-size:8.6pt}}
.s{{color:#5A7078;font-weight:600}}
tbody tr:nth-child(even){{background:#F1F5F3}}
.box{{border-left:2.4pt solid #FFB627;background:#F1F5F3;padding:3.2mm 4mm;margin:3mm 0;font-size:8.8pt}}
.box b{{color:#11485B}}
.duas{{display:grid;grid-template-columns:1fr 1fr;gap:5mm}}
ul{{margin:1mm 0;padding-left:4.5mm}}
li{{margin-bottom:1.2mm;font-size:8.8pt}}
.pe{{margin-top:6mm;padding-top:2.5mm;border-top:.6pt solid #CFC4B4;font-size:7.6pt;color:#5A7078;line-height:1.5}}
/* PAGINACAO
   Sem regra explicita o navegador quebra onde calha, e cortava a tabela de
   Patrocinio depois da primeira linha, deixando titulo e subtitulo sozinhos
   no pe da pagina. */
.quebra{{break-before:page}}
h2{{break-after:avoid}}
.sub{{break-after:avoid}}
table{{break-inside:avoid}}
thead{{display:table-header-group}}
tr{{break-inside:avoid}}
.box,.pe,.duas{{break-inside:avoid}}
p,li{{orphans:2;widows:2}}
</style></head><body>

<div class="capa">
  <div class="marca">SANTA <em>INFORMA</em></div>
  <div class="tag">Litoral de Santa Catarina</div>
  <h1>Tabela de preços 2026</h1>
  <p>Notícia de Itapema, da Costa Esmeralda e de Santa Catarina, com formato próprio de leitura e apuração em fonte oficial.</p>
  <div class="val">Vigência: agosto a dezembro de 2026</div>
</div>

<h2>Espaços de anúncio</h2>
<p class="sub">Todo espaço tem área reservada no layout, então o anúncio não empurra o texto quando carrega. A arte é entregue no tamanho da coluna Desktop e aparece assim em tela larga. Entre 760 px e 1120 px ela é reduzida proporcionalmente, sem cortar nada. Abaixo de 760 px entra a arte de celular. A coluna Diário é o mensal dividido por 30, e serve para comparar com o que você já gasta em outro lugar.</p>
<table><thead><tr><th>Espaço</th><th>Desktop</th><th>Celular</th><th>Onde aparece</th><th>Mensal</th><th>Diário</th></tr></thead><tbody>{esp()}</tbody></table>

<h2>Patrocínio de seção</h2>
<p class="sub">Não é banner. Sua marca assina a seção, com exclusividade, e aparece junto do conteúdo.</p>
<table><thead><tr><th>Seção</th><th>O que inclui</th><th>Mensal</th></tr></thead><tbody>{tr3(PATROCINIOS)}</tbody></table>

<div class="quebra"></div>
<h2>Publieditorial</h2>
<p class="sub">Texto escrito pela nossa redação, sobre o que você quer mostrar. Sai com selo de Publieditorial e o nome de quem pagou, em área separada da cobertura. Link permanente.</p>
<table><thead><tr><th>Formato</th><th>O que inclui</th><th>Valor</th></tr></thead><tbody>{tr4(EDITORIAIS)}</tbody></table>

<h2>Cotas fechadas</h2>
<p class="sub">Para quem quer o site inteiro, ou a temporada inteira.</p>
<table><thead><tr><th>Cota</th><th>O que inclui</th><th>Valor</th></tr></thead><tbody>{tr3(COTAS)}</tbody></table>

<h2>Incluído em qualquer contratação</h2>
<div class="duas">
  <div>
    <ul>
      <li><b>Uma matéria por mês</b> a partir de {brl(MATERIA_A_PARTIR)} mensais, escrita pela nossa redação, sobre o seu negócio ou sobre um assunto que interessa a você.</li>
      <li><b>Troca de arte</b> sem custo, até duas vezes por mês.</li>
    </ul>
  </div>
  <div>
    <ul>
      <li><b>Área separada</b> da cobertura, sempre identificada.</li>
      <li><b>Um espaço, um dono.</b> Enquanto for seu, não é de mais ninguém.</li>
    </ul>
  </div>
</div>

<div class="box">
  <b>Por que este portal.</b> O Santa Informa cobre Itapema e a Costa Esmeralda com apuração em fonte oficial, foto do próprio fato e um formato de leitura que é só nosso: cada matéria tem versão de 30 segundos, versão completa e três colunistas com olhares diferentes sobre o mesmo assunto. Quem entra fica mais tempo, porque tem mais de um jeito de ler.
</div>

<div class="pe">
  <b>Santa Informa</b> &middot; CNPJ 51.087.731/0001-57 &middot; Responsável: Lucas Esmerio Varela &middot; Itapema, Santa Catarina<br>
  vl7producoes@gmail.com &middot; santainforma.com.br/anuncie.html<br>
  Valores em reais, por mês, sem reajuste durante a vigência do contrato. Tabela sujeita a alteração mediante aviso prévio.
</div>

</body></html>'''
open('/tmp/tabela-santainforma.html','w',encoding='utf-8').write(HTML)
print('  HTML do PDF gerado')
