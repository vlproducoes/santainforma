Analisei `index.html`, `estilo.css` (501 linhas), `visual.js` e a matéria canônica. O que segue é o sistema tipográfico e de grid do redesign, calibrado para o que o site é: portal estático, leitor de celular intermediário, receita vinda de Core Web Vitals.

**Nota de honestidade técnica antes de tudo.** Nada nesta camada precisa de WebGL, Three.js, GSAP, Lenis ou WebAssembly. O "moderno" em tipografia editorial hoje é CSS puro: fontes variáveis (já carregadas), `clamp()`, grid nomeado, `text-wrap`, `initial-letter`, animação por scroll-timeline (o site já usa na barra de progresso). Zeit Online e NYT entregam a percepção de qualidade deles com exatamente essas ferramentas. Biblioteca de animação aqui só adicionaria peso ao LCP sem mover a percepção de qualidade um milímetro.

---

## 1. Escala tipográfica com clamp()

Fluida entre 400px e 1180px de viewport (a largura do `.wrap`). Nove papéis, tudo com as fontes já carregadas. Tokens para o topo do `estilo.css`:

```css
:root{
  /* papéis tipográficos */
  --t-manchete:   clamp(1.9rem,  1.13rem + 3.08vw, 3.4rem);   /* 30 → 54px */
  --t-capa-lead:  clamp(1.625rem, 1.05rem + 2.31vw, 2.75rem); /* 26 → 44px, manchete da home */
  --t-secao:      clamp(1.19rem, 1.06rem + .51vw, 1.44rem);   /* 19 → 23px */
  --t-card:       clamp(1.0625rem, .95rem + .45vw, 1.28rem);  /* 17 → 20.5px */
  --t-linhafina:  clamp(1.0625rem, .97rem + .38vw, 1.25rem);  /* 17 → 20px */
  --t-corpo:      clamp(1.0625rem, 1rem + .26vw, 1.1875rem);  /* 17 → 19px */
  --t-intertitulo:clamp(1.25rem, 1.12rem + .51vw, 1.5rem);    /* 20 → 24px */
  --t-legenda:    clamp(.85rem, .8rem + .2vw, .95rem);        /* 13.6 → 15.2px */
  --t-ui:         clamp(.72rem, .68rem + .18vw, .81rem);      /* 11.5 → 13px */
  --t-num:        clamp(1.625rem, 1.3rem + 1.28vw, 2.25rem);  /* 26 → 36px, dados do Raio-X */
}
```

Especificação por papel:

| Papel | Fonte | Peso | line-height | letter-spacing |
|---|---|---|---|---|
| Manchete de matéria | **Newsreader, opsz 72** | 600 | 1.1 | -0.01em |
| Manchete da capa | Archivo | 800 | 1.05 | -0.03em |
| Título de card | Archivo | 800 | 1.18 | -0.015em |
| Linha fina | Newsreader | 500 | 1.45 | 0 |
| Corpo | Newsreader | 400 | 1.6 | 0 |
| Intertítulo | Archivo | 800 | 1.25 | -0.015em |
| Legenda | Newsreader | 400 | 1.5 | 0 |
| UI / chapéu / data | Archivo | 600 | 1.2 | .09em a .13em, caixa alta |
| Número de dado | Archivo | 800, `tabular-nums` | 1.1 | -0.02em |

**A jogada de maior impacto e custo zero: manchete de matéria em Newsreader opsz 72.** O eixo óptico do Newsreader vai de 6 a 72 e hoje o site só usa o miolo dele (o navegador, com `font-optical-sizing:auto`, aplica opsz igual ao tamanho em px, então o corpo a 18px recebe o corte 18). Forçar o corte display na manchete entrega um desenho de alto contraste, serifa fina, espaçamento fechado, que o arquivo já contém:

```css
.hero h1{
  font-family:var(--corpo);
  font-size:var(--t-manchete);
  font-weight:600;
  font-variation-settings:'opsz' 72; /* desliga o auto de propósito, corte display */
  line-height:1.1; letter-spacing:-.01em; max-width:22ch;
}
```

Isso cria o sistema de duas vozes do Zeit: serifa na matéria (voz de leitura, autoridade), sans na capa e nos cards (voz de fluxo, velocidade). O peso 600 já está carregado. Zero bytes novos. Manter Archivo 800 na capa preserva a marca.

No outro extremo do eixo: legendas podem forçar `'opsz' 10` para ganhar robustez em corpo pequeno (desenho mais aberto, serifa mais grossa). Ganho sutil, custo zero, aplicar em `figcaption`.

**Sobre trocar ou acrescentar fonte: não trocar.** Archivo + Newsreader é um par legítimo (Grilli faria pares assim). Dois acréscimos opcionais, ambos Google Fonts:

1. **Itálico do Newsreader**, hoje ausente. O site não tem como grifar título de obra nem citação com ênfase. Custo: um woff2 a mais, na casa de 30 a 50 KB, no mesmo request CSS. URL: `family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..600`. Recomendo entrar.
2. **Trocar os pesos discretos por sintaxe de intervalo** (`Archivo:wght@400..800`), que serve o arquivo variável: pesos 500 e 700 ficam disponíveis de graça para hierarquias intermediárias. O peso total muda pouco (medir no DevTools, esperar variação de ±20 KB). Recomendo, mas medir antes.

---

## 2. Grid da home: assimetria editorial

Hoje a capa é carrossel 2-up + grade uniforme de 3 colunas. Uniformidade comunica que tudo tem o mesmo peso, e jornal vive de dizer o que importa mais. Proposta: **pacote de capa 8/4 sobre grid de 12 colunas**, no lugar do carrossel como abre.

```
┌────────────────────────────────┬───────────────┐
│  MANCHETE (col 1–8)            │ RIO DE ÚLTIMAS│
│  imagem 16:9, fetchpriority    │ (col 9–12)    │
│  chapéu + título --t-capa-lead │ 5–6 itens,    │
│  + linha fina                  │ hora + título,│
│                                │ filete entre  │
├──────────┬──────────┬──────────┤ eles          │
│ card 2   │ card 3   │ card 4   │ (continua)    │
└──────────┴──────────┴──────────┴───────────────┘
```

```css
.capa-grade{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));
  column-gap:clamp(16px,2.4vw,32px);row-gap:var(--esp-6)}
.capa-manchete{grid-column:1/9}
.capa-rio{grid-column:9/13;border-left:var(--fio) solid var(--areia);
  padding-left:clamp(16px,2vw,28px)}
.capa-banda{grid-column:1/9;display:grid;grid-template-columns:repeat(3,1fr)}
```

Matemática no `.wrap` de 1180px (1132 úteis): coluna de ~69px com gutter de 28px. A manchete ocupa 745px (imagem 16:9 de 419px de altura, título a 44px rende ~28 caracteres por linha, duas linhas). O rio ocupa 359px, onde o retângulo 300×250 do AdSense cabe com folga no fim da coluna.

**Como a manchete domina:** 2/3 da largura, título com o dobro do corpo do título de card, único elemento da capa com letter-spacing -0.03em e com o filete duplo (item 4) acima do chapéu. Um só protagonista por dobra.

**O rio de últimas** é o padrão Zeit ("Schlagzeilen"): hora em Archivo 600 `tabular-nums` cor `--suave`, título em Archivo 600 (não 800: o rio é ruído de fundo, a manchete é o sinal), filete de 1px entre itens, sem imagem (ou miniatura de 56px no máximo). Alimenta o hábito de recarregar a página, que é o comportamento que sustenta portal regional.

**Banda de editorias abaixo:** a `.grade` atual continua, com uma assimetria por bloco: o primeiro card de cada editoria vira destaque duplo, `grid-column:span 2` com imagem 2:1 e título em `--t-capa-lead` reduzido. Um seletor resolve: `.grade-ed>article:first-child{grid-column:span 2}`.

**Quebras:** abaixo de 1020px o rio desce para baixo da manchete como lista; abaixo de 720px tudo vira uma coluna na ordem manchete → rio (4 itens) → cards. No celular, os cards trocam imagem em cima por **linha de lista com miniatura de 88px à direita** (padrão NYT mobile): três matérias visíveis por tela em vez de uma e meia. Densidade é respeito pelo 4G do leitor.

**Efeito colateral em Web Vitals:** o carrossel como abre faz o LCP depender de imagem com overlay e concorre com JS. O pacote estático melhora LCP (uma imagem `fetchpriority="high"` com `aspect-ratio` reservado, texto do rio renderiza instantâneo) e reduz INP. Se o editor quiser manter o carrossel, ele desce para depois da banda, com toda a acessibilidade atual intacta (pausa, pontos, teclado). Nada do que existe de a11y regride.

---

## 3. Ritmo vertical, densidade e medida

Escala de espaçamento em base 4, com os saltos grandes fluidos:

```css
:root{
  --esp-1:.25rem; --esp-2:.5rem; --esp-3:.75rem; --esp-4:1rem;
  --esp-5:1.5rem; --esp-6:2rem;
  --esp-7:clamp(2.5rem,2rem + 1.5vw,3.5rem);   /* entre blocos */
  --esp-secao:clamp(3rem,2.2rem + 2.5vw,4.5rem); /* entre seções */
}
```

Regras de ritmo:

- Parágrafo: margem inferior 0.9em (relativa ao corpo, escala junto).
- Intertítulo: 2.2em acima, 0.6em abaixo. O espaço pertence a quem vem antes, o título cola no texto que anuncia.
- Figura: `--esp-6` acima e abaixo; legenda a 0.5em da imagem.
- Card: padding interno cai de 24/22px para 18/20px, gap interno de 8px. Em portal, ar demais dentro do card lê como página institucional.

**Medida por papel** (a régua que mais muda percepção de qualidade):

| Papel | Medida ideal |
|---|---|
| Corpo de matéria | **62 a 66ch** |
| Linha fina | 45 a 55ch |
| Manchete | 20 a 22ch (via max-width) |
| Legenda | 55ch |
| Título de card | ~38ch (a coluna já garante) |

O `.estreito` atual (760px, 712 úteis) rende perto de 80ch a 18px de Newsreader. Está largo, e é a correção mais barata de todo o redesign: **coluna de leitura a 65ch** (`max-width:65ch` no bloco de texto, ~630px), com figuras, box destaque e anúncios sangrando até os 760px do contêiner. Texto estreito com mídia mais larga é o ritmo de página do Zeit, e a alternância cria respiração vertical sem custar uma linha de JS.

---

## 4. Detalhes finos: o que cada um custa e onde entra

**Capitular (`initial-letter`).** Três linhas, Archivo 800, cor `--mar`, só no primeiro parágrafo de "Entenda o assunto". Chrome 110+ e Safari; Firefox ignora e mostra letra normal, sem quebra. Custo: ~6 linhas de CSS dentro de `@supports(initial-letter:3)`. Zero CLS porque é CSS presente desde o primeiro paint. É o detalhe de maior retorno visual da lista.

```css
@supports(initial-letter:3){
  .texto .abre::first-letter{initial-letter:3;font-family:var(--display);
    font-weight:800;color:var(--mar);padding-right:.12em}
}
```

**Filete duplo (scotch rule).** Grosso sobre fino nos `.titulo` de seção, no lugar do 2px atual: `border-bottom:3px solid var(--breu)` mais um `::after` de 1px afastado 3px. Assinatura clássica de jornal impresso, custa 4 linhas. Reservar só para títulos de seção e topo de matéria; em todo lugar vira papel de parede.

**Hairlines.** Token `--fio:1px` que vira 0.5px em telas 2x (`@media(min-resolution:2dppx){:root{--fio:.5px}}`). Aplicar nas bordas de card, separadores do rio e filete da legenda. Meio pixel físico é o que separa "site" de "publicação" em tela retina. Custo: 3 linhas.

**Numerais.** `font-variant-numeric:oldstyle-nums` no corpo (algarismos de texto, que não gritam no meio do parágrafo) e `lining-nums tabular-nums` em tabelas de preço, timestamps do rio e nos números do Raio-X. Ressalva honesta: o subsetting do Google Fonts às vezes remove features como `onum` do arquivo servido; se estiver ausente a declaração é inerte, sem efeito e sem dano. Testar no DevTools antes de dar por entregue. `tabular-nums` do Archivo tende a estar presente.

**Versaletes.** Não usar. O Google Fonts provavelmente não serve `smcp` nesses recortes e o navegador sintetizaria versaletes falsos (maiúsculas encolhidas, peso errado). A voz de caixa alta da casa já existe: Archivo 600 espacejado. Versalete verdadeiro exigiria self-host, fora do combinado.

**Pontuação pendurada.** `hanging-punctuation:first allow-end` em `.texto p` e nas manchetes. Safari apenas, uma linha, zero risco nos demais. Para aspas abrindo manchete nos outros navegadores, classe utilitária `.cita-abre{text-indent:-.45ch}` aplicada pelo editor quando o título começa com aspas.

**Ligaduras e kerning.** `liga` e `kern` já vêm ativos por padrão, não mexer. Não ligar `dlig` (ligaduras decorativas viram maneirismo em texto de notícia). Avaliar remover o `-webkit-font-smoothing:antialiased` do corpo em tela 1x: ele afina a serifa do Newsreader em monitor comum; manter só em `.escuro` (texto claro sobre fundo escuro, onde ajuda).

**Hifenização.** `hyphens:auto` com `hyphenate-limit-chars:6 3 3` no corpo abaixo de 600px. O `lang="pt-BR"` já está no html, o dicionário existe nos navegadores. Em coluna estreita de celular, elimina os buracos de `text-wrap:pretty` lutando com palavra longa.

**Aparar o leading (`text-box`).** `text-box:trim-both cap alphabetic` nas manchetes e títulos de card alinha o topo da caixa com a altura de capitular de verdade, colando título em imagem sem o respiro fantasma do line-height. Chrome 128+/Safari 18.2, progressivo, uma linha. É o detalhe mais "2026" da lista e ninguém percebe conscientemente, que é o ponto.

---

## 5. Modo escuro: mapeamento das 8 variáveis

Princípio: cabeçalho, rodapé, hero e `.escuro` já são escuros e **não mudam**, são a âncora da marca nos dois modos. O que inverte é o "papel" (fundo `--espuma` e superfícies brancas). Como as variáveis atuais são cores literais usadas ora como texto, ora como superfície, inverter os 8 valores diretamente quebraria o header. A implementação correta é uma camada semântica fina por cima delas, remapeada no dark:

```css
:root{
  --fundo:var(--espuma);   --tinta:var(--breu);
  --tinta-2:var(--suave);  --superficie:#fff;
  --filete-cor:var(--areia); --link:var(--mar);
  color-scheme:light;
}
@media(prefers-color-scheme:dark){
  :root{
    --fundo:#0C181E;                 /* breu rebaixado meio tom */
    --tinta:#E9F0F1;                 /* espuma levemente aquietada */
    --tinta-2:#9FB1B6;               /* suave clareado */
    --superficie:#10222B;            /* card: mistura breu/mar */
    --filete-cor:rgba(207,196,180,.16); /* areia como véu */
    --link:var(--mar-claro);         /* #8FB0B9 assume o papel de --mar */
    color-scheme:dark;
  }
}
```

Destino de cada uma das 8, com contraste calculado (WCAG 2.x, sobre #0C181E):

| Variável | Light | Dark | Contraste no dark |
|---|---|---|---|
| `--breu` #0A1F28 | texto/superfície escura | segue sendo superfície (header) | n/a |
| `--mar` #11485B | link, acento | vira só superfície (`.escuro`); cede o papel de link | n/a |
| `--mar-claro` #8FB0B9 | texto secundário no escuro | **assume link e acento frio** | **7.9:1** ✓ |
| `--espuma` #F1F5F3 | fundo | texto principal via `--tinta` #E9F0F1 | **15:1** ✓ |
| `--sol` #FFB627 | destaque | mantém, funciona ainda melhor | **10.4:1** ✓ |
| `--coral` #D1331F | chapéu de editoria | **clarear para #F0654C** (o original dá 3.7:1, reprova em texto de 10px) | **5.8:1** ✓ |
| `--areia` #CFC4B4 | bordas | véu `rgba(207,196,180,.16)` para filetes | decorativo, ok |
| `--suave` #5A7078 | texto de apoio | #9FB1B6 | **~8:1** ✓ |

Duas cores efetivamente novas (#0C181E e #F0654C), ambas derivação direta de breu e coral por necessidade de contraste, não paleta nova; registrar isso na proposta ao editor porque a Constituição é dele. Complementos: `<meta name="color-scheme" content="light dark">` no head (evita flash branco antes do CSS), fotos com `filter:brightness(.88)` opcional no dark para não estourarem sobre fundo escuro, AdSense indiferente ao modo. O trabalho braçal do dark é trocar, nos seletores de conteúdo, `--espuma`/`#fff`/`--breu` literais pelos tokens semânticos; header, hero, footer e `.escuro` ficam intocados, o que corta o escopo pela metade.

---

**Ordem de implementação sugerida ao agente que consolidar isto:** (1) tokens de escala e espaçamento, (2) medida de 65ch na matéria, (3) manchete serifada opsz 72, (4) pacote de capa 8/4 com rio, (5) detalhes finos, (6) camada semântica + dark. Os itens 1 a 3 mudam a percepção do site inteiro e cabem num commit pequeno cada, o que facilita a aprovação humana exigida pela regra 2 do CLAUDE.md.

Arquivos de referência: `/Users/viniciusdelego/Documents/santainforma/estilo.css` (tokens entram no topo, junto do `:root` existente), `/Users/viniciusdelego/Documents/santainforma/index.html` (carrossel nas linhas 127 a 145, grade na 155), `/Users/viniciusdelego/Documents/santainforma/materia-01-alargamento-meia-praia.html` (hero h1 na linha 119, coluna `.estreito` na 130), URL das fontes na linha 16 de ambos.