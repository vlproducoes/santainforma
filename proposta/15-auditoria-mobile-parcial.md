# Auditoria mobile (PARCIAL) · 24/08/2026

Dois de quatro auditores concluíram antes de o limite de uso ser atingido.
Faltam: navegação/céu/cabeçalho, páginas internas, e a verificação do líder técnico.
Retomar com resumeFromRunId wf_21751d6e-e1a (os concluídos voltam do cache).


# Auditor: capa

## 1. [grave] Topo da capa: header + .editorias.fixa + .horizonte (index.html; estilo.css blocos HEADER e CAPA v2)

**Problema.** O leitor abre o site e a primeira notícia fica na dobra. Em 360px o título da manchete só começa em y=457 (em 390: y=434): são 245px de cabeçalho + 52px da barra de editorias + 48px de ondas = 345px de moldura antes de qualquer conteúdo. Num Android intermediário (360×640, ~560px úteis com a UI do navegador) a primeira tela é logo, 'Itapema, Santa Catarina', data, dois menus e ondas; a manchete aparece cortada. O bloco .meta (68px) ainda repete a localização que a tagline do logo já diz ('Litoral de Santa Catarina').

**Evidência.** Medidas getBoundingClientRect em Chrome emulando 360 e 390: header 245/223px, .editorias 52px, .horizonte 48px, .meta 68px, topo do h2 da manchete em 457/434px; captura m390-0.png (primeira dobra só com moldura).

**Correção.** No @media(max-width:720px) (estilo.css, bloco CAPA v2): header{padding-top:14px} .meta{display:none} nav{margin-top:10px} nav ul{padding:8px 0} .editorias ul{padding:8px 0} — poupa ~100px e a manchete sobe para ~y345, inteira na primeira dobra. Vale para o site todo (todas as páginas usam o mesmo header). Alvos de toque não mudam (o link já tem 28px próprios).

## 2. [grave] Seção 'Itapema e Costa Esmeralda', .linha-1 (líder + pilha), logo depois do rio (index.html)

**Problema.** No celular tudo vira uma coluna, e as 4 chamadas da primeira linha da seção são exatamente as mesmas 4 matérias que o leitor acabou de ler no rio de Últimas, uma tela acima: m77 vira o líder com foto grande, m74, m72 e m70 formam a pilha. 4 de 4 repetidas em sequência de rolagem: a sensação é 'já li isso' e a página parece não avançar. No desktop o rio é coluna lateral e a repetição dilui; no celular ela é literal e consecutiva.

**Evidência.** Comparação de hrefs via JS: os 4 links de .linha-1 (materia-77, 74, 72, 70) estão todos entre os 8 do .rio (duplicados=4/4); capturas m390-1.png e m390-3.png mostram a sequência.

**Correção.** Regra de curadoria no ferramentas/prompt-agente-noticias.md: a linha-1 da seção não usa matéria que já está no rio (pega as próximas mais recentes da região). Paliativo imediato em CSS/HTML enquanto o ciclo não muda: marcar as repetidas com class="ja-no-rio" e @media(max-width:980px){.pilha article.ja-no-rio{display:none}} (o líder, por ter foto e resumo, pode ficar como aprofundamento).

## 3. [medio] Formato lista do celular: .subs (thumb 94px) e .linha-2 article.card.v2 (estilo.css @media max-width:720px)

**Problema.** O título mantém o corpo de card (--t-card ≈17px) mas a coluna de texto encolhe para 194-217px ao lado da thumb de 94px: o título da matéria 21 rende 6 linhas em 360 (bloco de 132px de altura), os subs rendem 5 linhas (99px). Vira parede de negrito com um vazio grande à direita, abaixo da thumb; ruim de escanear rolando.

**Evidência.** Medidas JS a 360: alturas dos links de título 99/99/132px (≈5-6 linhas de 20px); captura m360-linha2.png mostra o card do turista com 6 linhas de título.

**Correção.** Dentro do @media(max-width:720px) já existente: .subs:has(.capa-sub) .sub h3,.linha-2 article.card.v2 h3{font-size:var(--t-rio);line-height:1.25} — usa token existente (≈15px, o mesmo dos títulos do rio, que leem bem), cai para 3-4 linhas. Nenhum hex ou tamanho novo.

## 4. [medio] Costuras entre seções: fim da .linha-2 → #semanal, e Ferramentas → .institucional (estilo.css: main.com-capa>.wrap padding-bottom:52px + .escuro margin:52px; section com padding-bottom:56px inline + .institucional margin-top)

**Problema.** Buraco de 140px de fundo vazio entre o último card e o bloco escuro do Resumo Semanal (mais de 1/5 da tela de um 360×640: parece fim de página no meio da rolagem). Outro respiro de 88px entre o último card de Ferramentas e a faixa Manifesto. São os espaçamentos de desktop somados em dobro (padding da seção + margin do bloco), sem versão de celular.

**Evidência.** Medida JS: gap_linha2_semanal=140px tanto em 390 quanto em 360; gap_dados_institucional=88px; visível nas capturas m390-4.png e m360-linha2.png (faixa clara vazia antes do bloco escuro).

**Correção.** @media(max-width:720px){main.com-capa>.wrap{padding-bottom:24px}.escuro.anoitecer{margin:32px 0}.institucional{margin-top:2rem}} — o buraco de 140px cai para ~70px, mantendo respiro. Escopado em .escuro.anoitecer para não mexer nos blocos escuros das outras páginas.

## 5. [medio] Anúncio .a-super abaixo da capa (index.html linha 214-219; estilo.css bloco ESPACO PUBLICITARIO)

**Problema.** No celular a caixa mede de verdade 320×100 (correto), mas o rótulo central segue dizendo '970 × 250 px', porque o .onde que explicava a troca ('No celular, 320 × 100 px') é escondido no mobile. O anunciante que olha a capa pelo celular lê uma medida que não é a do espaço que está vendo. Detalhe: em 320px de viewport o conteúdo ainda estoura 5px e é cortado pelo overflow:hidden.

**Evidência.** JS: caixa 320×100 em 390; em 320 de viewport a caixa fica 272×85 com scrollHeight 5px maior que o clientHeight; captura m390-2.png mostra a caixa pequena rotulada '970 × 250 px'.

**Correção.** No index.html: <b class="medida"><span class="md-desk">970 &times; 250 px</span><span class="md-cel">320 &times; 100 px</span></b>; no estilo.css: .medida .md-cel{display:none} e, dentro do @media(max-width:760px) existente, .medida .md-desk{display:none}.medida .md-cel{display:inline}. Para o corte em 320: no mesmo media query, .anuncio{padding:6px}.

## 6. [leve] .onda-pausa na faixa .horizonte (estilo.css linhas 594-600)

**Problema.** O botão 'Pausar ondas' vive com opacity:0 e pointer-events:none e só volta com :hover ou :focus-within. Celular não tem hover nem Tab: no aparelho da maioria dos leitores o único jeito de parar a animação infinita (exigência 2.2.2 da regra da casa) simplesmente não existe. Reduced-motion cobre quem configurou o aparelho, mas não quem só quer pausar.

**Evidência.** Regras no estilo.css (opacity:0;pointer-events:none; reaparece só em .horizonte:hover/:focus-within); em emulação touch o botão nunca fica visível nem tocável.

**Correção.** @media(hover:none){.onda-pausa{opacity:.7;pointer-events:auto}} — em tela de toque o botão fica sempre visível, discreto no canto da faixa; no desktop segue escondido como o editor pediu.

### Em ordem
Muita coisa da capa funciona bem no celular, confirmado em 390, 360 e 320: não há estouro horizontal em nenhuma das três larguras (scrollWidth = viewport, medido); o rio de Últimas com thumb de 76px à direita é o melhor trecho da página (título com 252px em 390 / 222px em 360, 2-3 linhas, horário em cima, item inteiro tocável com ~110px de altura, overlay ancorado no li); a manchete domina a abertura quando enfim aparece (26px bold + foto 3:2 + linha fina, contra 15px do rio); os alvos de toque passam da régua de 24px (nav 28px, editorias 25px, rodapé 29px, cards com overlay no article inteiro); o Resumo Semanal em coluna única lê muito bem (numeral 2rem, thumb 60px e texto centrados na mesma linha); as Ferramentas empilhadas e o rodapé estão limpos; o retângulo 300×250 do bloco escuro rende no tamanho certo e centrado; e o reduced-motion está coberto de verdade (estado invisível no from dos keyframes, kill switch repõe opacidade, inclusive nos pseudo-elementos do tempo). Atenção ao medir: headless Chrome com --window-size=390 aplica largura mínima de ~500px e gera capturas falsas de estouro; a auditoria usou iframe de 390/360px reais e emulação de dispositivo no Chrome para as medidas.


# Auditor: materia

## 1. [grave] Hero escuro da matéria (header + .hero com o painel Em 30 segundos), materia-74 e materia-01; estilo.css linhas 62-96

**Problema.** No celular o leitor atravessa quase duas telas de bloco escuro antes de chegar à matéria. Medido na materia-74 em 390px: header 294px + hero 1249px; a foto de topo só aparece a 1803px (2,1 telas de 844px) e o 'Entenda o assunto' a 2125px. Em 320px a foto cai para 2081px. Contribuem: título SEO de 96 caracteres em 32px/1.04 (5 linhas em 390, 7 em 320), painel de 30s com padding 24/26 + min-height, e o .meta do header repetindo 'ITAPEMA · INFRAESTRUTURA' que o chapéu mostra de novo 250px abaixo.

**Evidência.** Medidas via CDP com emulação mobile (390/360/320): hero.h=1249/1337/1509, foto.top=1803/1891/2081; captura full-page m74.png confirma a parede escura de ~1550px antes do branco. (Atenção: headless Chrome sem CDP trava a janela em 500px de largura mínima, screenshot direto em --window-size=390 mente.)

**Correção.** Compactar só no celular, dentro do @media(max-width:600px) existente (estilo.css linha 491): `.meta{display:none} .hero{padding:30px 0 46px} .modo{margin-top:26px;padding-top:16px} .painel{padding:18px 16px}`. Ganho de ~150px sem mexer no desktop. Opcional: `.hero h1{font-size:1.85rem}` no mesmo bloco tira mais ~35px do título longo.

## 2. [medio] Seção 'Leia também' (.grade com article.card) no fim das matérias; estilo.css linhas 224-231 e 382

**Problema.** Em 390px cada card vira um bloco de 476px (capa 16:9 de 342x191 + texto), e os três somam 1430px de rolagem, mais que a própria seção 'Entenda o assunto'. A capa da matéria já resolveu esse problema na mesma largura: em <=720px os cards v2 viram lista com thumb quadrada de 94px. Na matéria o padrão antigo ficou, e o leitor rola 1,7 tela de cards entre as fontes e o rodapé.

**Evidência.** Medido via CDP em 390px: .grade h=1430px, card1 h=476px, imagem h=191px; recortes c-cards.png e c-card3-ret.png; compare com .linha-2 em estilo.css linhas 807-812 (formato lista de 94px do index).

**Correção.** No @media(max-width:600px): `.texto .grade{border:0} .texto .grade article.card{border:0;border-bottom:1px solid var(--fio-cor);background:transparent;padding:14px 0} .texto .grade article.card:has(.capa){display:grid;grid-template-columns:1fr 94px;gap:2px 16px} .texto .grade article.card .capa{grid-column:2;grid-row:1/5;width:94px;height:94px;aspect-ratio:1;margin:0} .texto .grade article.card h3{font-size:1.02rem} .texto .grade article.card p{font-size:.9rem}`. O overlay de clique continua ancorado no article.card (position:relative já existe, nenhum ancestral posicionado novo).

## 3. [medio] Link 'Ver tabela de preços' nos dois blocos .anuncio de toda matéria (.a-faixa e .a-ret); estilo.css linha 147

**Problema.** O alvo de toque do link mede 116x14px, bem abaixo do mínimo de 24px da regra da casa (ideal 44). Os links da trilha, publicado e fonte ganharam padding vertical exatamente por isso (linha 339), mas o .valor a ficou de fora. São dois alvos por matéria, em todas as matérias.

**Evidência.** Medido via CDP: .anuncio .valor a = {w:116, h:14} em 390, 360 e 320; a regra `.trilha a,.publicado a,.selo a,.fonte a{display:inline-block;padding:6px 0}` não inclui .valor.

**Correção.** Em estilo.css, junto da linha 148: `.anuncio .valor a{display:inline-block;padding:8px 12px;margin:-8px -12px}` (o margin negativo devolve o espaço visual, só a área de toque cresce para ~30px; cabe nos 100px da faixa: conteúdo atual ocupa ~78px).

## 4. [medio] Bloco .anuncio.a-faixa no meio da matéria; estilo.css linhas 152, 177-179 e HTML das matérias (materia-74 linhas 195-200)

**Problema.** No celular a caixa é servida em 320x100px, mas o rótulo grande diz '728 × 90 px'. A linha que explicava ('No celular, 320 × 100 px') está com display:none no formato faixa em qualquer largura. Anunciante local lendo no celular, que é o cenário mais comum, vê o tamanho errado do espaço que compraria.

**Evidência.** Recorte c-fonte-faixa.png mostra a caixa de 320px anunciando '728 × 90 px'; medido .a-faixa w=320 h=100 em 390px; `.a-faixa .onde{display:none}` na linha 178.

**Correção.** No template e nas matérias: `<b class="medida"><span class="so-largo">728 &times; 90 px</span><span class="so-cel">320 &times; 100 px</span></b>`; em estilo.css: `.medida .so-cel{display:none}` e no @media(max-width:760px) existente (linha 189): `.a-faixa .medida .so-largo,.a-super .medida .so-largo,.a-bill .medida .so-largo{display:none} .a-faixa .medida .so-cel,.a-super .medida .so-cel,.a-bill .medida .so-cel{display:inline}`.

## 5. [leve] Logo SVG do cabeçalho (width=298 fixo) em telas de 320px; todas as páginas

**Problema.** Em viewport de 320px o SVG do logo (298px + 24px de padding esquerdo = borda direita em 322px) estoura 2px e cria rolagem horizontal na página inteira: documentElement.scrollWidth = 322. É um balanço lateral sutil ao arrastar, típico de Android de entrada.

**Evidência.** Medido via CDP em 320px: vw=320, scrollWidth=322; em 360/390 scrollWidth = viewport. O elemento largo é o svg do .topo (a regra img{max-width:100%} da linha 53 não alcança svg).

**Correção.** Em estilo.css, junto da linha 453: `.topo>a svg{max-width:100%;height:auto}`.

## 6. [leve] Bloco 'Fontes' no rodapé da matéria (.fonte); estilo.css linha 232

**Problema.** O bloco de fontes, que é o selo de credibilidade do portal, rende 4+ linhas de caixa alta em 11.5px com tracking largo (87px de altura na materia-74, mais na 01 que lista 6 fontes). Caixa alta corrida nesse corpo é o texto mais difícil de ler da página no celular, justamente onde o leitor confere de onde saiu o dado.

**Evidência.** Recorte c-fonte-faixa.png; medido via CDP: .fonte font-size 11.5px, h=87px em 390px, text-transform uppercase com letter-spacing .06em.

**Correção.** No @media(max-width:600px): `.texto .fonte{font-size:12.5px;letter-spacing:.04em}`. Se o editor aceitar mexer na identidade: manter em caixa alta só o rótulo 'Fontes:' e deixar a descrição em caixa normal (`.texto .fonte{text-transform:none} .texto .fonte strong{text-transform:uppercase}`).

### Em ordem
Muita coisa está bem no celular: sem estouro horizontal em 390 e 360 (o de 320 é só o logo, achado 5); corpo em 17px/1.62 com ~42 caracteres por linha, medida confortável; breadcrumb e barra publicada-em quebram limpo em 2-3 linhas com alvos de toque de 30px (o padding da linha 339 do estilo.css funciona); foto de topo full-bleed na coluna com legenda de 14.7px e crédito legíveis; box destaque e 'Os números que importam' leem muito bem; o painel de 30 segundos é legível (16.96px, bom contraste sobre o breu) e as três leituras Clara/Prudêncio/Caco ficam confortáveis nas caixas brancas; os anúncios ficam centrados e dentro da coluna (320x100 e 300x250) e a reserva de espaço do .pub-google segura o CLS em zero como prometido (o vão em branco sem rótulo enquanto o AdSense não serve é decisão registrada no CSS); as duas barras de navegação roláveis cortam o texto na borda, o que até serve de indício de rolagem; prefers-reduced-motion está coberto. Nota de escopo: os heros dessas matérias NÃO têm chips do Modo de Leitura, o painel é estático e as outras versões vivem no fim do texto, então não há alvo de toque para errar ali. Nota de método: headless Chrome trava a janela em 500px de largura mínima, então screenshot com --window-size=390 sai com layout de 500px cortado, parecendo estouro que não existe; auditei com emulação de dispositivo via CDP (scripts shot.mjs e med.mjs no scratchpad, capturas m74.png e m01.png).


# Auditor: cromo

### Em ordem



# Auditor: internas

### Em ordem

