# VEREDITO DO PAINEL · Thumbs no rio de últimas

**1. Recomendação:** **Não.** O rio permanece só texto, no desktop e no celular, por ora.

**2. Por quê:**

- **A quietude é o design** (Direção de Arte). A capa funciona pelo contraste entre uma única massa fotográfica e uma coluna tipográfica. Oito quadradinhos viram oito pontos de fuga disputando com a manchete, e no celular o rio ficaria idêntico aos cards e ao Resumo Semanal, apagando a distinção de "últimas".
- **O acervo não sustenta a thumb** (UX). Miniatura só acelera o clique quando é foto específica do fato. O acervo do portal é majoritariamente ilustrativo (nuvem, dinheiro, prédio), e a 48 ou 60px isso vira textura repetida que lê como template e derruba a credibilidade da coluna. O G1 pode porque tem foto factual em quase tudo; nós ainda não temos.
- **Performance não veta, mas manutenção pesa** (Performance). Os 25 a 50 KB são irrelevantes, porém o template passaria a depender de `mNN-mini.jpg` existir para toda matéria, com validação e fallback no ciclo automático. Custo real para ganho não comprovado.

**3. Divergência e desempate:** Performance disse "sim no mobile", UX disse "talvez no mobile, após teste", Arte disse "não". Desempatei pelo argumento que os outros dois não refutaram: a thumb só paga o custo quando a imagem é factual, e hoje ela quase nunca é. O parecer de Performance provou que dá para fazer sem quebrar nada, não que vale a pena fazer.

**4. Em vez disso:**

- Vida à coluna por via tipográfica: cor coral no horário, peso do filete, teste de espaçamento. Mexer só em `estilo.css`, bloco CAPA v2.
- Minis seguem no Resumo Semanal e nos cards, onde já funcionam.
- **Gatilho de revisão:** quando a maioria das matérias tiver foto factual própria ou de divulgação, reabrir a questão como teste A/B mobile-only, usando a espec já pronta do painel (48x48, à direita do texto, `width`/`height`/`loading="lazy"`, slot fixo, fallback sem slot, desktop intocado).

---

# Pareceres individuais

PARECER · DIREÇÃO DE ARTE EDITORIAL

Posição: **não**. O rio fica só texto.

**1. A capa funciona por contraste, não por soma.** A hierarquia atual tem uma única massa fotográfica (a manchete, 8 colunas) contra uma coluna puramente tipográfica. É esse desequilíbrio deliberado que faz o olho pousar primeiro na manchete. Imagem sempre ganha de texto na disputa por atenção: 8 quadradinhos à direita viram 8 pontos de fuga competindo com a foto principal. O rio deixa de ser rio e vira um tabuleiro. A quietude dele não é ausência de design, é o design.

**2. Thumb a 60px não informa, só decora.** Nesse tamanho, foto de notícia vira confete: não dá para ler o conteúdo da imagem, apenas perceber "tem uma imagem ali". O que comunica urgência no rio é o horário tabular e o ponto coral do cabeçalho, e isso já está lá. Guardian e Zeit mantêm o trilho de últimas só texto exatamente por isso. O G1 usa thumbs porque a home dele é feed rolável sem manchete dominante, um modelo diferente do nosso pacote de capa. Não é referência para esta superfície.

**3. No celular o dano é maior.** O rio empilha logo abaixo da foto da manchete. Com thumbs, ele fica visualmente idêntico aos cards de seção e ao Resumo Semanal (que já usa as minis a 60x60): a distinção entre "últimas" e o resto da home some, e a página vira uma lista uniforme de foto+título do topo ao rodapé. Monotonia é o oposto de hierarquia. De quebra, 8 imagens acima da dobra num site que vive de Discover é risco gratuito de CLS.

Se a intenção é dar mais vida à coluna, o caminho é tipográfico: peso, cor do horário, o filete. As miniaturas já têm casa certa, que é o Resumo Semanal e os cards. A capa não precisa delas.

Arquivos citados: /Users/viniciusdelego/Documents/santainforma/index.html, /Users/viniciusdelego/Documents/santainforma/estilo.css (bloco CAPA v2, `.rio` linhas 607-618).

---

**PARECER · UX de leitura e varredura**

**Posição: não no desktop. No celular, aceitável só com condições estritas, e depois de teste.**

**Argumento 1. A espinha de varredura hoje é ótima, e thumb quebra isso.** O leitor varre lista de últimas pelo padrão F: desce pela borda esquerda fixando as duas ou três primeiras palavras de cada título. O rio atual entrega exatamente essa espinha: horário e título alinhados, fio separando, nada competindo. Miniatura à esquerda desloca o início do texto e insere uma fixação extra por item antes da palavra que decide o clique. Em 8 itens, isso é custo puro.

**Argumento 2. Miniatura só acelera reconhecimento quando é específica.** Eyetracking mostra que imagem genérica em lista é ignorada (o leitor aprende a pular o que não informa). O acervo do portal é majoritariamente ilustrativo: nuvem, dinheiro, prédio. A 60px isso vira textura, e pior, ilustrativa repetida em dois itens visíveis lê como template, derruba a credibilidade da coluna inteira. O G1 usa thumb porque tem foto factual do evento em quase tudo. Guardian e Zeit, com rio texto, provam que recência mais título já carrega o clique.

**Argumento 3. Hierarquia da capa.** O rio é quieto de propósito para a manchete dominar. Thumbs criam 8 mini-cards disputando com a foto principal e reduzem itens visíveis sem rolar.

**Se o editor quiser testar no celular (<980px), exijo:**

- mNN-mini.jpg a 56x56, **à direita** do texto (espinha esquerda intacta, padrão NYT app e BBC)
- `width`, `height` e `loading="lazy"` no HTML (CLS zero, é receita)
- item inteiro clicável, alvo mínimo de 48px
- ilustrativa repetida entre os 8 itens: aquele item volta a texto puro
- desktop permanece texto, sempre

**O que não pode acontecer:** thumb à esquerda, título espremido em duas palavras por linha, layout shift, e thumb virar obrigação quando não existe imagem honesta.

---

PARECER · PERFORMANCE E LAYOUT

**Posição: sim, com condições. E com uma preferência clara: thumb só no mobile, desktop segue texto puro.**

Argumentos decisivos:

1. **Bytes não são argumento contra.** As 8 minis somam 25 a 50 KB (3 a 9 KB cada, já prontas, já usadas no Resumo Semanal). Com `loading="lazy"` elas nem disputam o carregamento crítico. O LCP da home é a foto da manchete e continua sendo. Quem quiser vetar thumbs precisa de outro motivo, performance não é.

2. **O risco real é altura, não peso.** Hoje cada item do rio fecha em ~80px (horário + título em 2 linhas, padding 13px) e a coluna termina alinhada com o bloco da manchete. Thumb à esquerda estreita a caixa do título: título que cabia em 2 linhas vai para 3, cada item cresce ~20px e o rio desce 150px ou mais além da manchete no desktop. É exatamente o desalinhamento que o blueprint quis evitar. No mobile esse problema não existe: o rio já empilha como lista, e ali a thumb ajuda a escanear.

3. **Custo de manutenção do ciclo automático.** O template do rio passa a depender de `mNN-mini.jpg` existir para toda matéria. Mini ausente vira ícone quebrado na capa. O gerador precisa validar o arquivo e ter fallback.

Parâmetros que eu exigiria:

- Exibição em 48x48 (o arquivo 160x160 cobre tela 3x), canto arredondado igual ao dos cards.
- `<img>` com `width`, `height`, `loading="lazy"`, `decoding="async"` e slot de largura fixa no flex. CLS zero por construção.
- Thumb visível só abaixo de 980px; acima disso o CSS mantém o rio como está.
- Fallback no template: sem mini, o item renderiza sem o slot, nunca com imagem quebrada.
- Proibido: preload das minis, imagem acima da dobra além da manchete, slot de altura variável.