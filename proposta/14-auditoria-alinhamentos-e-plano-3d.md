# Fechamento do pacote · Capa v2

Verifiquei cada achado no código antes de aceitar. Arquivos conferidos: `/Users/viniciusdelego/Documents/santainforma/estilo.css`, `index.html`, `anuncie.html`, `noticias.html`, `sobre.html`, `regiao.html`, `visual.js`. Todos os seletores citados existem nas linhas citadas. Escopo confirmado por grep: `.manchete`, `.pilha`, `.semana`, `.dados-capa`, `.onda-pausa` só existem em `index.html`; `.numeros` existe nas 13 páginas de arquivo; `.dados` sem `dados-capa` vive em regiao, horoscopo e anuncie e não é tocado por nenhum patch abaixo.

---

## 1 · Correções de alinhamento confirmadas

Nenhum achado foi descartado por não proceder. Um patch de auditor estava errado e foi corrigido (item 5). Um achado foi reclassificado como decisão de editor (item 11). Auditor de matéria: zero achados, nada a fazer.

### GRAVE

**1. Paginação vaza 87px para cada lado no celular** · `estilo.css:328`
Confirmado: 13 botões de 36px + 12 gaps de 8px = 564px, sem quebra, num viewport de 390px. Vale para as 13 páginas de arquivo.

```css
/* linha 328, trocar */
.paginacao .numeros{display:flex;gap:8px}
/* por */
.paginacao .numeros{display:flex;flex-wrap:wrap;justify-content:center;gap:8px}
```

### MÉDIO

**2. Cabeçalho de coluna de dinheiro alinhado à esquerda, valores à direita** · `anuncie.html` + `estilo.css:116`
Confirmado: linha 113 dá `text-align:left` a todo th; linha 116 dá `right` só a `td.n`; os `<th scope="col">` de Mensal, Diário e Valor não têm classe.

CSS, logo após a linha 116 (especificidade 0,2,2 vence o `table.preco thead th` de 0,1,3):
```css
table.preco th.n{text-align:right}
```
HTML, adicionar `class="n"` nos th de dinheiro das quatro tabelas:
- linha 131: `<th scope="col" class="n">Mensal</th><th scope="col" class="n">Diário</th>`
- linha 187: `<th scope="col" class="n">Mensal</th>`
- linhas 201 e 215: `<th scope="col" class="n">Valor</th>`

**3. Vão de 111px sob a legenda da manchete, fio do rio correndo ao lado do nada** · `estilo.css:597-599`
Confirmado: `.manchete` já é flex column (588), a linha do grid é dimensionada pelo rio (8 itens), e o `aspect-ratio:3/2` da foto trava a altura. O patch funciona: em flex column o grow estoura o aspect-ratio para cima (vira mínimo, CLS zero, `object-fit:cover` absorve) e abaixo de 980px não há espaço livre, efeito nulo. Sem uso em outra página.

```css
/* linha 597, acrescentar à regra existente */
.manchete figure{margin:.5rem 0 0;overflow:hidden;animation:revela-foto .7s var(--curva-chegada) .2s both;flex:1;display:flex;flex-direction:column}
/* linha 599, acrescentar à regra existente */
.manchete figure img{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;background:var(--fio-cor);animation:foto-assenta .9s var(--curva-chegada) .2s both;flex:1 0 auto}
```

**4. Ferramentas do litoral com gap de 14px fora do gutter da capa** · `estilo.css:244`
Confirmado: `.dados{gap:14px}` na 244; `.dados-capa` só existe na home. Regra escopada, regiao/horoscopo/anuncie intactos. Colocar no bloco CAPA v2, junto da linha 723:

```css
.dados-capa{gap:clamp(16px,2.4vw,32px)}
```

**5. Card órfão na faixa tablet da linha-2 (721 a 980px)** · `estilo.css`, junto da linha 746
O problema procede (3 cards numa grade 2x1fr). **O patch do auditor não**: `.linha-2 article.card.v2:last-child:nth-child(odd)` tem especificidade (0,4,2) e venceria a regra de lista do bloco de 720px, que tem (0,3,2), quebrando o último card do mobile com colunas `1fr 220px` no lugar de `1fr 94px`. "Vem depois no arquivo" só desempata especificidade igual. Correção: mesma receita, presa na faixa por media range:

```css
@media(min-width:721px) and (max-width:980px){
  .linha-2 article.card.v2:last-child:nth-child(odd){grid-column:1/-1;display:grid;grid-template-columns:1fr 220px;gap:2px 24px}
  .linha-2 article.card.v2:last-child:nth-child(odd) figure{grid-column:2;grid-row:1/5;margin:0}
  .linha-2 article.card.v2:last-child:nth-child(odd) .capa{width:100%;height:auto;aspect-ratio:16/10}
}
```
(figure `grid-row:1/5` bate com os 4 filhos de texto do card: ed, h3, p, quando. Conferido no index.html 235-255.)

**6. Coluna do Resumo Semanal serpenteando até 7px** · `estilo.css:710`
Confirmado: `.num` da home usa `var(--corpo)` proporcional com `min-width:1.6ch` (~duas larguras de dígito não cabem). Escopo `.escuro.anoitecer` protege `.num` base (239) e `.carta .num` do horóscopo. O `min-width:2.4ch` é a trava real; `tabular-nums` iguala os dígitos onde a fonte suporta.

```css
/* linha 710, trocar */
.escuro.anoitecer .num{font-family:var(--corpo);font-weight:500;font-size:2rem;line-height:1;padding-top:0;min-width:1.6ch}
/* por */
.escuro.anoitecer .num{font-family:var(--corpo);font-weight:500;font-size:2rem;line-height:1;padding-top:0;min-width:2.4ch;font-variant-numeric:tabular-nums}
```

**7. Ícone do h2 flutuando entre as linhas quando o título quebra** · `estilo.css:407-408`
Confirmado: `align-items:center` na 407, títulos de 2-3 linhas em regiao e nas matérias. **Ajuste no valor do auditor**: com line-height herdado de 1.62 e ícone de .9em, o centro da primeira linha fica em `(1.62em − .9em)/2 = .36em`; os .18em propostos subiriam o ícone ~5px em relação ao desenho atual de linha única. Com .36em, título de uma linha rende pixel a pixel igual a hoje e o de várias linhas ancora na primeira.

```css
.texto h2{display:flex;align-items:flex-start;gap:11px}
.texto h2 .icone{color:var(--sol);width:.9em;height:.9em;margin-top:.36em}
```

### LEVE

**8. Pilha termina 80px antes do líder** · `estilo.css:680`
Confirmado: `.pilha` é flex column (679). `flex:1` distribui o vão nos três artigos; no mobile a altura é do conteúdo e nada muda.

```css
/* linha 680, acrescentar flex:1 */
.pilha article{position:relative;padding:16px 0;border-bottom:var(--fio) solid var(--fio-cor);flex:1}
```

**9. Resumo Semanal com gap de 42px fora do token** · `estilo.css:237`
Confirmado. `.semana` hoje só existe na home, mas o escopo protege uma futura página de Resumo. No bloco CAPA v2, junto da 709:

```css
.escuro.anoitecer .semana{gap:0 clamp(16px,2.4vw,32px)}
```

**10. Pausar ondas fora do prumo e 1px abaixo do alvo mínimo** · `estilo.css:582`
Confirmado: `right:14px` e altura de 23px. Com `right:24px` alinha com a margem do wrap no mobile/tablet; no desktop segue controle flutuante (o auditor de desktop já tinha aceitado esse comportamento). Padding novo dá ~27px de alvo, acima dos 24 da WCAG 2.5.8.

```css
/* na regra .onda-pausa, trocar right:14px por right:24px e padding:5px 11px por padding:7px 12px */
```

**11. Cabeçalho das internas 20px mais alto que o da home** · decisão de editor
Procede tecnicamente: nas internas a `.editorias` vive dentro do `<header>` escuro e herda o `nav{margin-top:20px}` da linha 71; na home a `.fixa` zera isso (564). O vão é breu sobre breu, invisível, e o patch `header .editorias{margin-top:0}` é seguro (não recria a faixa clara, que só aparecia fora do header). Mas muda a altura do cabeçalho de todas as internas: vai para a branch com uma nota, o editor bate o martelo entre uniformizar ou registrar como intencional.

**Entrega**: os itens 1 a 10 são conserto de defeito, mas são CSS/layout, então seguem a seção 2 do CLAUDE.md: branch única `correcoes-alinhamento`, um commit por gravidade, screenshots antes/depois em 390, 800 e 1440, aprovação do editor, merge. O item 11 vai na mesma branch como commit separado e reversível.

---

## 2 · Plano 3D

Fio condutor (das referências, e é a régua de aceitação): a profundidade do Santa Informa é **atmosférica, não geométrica**. Luz do céu, camadas de paisagem, maré, mergulho de navegação. Tudo `color-mix` sobre as 8 cores, tokens `--dur-*`/`--curva-*`, zero JS novo, zero main thread, kill switch da linha 494-495 cobrindo tudo, estado de repouso sempre neutro no `from`.

Verificações que sustentam o plano: a mola do `visual.js:383` escreve `transform:scale()` inline nos cards, então todo movimento novo usa as propriedades independentes `scale`/`translate`, que compõem sem conflito; `@view-transition{navigation:auto}` já está ativo (estilo.css:21) com `navigation:none` no reduced-motion (25); header, rodapé e barra têm `view-transition-name` próprios (22, 23, 564), logo saem do grupo `root` sozinhos.

### Entrega A · estáticos, risco mínimo

**A1. Relevo de impressão nos fios estruturais.** Profundidade de papel: fio de luz de 1px sob os traços fortes, página ganha espessura sem nada se mover. Sem fallback necessário, reduced-motion irrelevante.

```css
.titulo.regua{box-shadow:0 -1px 0 color-mix(in srgb,var(--superficie) 70%,transparent) inset}
.rio li{box-shadow:0 1px 0 color-mix(in srgb,var(--superficie) 60%,transparent)}
.rio li:last-child{box-shadow:none}
```
Risco: em DPR 1 o fio de luz sobre a espuma pode sujar; validar no screenshot 1x e, se sujar, restringir à régua.

**A2. Sombra em camadas tingida pelo céu.** Fusão das duas listas: elevação por pseudo-elemento pré-renderizado (opacidade composita; animar box-shadow repinta) e a cor da sombra acompanhando as classes `ceu-*` que o visual.js já escreve. Ao entardecer a sombra esquenta um fio de coral; ninguém nota conscientemente, e esse é o ponto.

```css
:root{
  --sombra-cor:color-mix(in srgb,var(--breu) 12%,transparent);
  --sombra-1:0 1px 2px var(--sombra-cor);
  --sombra-2:0 1px 2px var(--sombra-cor),0 6px 18px -8px var(--sombra-cor);
}
html.ceu-entardecer{--sombra-cor:color-mix(in srgb,color-mix(in srgb,var(--breu) 82%,var(--coral) 18%) 13%,transparent)}
article.card.v2,.dados-capa .d{box-shadow:var(--sombra-1)}
article.card.v2::before{content:"";position:absolute;inset:0;box-shadow:var(--sombra-2);opacity:0;transition:opacity var(--dur-troca) var(--curva-troca);pointer-events:none}
article.card.v2:hover::before,article.card.v2:has(a:focus-visible)::before{opacity:1}
```
Trava de identidade: alfa nunca acima de ~13%, senão vira Material Design em cima de um desenho de jornal impresso. (`article.card` já é `position:relative`, linha 385; `.dados-capa .d`, linha 723.)

### Entrega B · scroll-driven simples

**B1. Parallax nas capas de card.** A foto desliza 4% em contrafase dentro da janela recortada (as figures já têm `overflow:hidden`, 670 e 694). Nunca na manchete (candidata a LCP, já tem `foto-assenta`), nunca nas minis de 52/76px, e com guarda de largura para não pegar o thumb de 94px do formato lista mobile:

```css
@media(min-width:721px){
  @supports (animation-timeline:view()){
    article.card.v2 .capa,.lider-sec img{
      animation:capa-flutua linear both;
      animation-timeline:view();
      animation-range:cover 0% cover 100%;
    }
    @keyframes capa-flutua{from{scale:1.09;translate:0 -4%}to{scale:1.09;translate:0 4%}}
  }
}
```
`scale`/`translate` independentes não brigam com a mola (que escreve `transform` no article, não na img). Fallback: foto parada, idêntica a hoje. Não subir a amplitude: 1.09 já come 4,5% de borda.

**B2. Números do Semanal em contrafase.** Mesma técnica, os numerais decorativos 01-07 andam 12px como tinta atrás da lista. Não interfere na âncora `#semanal` (só transform).

```css
@supports (animation-timeline:view()){
  .escuro.anoitecer .num{animation:num-fica linear both;animation-timeline:view();animation-range:cover 0% cover 100%}
  @keyframes num-fica{from{translate:0 12px}to{translate:0 -12px}}
}
```
Nota de compatibilidade com a correção 6: `min-width:2.4ch` e `translate` convivem, nenhum ajuste.

### Entrega C · o mergulho de navegação

**C1. Palco no eixo Z: a capa recua, a matéria sobe.** Das referências, e é o clique mais frequente do site. Como header, rodapé e barra têm nomes próprios, só o conteúdo mergulha; o voo da foto `capa-mNN` continua acontecendo por cima. Reduced-motion já mata tudo via `navigation:none`.

```css
::view-transition-old(root){animation:vt-recua var(--dur-troca) var(--curva-troca) both}
::view-transition-new(root){animation:vt-chega var(--dur-troca) var(--curva-chegada) both}
@keyframes vt-recua{to{opacity:0;transform:scale(.985)}}
@keyframes vt-chega{from{opacity:0;transform:translateY(12px)}}
```
(Substituir a animação padrão exige repor a opacidade nos keyframes, já está reposto acima.)

### Entrega D · o horizonte, com medição antes do commit

**D1. Multiplano: ondas em contrafase na saída e o sol que fica no céu.** Correção técnica sobre a receita da plataforma: não precisa de wrapper nenhum. A `deriva` anima `transform` (estilo.css:580); a separação vertical vai na propriedade independente `translate`, que compõe com transform no mesmo elemento. E a camada da frente só pode descer, nunca subir, senão abre um fio de gradiente entre a onda e a página (o SVG ancora em `bottom:-1px` e o overflow só clipa para baixo).

```css
@supports (animation-timeline:view()){
  .onda-camada.tras{animation:deriva 34s linear infinite,separa-tras linear both;animation-timeline:auto,view();animation-range:normal,exit 0% exit 100%}
  .onda-camada.frente{animation:deriva 26s linear infinite,separa-frente linear both;animation-timeline:auto,view();animation-range:normal,exit 0% exit 100%}
  @keyframes separa-tras{from{translate:0 0}to{translate:0 -6px}}
  @keyframes separa-frente{from{translate:0 0}to{translate:0 6px}}
}
@supports (animation-timeline:scroll()){
  .astro{animation:sol-fica linear both;animation-timeline:scroll(root);animation-range:0 260px}
  @keyframes sol-fica{to{translate:0 22px}}
}
```
O `.astro` usa `transform:translateY(var(--astro-y))` (554); `translate` independente soma sem conflito. A terceira camada `.fundo` (~300 bytes de SVG, opacity .25, deriva 46s) só entra se o painel Layers do DevTools liberar no celular; cada camada é textura de 200% de largura. Botão Pausar ondas segue pausando a deriva; a separação é scroll-driven e não precisa de pausa (não anda sozinha).

### Descartado, com motivo

- **Tilt 3D no hover**: conflito direto com a mola do `visual.js:383` (mesmos alvos, mesmo `transform` inline), audiência majoritariamente touch, e rotacionar bloco de texto mata a nitidez de subpixel de título. É o único candidato que o leitor percebe como efeito.
- **Sombra longa na manchete**: cartaz de 2014, briga com o Archivo -0.03em, `text-shadow` multi-passo custa paint. Substituída pelo relevo de impressão (A1).
- **WebGL/Three.js, vídeo de fundo no herói**: lib externa e LCP, proibidos pela casa.
- **Scroll-jacking**: rouba a rolagem do leitor de notícia.
- **preserve-3d/flip de cartão**: profundidade literal, envelhece rápido, não conversa com a linguagem plana mar/céu/sol.
- **Cena sticky de scrollytelling**: adiada, não descartada. Só faz sentido em especial de fôlego; na home vira ruído e a matéria de 300-500 palavras não sustenta.

### Custo e processo

Pacote 3D completo: ~60 linhas de CSS, ~300 bytes de SVG opcionais, zero JS, zero dependência, nada no main thread. Arquivos: `estilo.css` (bloco CAPA v2) e `index.html` (só se a camada `.fundo` entrar). Tudo é mudança de visual: branch `capa-profundidade`, separada da branch de correções, commits na ordem A → B → C → D (D só depois da medição de GPU), screenshots e teste de reduced-motion em cada fase, aprovação do editor antes do merge, conforme a seção 2 do CLAUDE.md.