# Auditoria de celular · consolidação técnica

## 0. Nota de estado (lê isto antes da lista)

O commit `b4d3198` ("Celular: menos moldura, menos repeticao e menos buraco", hoje 14h03) já criou o bloco **CELULAR v2** no fim do `estilo.css` (linhas 947 a 1018) e **já aplicou inteiros os relatórios dos auditores "capa" e "materia"**. Confirmado linha a linha no arquivo real. Os dois auditores mediram o site de antes; "cromo" e "internas" mediram o de agora (cromo cita as linhas 956, 961 e 965, que só existem depois desse commit).

Também confirmei no navegador, com viewport real de 390px (iframe de 390 dentro de janela de 820, porque o headless desta máquina trava a janela em 500px de largura mínima e mente na captura direta): a manchete da capa hoje abre em **y=294**, dentro da primeira dobra.

### Descartados por já estarem no código
| Achado | Onde está resolvido |
|---|---|
| capa#1 moldura do topo (header, .meta, navs) | estilo.css 965-976 |
| capa#3 título de lista em `--t-rio` | 979 |
| capa#4 costuras de 140px/88px | 983-985 |
| capa#5 e materia#4 rótulo "970 × 250" no celular | 1012-1017 + `md-desk`/`md-cel` nos 89 HTML de matéria, index, noticias e anuncie |
| capa#6 botão de pausa no toque | 961-963 (mas ver P5, há conflito) |
| materia#1 hero de 2,1 telas | 988-991 (`.hero`, `.modo`, `.painel`) mais `.meta{display:none}` a 720 |
| materia#2 "Leia também" em lista | 997-1003 |
| materia#3 alvo de toque de "Ver tabela de preços" | 1008 |
| materia#5 logo estourando em 320 | 956 |
| materia#6 `.fonte` em 12,5px | 1006 |

### Descartados por não procederem mais
- **capa#2 (repetição rio × linha-1):** não procede. Hoje o rio traz 81 a 89 e a linha-1 traz 21, 29, 31, 72, 74, 77 e 79. Zero repetido. **Sobra um resíduo real:** os três sub-destaques são 69, 86 e 87, e **86 e 87 estão no rio**, duas telas acima no celular. Vira P12, curadoria, não CSS. Nada de classe `ja-no-rio`, gambiarra de marcação para problema de pauta.
- **materia#1 opcional (`.hero h1{font-size:1.85rem}`):** não aplicar agora. O `clamp` já entrega 32px a 390 e o hero encolheu 150px. Encolher a manchete da matéria é decisão de identidade, não de celular.

---

## 1. Lista final de patches

Tudo abaixo é **layout**, então pela seção 2 do CLAUDE.md vai em branch e espera o editor. Ao fim, `python3 ferramentas/checa-site.py` tem que sair 0.

Todo o CSS entra num bloco novo **no fim do `estilo.css`**, depois do CELULAR v2. A posição importa em dois pontos: a tabela precisa vencer o bloco `@media(max-width:760px)` da linha 189, e o horizonte precisa vencer o TEMPO v1 da linha 902.

```css
/* ============================================================
   CELULAR v3 · 24/08/2026 · segunda leva da auditoria
   A primeira leva (CELULAR v2) tratou a capa e a materia. Esta
   trata a NAVEGACAO e as paginas internas, que ficaram para tras.
   Aditivo: nenhum seletor de mesa muda, nenhum hex novo.
   ============================================================ */
```

---

### P1 · GRAVE · As duas barras roláveis escondem metade do site
Junta cromo#1, cromo#2, cromo#5 e internas#6, que são o mesmo problema visto de três ângulos.

**Procede.** Medido: `nav ul` tem 647px de itens numa janela de 342 (390) e de 312 (360); `.editorias ul` tem 799px. O corte é seco, no meio da palavra, e ainda para 24px antes da borda, então lê como defeito e não como "arrasta". Em editoria e matéria o item `.ativo` pode estar a 700px de distância e a barra abre em `scrollLeft 0`: a marcação de "você está aqui" existe no CSS (linha 276) e nunca chega ao olho. E o alvo de toque é 25,4px de altura dentro de uma linha de 44,8px.

**Verificado em tela:** com o patch, "HORÓSCOPO & TARÔ" e "INFRAESTRUTURA" dissolvem no céu do cabeçalho em vez de serem decepados. Fica óbvio que continua.

Apagar as linhas **973 e 974** (`nav ul{padding:8px 0}` e `.editorias ul{padding:8px 0}`), que esta regra substitui, e acrescentar:

```css
/* P1 · as duas barras roláveis: a faixa encosta na borda da tela, o
   ultimo item esmaece em vez de ser cortado, e o alvo cresce para o
   dedo sem mexer no desenho. A camada de clique ancora no LI. */
@media(max-width:720px){
  header nav ul,.editorias ul{
    padding:8px 24px;margin-inline:-24px;
    scroll-padding-inline:24px;scroll-snap-type:x proximity;scrollbar-width:none;
    -webkit-mask-image:linear-gradient(90deg,#000 0 calc(100% - 44px),transparent);
            mask-image:linear-gradient(90deg,#000 0 calc(100% - 44px),transparent)}
  header nav ul::-webkit-scrollbar,.editorias ul::-webkit-scrollbar{width:0;height:0}
  header nav li,.editorias li{scroll-snap-align:start;position:relative;display:flex;align-items:center}
  header nav a::after,.editorias a::after{content:"";position:absolute;inset:-10px -7px}
}
```

Editoria vai de 25,4 para 45,4px de alvo, nav principal de 28,1 para 48,1px, e sobram 8px e 10px entre alvos vizinhos, sem toque ambíguo. `342 + 24 + 24 = 390`, então não nasce rolagem horizontal. O `mask` só apaga pixel, não usa cor, então vale para qualquer céu do cabeçalho e para qualquer clima do TEMPO v1.

E no **`visual.js`**, uma rotina para o item da página atual nascer visível:

```js
/* NAVEGACAO ROLAVEL: a barra abre em zero, entao quem entra em Meio
   Ambiente ve so as tres primeiras editorias e nenhum destaque. Rola
   so a barra, nunca a pagina, e sem movimento: nada de CLS. */
document.addEventListener('DOMContentLoaded', function () {
  function centraliza(caixa, alvo) {
    if (!caixa || !alvo || caixa.scrollWidth <= caixa.clientWidth) return;
    var a = alvo.getBoundingClientRect(), c = caixa.getBoundingClientRect();
    var antes = caixa.style.scrollBehavior;
    caixa.style.scrollBehavior = 'auto';        /* o html tem scroll-behavior:smooth */
    caixa.scrollLeft += (a.left - c.left) - (caixa.clientWidth - a.width) / 2;
    caixa.style.scrollBehavior = antes;
  }
  var barras = document.querySelectorAll('nav ul');
  for (var i = 0; i < barras.length; i++) centraliza(barras[i], barras[i].querySelector('a.ativo'));
  var nums = document.querySelector('.paginacao .numeros');
  centraliza(nums, nums && nums.querySelector('[aria-current]'));   /* ver P6 */
});
```

Correção importante em cima do que o cromo propôs: ele usava `atual.offsetLeft`, que **quebra junto com este mesmo patch**, porque o `li` passa a ser `position:relative` e vira o `offsetParent` do link, zerando a conta. Por isso a versão acima usa `getBoundingClientRect`. Também troquei `scrollIntoView` por `scrollLeft` na paginação: `scrollIntoView` arrastaria a página inteira para o rodapé do arquivo no carregamento.

---

### P2 · GRAVE · O arquivo e as editorias ficaram com o cartão gigante
internas#1. **Procede.** `editoria-economia.html` mede 12.369px para 22 títulos, quase 16 telas. `noticias.html` gasta 4.692px para 6 títulos. Todas as outras listas do site já viram lista compacta com miniatura de 94px no celular (rio, `.linha-2`, `.subs`, e o "Leia também" desde ontem). O arquivo, que é justamente a página de escanear, ficou de fora.

**Verificado em tela:** no mesmo trecho de 1.000px onde hoje cabem 2 chamadas, passam a caber 5, no mesmo idioma visual do resto do site.

O patch é uma linha de tesoura, não código novo: nas **linhas 997 a 1002**, trocar `.grade.leia-tambem` por `.grade`. A classe `leia-tambem` deixa de ser necessária no CSS (pode ficar no HTML das matérias, é inofensiva).

```css
@media(max-width:600px){
  .grade{border:0;grid-template-columns:1fr}
  .grade article.card{border:0;border-bottom:1px solid var(--fio-cor);background:transparent;padding:14px 0;display:grid;grid-template-columns:1fr 94px;gap:2px 16px}
  .grade article.card:last-child{border-bottom:0}
  .grade article.card .capa{grid-column:2;grid-row:1/5;width:94px;height:94px;max-width:none;aspect-ratio:1;margin:0;align-self:start}
  .grade article.card h3{font-size:var(--t-rio);line-height:1.25}
  .grade article.card p{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
}
```
O overlay de clique continua ancorado no `article.card`, que já é `position:relative` desde a linha 391. Nenhum ancestral posicionado novo.

---

### P3 · GRAVE · A tabela de preços não mostra preço nenhum
internas#2. **Procede, e é o pior achado comercial.** `table.preco` tem `min-width:560px` (linha 112) e a primeira tabela mede 690px dentro de uma caixa de 342: 49% visível, as colunas Mensal e Diário inteiramente fora da tela. Nada avisa que rola de lado. O anunciante local abre a página de preços no celular e vê uma grade sem preço.

**Bug encontrado na verificação, que a proposta original do auditor não previa:** a linha 199 do estilo.css (`table.preco tbody tr:nth-child(even) th{background:var(--espuma)}`, especificidade 0,2,4) vence a regra nova (0,1,3) e, como a ficha pinta o `th` de branco sobre `--mar`, o nome de metade dos espaços saía **branco no branco**. Confirmado na captura e corrigido abaixo com o seletor duplo.

```css
/* P3 · a tabela de precos vira ficha no celular: 6 colunas em 342px
   escondiam justamente o preco. Rotulo de coluna vira etiqueta. */
@media(max-width:720px){
  .tabela-rolagem{overflow:visible;border:0}
  table.preco{min-width:0;display:block}
  table.preco thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
  table.preco tbody,table.preco tr,table.preco th,table.preco td{display:block;width:auto}
  table.preco tbody tr{border:1px solid #9F8A6A;background:var(--superficie);margin-bottom:14px}
  table.preco tbody tr:nth-child(even){background:var(--superficie)}
  /* o seletor duplo e obrigatorio: a linha 199 pinta o th par de
     --espuma e o nome do espaco sumia, branco no branco. */
  table.preco tbody th,table.preco tbody tr:nth-child(even) th{
    position:static;background:var(--mar);color:var(--espuma);box-shadow:none;
    white-space:normal;padding:10px 13px}
  table.preco td{border-bottom:var(--fio) solid var(--fio-cor);padding:9px 13px;text-align:left}
  table.preco tbody tr td:last-child{border-bottom:0}
  table.preco td::before{content:attr(data-rot);display:block;font-family:var(--display);font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--suave);margin-bottom:3px}
  table.preco td.n{text-align:left}
}
```

No **`anuncie.html`**, cada `<td>` das quatro tabelas ganha o rótulo da coluna. Exemplo da linha 133:

```html
<tr><th scope="row">Super Banner</th><td data-rot="Desktop"><b>970 &times; 250</b></td><td data-rot="Celular">320 &times; 100</td><td data-rot="Onde aparece">Topo da página inicial, antes da manchete do dia</td><td class="n" data-rot="Mensal">R$ 3.750,00</td><td class="n" data-rot="Diário">R$ 125,00</td></tr>
```
Rótulos das outras três tabelas: `O que inclui` e `Mensal` ou `Valor`. O `<caption class="so-leitor">` continua nomeando a região para leitor de tela, e o `tabindex="0"` do `.tabela-rolagem` pode ficar, é inofensivo sem rolagem. O `#9F8A6A` já é usado no arquivo, não é cor nova.

---

### P4 · GRAVE · O horóscopo não responde ao toque
internas#3. **Procede.** A grade de signos acaba em 1.144px, a `.leitura` começa em 1.170px, mas o primeiro conteúdo dela é a `.carta` decorativa com `min-height:300px` (linha 442), então o título da leitura só nasce em 1.524px e o texto em 1.566px. A página não rola nem move o foco depois do clique. Quem toca em Áries no alto da grade vê, no máximo, a beirada de uma caixa escura vazia, e conclui que o site travou.

**Verificado em tela:** com a inversão, o texto ("Toque no seu signo acima...", e depois a leitura) passa a ser a primeira coisa embaixo da grade.

```css
/* P4 · no celular a leitura vinha depois de 300px de carta decorativa:
   o toque no signo parecia nao ter feito nada. Texto primeiro, carta
   depois. A carta so tem glifo, nome e numero: nada se perde. */
@media(max-width:720px){
  .leitura{display:flex;flex-direction:column;gap:20px}
  .leitura>#leituraSigno{order:1}
  .carta{order:2;min-height:0;padding:20px 16px;gap:8px}
  .carta .glifo{font-size:2.4rem}
}
```

E no fim da função `abrir(i)` do script embutido do **`horoscopo.html`** (o arquivo já carrega a lógica dele ali, então é o lugar certo):

```js
  /* no celular a leitura nasce fora da tela: leva o leitor ate ela,
     senao o toque parece nao ter funcionado */
  if (window.matchMedia('(max-width:720px)').matches) {
    var suave = !window.matchMedia('(prefers-reduced-motion:reduce)').matches;
    document.getElementById('leituraSigno').scrollIntoView({block:'start', behavior: suave ? 'smooth' : 'auto'});
  }
```
O `#leituraSigno` já tem `aria-live="polite"`, então quem usa leitor de tela continua sendo avisado.

---

### P5 · MÉDIO · A faixa do horizonte: 48px de moldura, 4px de céu e um botão de enfeite na melhor tela do site
Aqui **cromo#3 e cromo#4 batem de frente com capa#6, que já está no código**. Decido a favor do cromo, com uma ressalva.

**Os fatos:** `.horizonte` mede `clamp(48px,8vw,84px)`, ou seja, 48px cravados no celular (linha 582), e `.onda-camada` tem `height:44px` fixos (linha 583). Sobram 4px de céu. Todo o TEMPO v1, que o editor acabou de aprovar, nasce fora da caixa: os fios de chuva aparecem numa tira de uns 8px e as nuvens (`at 26% -45%`) e a névoa (`at 33% 112%`) ficam fora da faixa. Ou seja, no aparelho da maioria dos leitores o recurso do céu que sente o clima quase não se vê, e mesmo assim quatro camadas ficam animando. Em cima disso, a regra `@media(hover:none)` da linha 961 (aplicada ontem, e correta na intenção) põe uma pílula de 116x27px com texto de 10px, o menor tipo do site, pousada logo acima da manchete.

**A decisão:** no celular a faixa para de andar e o botão sai junto. Sem movimento, a exigência 2.2.2 não se aplica e não é preciso mecanismo nenhum. O clima continua sendo dito pelo véu de chumbo, que o próprio cromo confirmou que lê bem a 390, e pela textura parada de chuva, que agora tem céu onde aparecer. A deriva é de 26 a 34 segundos numa faixa de 48px: ninguém percebe que ela existe, mas a bateria do Android intermediário percebe. A regra `@media(hover:none)` fica onde está, e passa a valer só para aparelho de toque acima de 720px, onde a faixa cresce e o movimento se lê.

```css
/* P5 · a faixa tem 48px: 44 de onda deixavam 4px de ceu e a chuva e as
   nuvens do TEMPO v1 nasciam fora da tela. E a 48px a deriva nao se le,
   entao ela para e o botao que a 2.2.2 exigiria devolve o lugar para a
   manchete. Onda parada, nada a pausar. */
@media(max-width:720px){
  .onda-camada{height:62%}
  .onda-camada,.horizonte::before,.horizonte::after{animation:none}
  .onda-pausa{display:none}
}
```
62% de 48px dá 29,8px de onda e 18,2px de céu, quatro vezes o de hoje, sem mudar a altura da faixa (CLS zero). O SVG usa `preserveAspectRatio="none"`, então achata sem deformar o traço. `.horizonte` só existe no `index.html`, então o patch não alcança nenhuma outra página. **Verificado em tela:** o céu aparece de verdade acima da onda.

Se o editor não quiser a onda parada, a alternativa é manter o movimento e encolher o botão para ícone, mas aí ele continua sendo um alvo de 44px em cima de uma faixa de 48. Eu recomendo a onda parada.

---

### P6 · MÉDIO · Paginação de 15 caixinhas
internas#4. **Procede.** 15 itens quebram em três fileiras (7, 7 e 1), o número 15 fica órfão sozinho, o bloco come 173px logo depois da última matéria, e cada caixa tem 36x36px (linha 331), abaixo dos 44 confortáveis.

```css
/* P6 · 15 caixinhas em tres fileiras viravam paredao de numero. Uma
   fileira que rola, com alvo de 44px. O JS do P1 ja centraliza a atual. */
@media(max-width:600px){
  .paginacao{gap:14px}
  .paginacao .numeros{width:100%;flex-wrap:nowrap;justify-content:flex-start;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x proximity;scroll-padding-inline:24px;scrollbar-width:none;
    -webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 26px),transparent);
            mask-image:linear-gradient(90deg,#000 calc(100% - 26px),transparent)}
  .paginacao .numeros::-webkit-scrollbar{display:none}
  .paginacao .numeros a,.paginacao .numeros span{flex:none;min-width:44px;height:44px;scroll-snap-align:center}
}
```

---

### P7 · MÉDIO · A barra de editorias gruda na capa e não gruda no resto (adiado, com motivo)
cromo#6. **Procede de fato:** só o `index.html` tem `class="editorias fixa"`; em matéria e editoria a mesma barra vive **dentro** do `<header>` (matéria linha 108, header fecha na 112), e `position:sticky` dentro do header só gruda enquanto o header está na tela. O leitor aprende um comportamento na capa e perde ele na matéria.

**Decisão: não entra nesta leva.** Não é ajuste de celular, é mudança de gabarito: tirar a `<nav>` de dentro do `<header>` em 89 matérias mais 6 editorias, mexer no modelo canônico (`materia-01`) e no `ferramentas/prompt-agente-noticias.md`. Isso é uma aprovação própria do editor e um script próprio, com risco próprio, e misturar com sete patches de CSS é pedir para o `checa-site.py` reprovar sem se saber por quê. Fica proposto para a leva seguinte. A regra `body:has(.editorias.fixa) [id]{scroll-margin-top:52px}` (linha 698) já cobre as âncoras dessas páginas no dia em que a classe existir.

---

### P8 · LEVE · Raio-X com 16 cartões de dado empilhados
internas#5. **Procede, com gravidade menor que a relatada** (o cartão tem 214px, então cabem uns três por tela, não um). O ganho real não é rolagem, é comparação: os quatro valores de metro quadrado da Camada 3 são feitos para ficar lado a lado.

**Escopo corrigido:** o auditor propôs mexer em `.dados` inteiro, o que arrastaria junto o bloco Ferramentas da capa, que o auditor da capa aprovou empilhado. Escopei com `:not(.dados-capa)`. **Verificado em tela:** duas colunas em 390 sem estouro, "81,1 anos" inteiro, fonte da linha de crédito legível.

```css
/* P8 · fora da capa, o cartao de dado cabe em duas colunas: os quatro
   metros quadrados da Camada 3 voltam a poder ser comparados de relance. */
@media(max-width:600px){
  .dados:not(.dados-capa){grid-template-columns:1fr 1fr;gap:10px}
  .dados:not(.dados-capa) .d{padding:16px 14px}
  .dados:not(.dados-capa) .d i{font-size:clamp(1.3rem,6.4vw,1.85rem)}
  .dados:not(.dados-capa) .d .icone{margin-bottom:8px}
}
```

---

### P9 · LEVE · O rótulo "Manifesto" solto no meio da rolagem
cromo#7. **Procede.** `.institucional .wrap` é flex de linha com `gap:2rem` (linha 766); no celular quebra em três linhas mantendo os mesmos 32px, então o rótulo fica tão longe do texto que ele nomeia quanto um parágrafo fica do outro.

```css
/* P9 · sem duas colunas, o flex so afasta o rotulo do texto que ele nomeia */
@media(max-width:720px){
  .institucional .wrap{display:block}
  .institucional b{display:block;margin-bottom:.4rem}
  .institucional p+p{margin-top:.9rem}
}
```

---

### P10 · LEVE · Título com ícone quebrando no ponto do meio
internas#7. **Procede.** `.texto h2` é flex com ícone (linha 411) e herda `text-wrap:balance` da linha 32; em 390 o ícone mais o gap comem uns 40px e o balance parte o que sobra em partes iguais, deixando "Camada 3 ·" sozinho na primeira linha com o ponto pendurado. Especificidade de `.texto h2` (0,1,1) vence a global (0,0,1), então não precisa de `!important`. **Verificado em tela:** "Camada 1 · Santa Catarina" volta a caber numa linha só.

```css
@media(max-width:600px){
  .texto h2{text-wrap:pretty;gap:8px;font-size:1.32rem}
  .texto h2 .icone{margin-top:.3em}
}
```

---

### P11 · LEVE · O recado do 404 em quatro linhas de caixa alta
internas#8. **Procede.** `404.html` linha 113 usa `class="fonte"`, que é o crédito de fonte da matéria (caixa alta, 12,5px, tracking). Numa página cujo único trabalho é reorientar quem se perdeu, é o texto mais difícil de ler. Zero CSS novo, só trocar a classe por uma que já existe e é de leitura:

```html
<p class="leituras-nota" style="margin-top:30px">Achou um link quebrado dentro do nosso site? …</p>
```

---

### P12 · CURADORIA · Os sub-destaques repetem o rio
Resíduo do capa#2. Hoje: rio traz 86 e 87, e os sub-destaques trazem 69, **86 e 87**. No celular os subs vêm em coluna única logo abaixo do rio, então o leitor lê a mesma chamada duas vezes em menos de uma tela de distância. A regra de curadoria escrita no `ferramentas/prompt-agente-noticias.md` no commit de hoje cobriu a `linha-1` da seção, mas não os `.subs`. **Estender a mesma regra aos sub-destaques**, no prompt, e corrigir o `index.html` na próxima rodada do ciclo. Não é CSS, e não vale marcação de conveniência para esconder o sintoma.

---

## 2. Ordem de aplicação sugerida

1. P1 mais a rotina do `visual.js` (é o que devolve metade do site ao leitor de celular).
2. P2 e P3 (arquivo e tabela de preços, as duas páginas que hoje não cumprem a função delas).
3. P4, P5, P6.
4. P8 a P11, que são acabamento e podem ir no mesmo commit.
5. P7 e P12 em leva própria, com aprovação e script próprios.

Tudo conferido com viewport real de 390px. Nenhuma das regras acima toca em largura maior que 720px (P2, P6, P8 e P10 param em 600px), nenhuma cria hex, todas as cores saem das variáveis da casa ou do `#9F8A6A` já existente, o `mask-image` não usa cor, nenhum overlay de clique ganhou ancestral posicionado novo, e nada mexe em altura declarada, então o CLS continua zero. O único ponto que toca movimento é o P5, que só remove animação, então `prefers-reduced-motion` segue coberto pelo kill switch da linha 498 e pela regra explícita de pseudo-elemento da 940.

---

## 3. Diagnóstico em três frases, para o editor

O celular nunca esteve ruim de cor nem de tipo, esteve ruim de proporção e de caminho, e a parte da proporção já foi consertada hoje de manhã: a moldura do topo caiu de 345px para 129px e a manchete voltou para a primeira tela. O que ficou é o caminho: no celular a navegação inteira mora em duas barras que cortam a palavra no meio sem dizer que rolam e nunca mostram em que editoria o leitor está, então Turismo, Meio Ambiente, Santa Catarina e Quem somos praticamente não existem para quem lê pelo telefone. E as páginas que não são a capa ficaram para trás na fila do redesign: o arquivo entrega um cartão gigante por vez (16 telas para 22 títulos), a tabela de preços mostra tudo menos o preço, o horóscopo não dá sinal nenhum quando o leitor toca no signo, e a faixa de ondas ainda cobra 48px da tela mais cara do site para mostrar 4px de céu e um botão de pausar enfeite.