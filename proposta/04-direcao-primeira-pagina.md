## nome
Primeira Página

## conceito
O Santa Informa vira o jornal mais bonito do Brasil pelo caminho que NYT, Zeit Online e Le Monde provaram: tipografia impecável, espaço generoso e hierarquia que orienta o olho sem gritar. A dupla já instalada resolve tudo: a Newsreader assume as manchetes no corte óptico de display (o eixo opsz 6..72 existe exatamente para isso) e a Archivo recua para a voz de serviço, em chapéus, datas, navegação e rótulos. O luxo mora nos detalhes de composição, filetes de jornal impresso, numerais old-style, capitular, margem ativa com metadados, foto tratada com uma única receita. Movimento existe em dose mínima e sempre a serviço da leitura: transição entre páginas e reveals curtos, nada que chame atenção para si. Tudo isso é CSS moderno com fallback dentro do estilo.css único, sem uma dependência nova.

## home
Wrap mantém 1180px. Grid mestre de 12 colunas, gutter 24px, declarado uma vez (.capa{display:grid;grid-template-columns:repeat(12,1fr);gap:24px}).

SEÇÃO 1, CABEÇALHO: estrutura atual intacta (logo SVG, nav principal, barra de editorias). Ajuste fino: animação de entrada do logo passa a rodar só na home (hoje roda em toda página e compete com a manchete).

SEÇÃO 2, CAPA (substitui o carrossel): colunas 1 a 7, chapéu Archivo 600 11px caps tracking .15em precedido de filete 28x3px em --sol; manchete Nível 1 (Newsreader 500, clamp(2.4rem,5.6vw,4.25rem), line-height 1.05, letter-spacing -.01em, max-width 16ch); linha fina Newsreader itálico 400, 1.22rem, cor --suave, max 52ch; linha de meta em Archivo caps 11px com data em old-style. Colunas 8 a 12: foto do destaque em 3:2, tratamento único (ver tipografia_cor), crédito em caps 10px. Sob a manchete, filete 1px --areia e dois sub-destaques lado a lado em Nível 2 reduzido (Newsreader 600, 1.3rem, lh 1.15), cada um com chapéu de editoria. No celular empilha nesta ordem: chapéu, manchete, linha fina, foto, sub-destaques; a manchete textual vira candidata a LCP, que é o melhor cenário possível; a foto leva fetchpriority=high só quando cabe na primeira dobra. O carrossel sai da home: a capa passa a ser decisão editorial de 3 chamadas, o problema WCAG 2.2.2 do autoavanço desaparece junto.

SEÇÃO 3, SUPER BANNER: slot .a-super exatamente onde está, mesma reserva por aspect-ratio.

SEÇÃO 4, ITAPEMA E COSTA ESMERALDA: título de seção com filete duplo de impresso (border-top 2px --breu mais linha 1px --areia com 3px de vão, feita com background linear-gradient). Primeira linha assimétrica: chamada líder com foto 16:9 ocupando 6 colunas; à direita, 6 colunas com pilha de 3 chamadas só texto, título Nível 3 (Newsreader 600 1.22rem lh 1.24), uma frase de linha fina em .96rem --suave, separadas por filete 1px --areia (mesma técnica de borda nos próprios cards que a grade atual já usa). Segunda linha: 3 cards de 4 colunas com foto, herdando article.card atual com a tipografia nova. Datas em old-style.

SEÇÃO 5, RESUMO SEMANAL: bloco escuro --mar mantido. Os números 01 a 07 crescem para Newsreader 500, 2rem, oldstyle-nums, cor --sol, pendurados à esquerda do item; título do item vai a Newsreader 600 1.05rem; filete inferior atual permanece.

SEÇÃO 6, FERRAMENTAS DO LITORAL: cards .d atuais; o rótulo grande (.d i) passa a Newsreader 600 2rem com oldstyle-nums onde for número.

SEÇÃO 7, RODAPÉ: estrutura intacta, títulos de coluna já são caps 11px e ficam.

## materia
O topo escuro dá lugar a campo claro --espuma, como primeira página impressa. Sequência: trilha de migalhas em caps 11px; filete 28x3px --sol; chapéu Archivo 600 caps; título H1 em Nível 1 (Newsreader 500, clamp(2.1rem,4.6vw,3.4rem), lh 1.08, max 20ch); linha fina Newsreader itálico 1.25rem --suave; bloco .publicado atual com datas em old-style.

MEDIDA E MARGEM ATIVA: em viewport >=1120px o miolo vira grid de 3 trilhas, grid-template-columns:200px minmax(0,660px) 1fr, gap 40px. A coluna de 660px dá medida de 66 a 70 caracteres em Newsreader 18px/1.62 (hoje os 712px úteis passam de 74ch, largo demais). O rail esquerdo de 200px é sticky (top 24px) e carrega em Archivo caps 11px: editoria, data de publicação e atualização, tempo de leitura, âncoras para as seções da matéria. Abaixo de 1120px o rail volta para o fluxo, acima do texto, e a coluna central ocupa tudo, idêntico ao .estreito atual.

MODO DE LEITURA: chips atuais migram para o campo claro, borda --areia, selecionado com fundo --breu e texto --espuma (contraste 14:1); painel dos 30 segundos vira caixa branca com filete esquerdo 3px --sol, tipo Newsreader 1.06rem.

CORPO: capitular no primeiro parágrafo de Entenda o assunto via initial-letter:3 dentro de @supports, em Newsreader 500 cor --mar; Firefox mostra letra normal e nada quebra. Figuras na coluna central, legenda no formato atual, crédito em caps 10px. Box O que ainda está em aberto mantém .destaque com filete --sol. Os números que importam: lista sem marcador padrão, cada item com o numeral em Newsreader 600 1.4rem oldstyle-nums cor --mar pendurado à esquerda (padding-left 56px, número em posição absoluta), o que transforma a lista na assinatura visual da casa.

COLUNISTAS: as três caixas .leitura-v continuam brancas, filete esquerdo 3px na cor de cada voz, Clara --sol, Seu Prudêncio --mar, Caco --coral; nome do colunista no .autor atual (Archivo caps). Nenhuma fonte nova por voz: a diferença é só filete e nome.

FONTES E ANÚNCIOS: rodapé de fontes intacto; slots .pub-google e .anuncio permanecem nas posições e reservas atuais.

## tipografia_cor
ESCALA (4 níveis, nada fora dela): N1 manchete, Newsreader 500, clamp(2.4rem,5.6vw,4.25rem), lh 1.05, ls -.01em, opsz automático no corte 72. N2 destaque de seção, Newsreader 600, clamp(1.5rem,2.6vw,2rem), lh 1.14. N3 chamada corrente, Newsreader 600, 1.22rem, lh 1.24 (no Resumo Semanal compacto, Archivo 600 1rem como hoje). N4 micro, Archivo 600, 10 a 12px, caps, tracking .08em a .15em, que é o sistema já existente de chapéu, .ed, .quando e créditos, mantido como está. Corpo segue Newsreader 400 18px/1.62 (17px abaixo de 600px).

CARGA DE FONTE: a URL do Google Fonts ganha itálico e o peso 500 de display: Archivo:wght@400;600;800 (inalterado) e Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400. São 2 arquivos woff2 a mais (aprox. 50KB); mitigação no bloco de riscos.

NUMERAIS: font-variant-numeric:oldstyle-nums proportional-nums em datas, números do Resumo Semanal, capitular de listas e no rail da matéria; font-variant-numeric:lining-nums tabular-nums em table.preco e em qualquer número dentro de .dados. Se o corte Google da Newsreader não expuser onum, a declaração é inerte e os numerais ficam padrão, sem quebra. VERSALETES: nunca sintéticos (font-synthesis-small-caps:none); o efeito de versalete continua sendo o falso já usado no site, Archivo caps com tracking, que é honesto e consistente.

COR: paleta intocada, muda a dosagem. --espuma vira o campo dominante (o topo de matéria deixa de ser escuro); --breu concentra texto, cabeçalho e rodapé; --sol sai de preenchimentos grandes e vira acento fino, filete de 3px, marcador, foco, sublinhado de hover; --coral segue exclusivo de rótulo de editoria; --mar segue link e bloco do Resumo Semanal; --areia é a cor oficial de filete. Nenhum tom novo, nenhum color-mix necessário.

FOTOGRAFIA: uma receita única para toda foto editorial, filter:saturate(.94) contrast(1.03), aplicada por classe .foto-tratada em capas e cards; hover remove o filtro em 250ms (transição já existente). Proporções fixas: 3:2 na capa da home, 16:9 em card e topo de matéria, 1:1 nas miniaturas do semanal. Nada de duotone nem overlay de cor: consistência é o tratamento.

## motion
Princípio: só transform e opacity (regra que o próprio estilo.css já declara), nada acima de 700ms, tudo morto sob prefers-reduced-motion pelo kill switch global já existente.

1. ENTRADA DA CAPA (home, uma vez por carga): coreografia 100% CSS keyframes, sem JS, então funciona sem script e termina sempre no estado visível. Sequência: filete do chapéu desenha (scaleX 0 para 1, 450ms, cubic-bezier(.2,.7,.3,1)); chapéu fade 300ms; manchete sobe 14px com fade, 650ms, delay 120ms; linha fina idem com delay 260ms; foto revela por clip-path inset(0 0 100% 0) para inset(0), 700ms, delay 200ms, com o img interno indo de scale(1.03) a 1. Total percebido abaixo de 1s.

2. NAVEGAÇÃO ENTRE PÁGINAS: cross-document View Transitions, que o site já ativou (@view-transition e nomes em header e footer). Evolução: crossfade do root em 280ms e morph da foto, descrito no hero. Fallback é navegação normal, zero custo.

3. REVEAL AO ROLAR: mantém o IntersectionObserver de visual.js, recalibrado para o tom premium: translateY cai de 16px para 12px, duração 500ms, stagger 60ms com teto de 4 irmãos. As redes de segurança atuais (revelar tudo em 2s, fallback sem IO) ficam.

4. MICROINTERAÇÕES: sublinhado de link já transiciona cor e espessura em 160ms, mantido; fundo de card 200ms, filtro de foto 250ms, mantidos. Nada de parallax, nada de sticky cinético, nada de cursor custom.

5. BARRA DE PROGRESSO: scroll-driven animation já implementada com @supports(animation-timeline), fica exatamente como está.

6. GOVERNANÇA: nenhum listener de scroll novo, nenhuma animação em loop infinito na home (as cenas .anima continuam restritas a figuras de matéria, com botão de pausa já existente).

## hero
O momento assinatura é a abertura da capa e o que acontece quando o leitor sai dela. Ao carregar a home, a página respira uma vez: o filete âmbar de 28x3px acima do chapéu se desenha da esquerda para a direita em 450ms, o chapéu ITAPEMA · OBRAS aparece, e então a manchete em Newsreader de até 4.25rem sobe 14 pixels enquanto ganha opacidade, seguida pela linha fina em itálico 260ms depois. À direita, a foto 3:2 se revela de cima para baixo por clip-path, como uma página sendo desvirada, com um assentamento quase imperceptível de escala (1.03 para 1). Em menos de um segundo a capa está inteira e parada, e nada mais se move até o leitor rolar. Sem JS a coreografia roda igual, porque é só CSS; com reduced motion ela não existe e a capa nasce pronta.

A segunda metade da assinatura é a saída: ao tocar numa chamada, um script de 6 linhas em visual.js aplica view-transition-name:capa-materia na imagem do card no instante do clique, e o topo da matéria carrega a mesma imagem com esse nome. Resultado: a foto do card viaja e cresce até virar a foto de topo da matéria em 320ms, o título faz crossfade, e cabeçalho e rodapé ficam imóveis (os nomes de transição deles já existem no CSS). É o tipo de movimento que o leitor não sabe nomear, só sente que o site é caro. Em Firefox e navegadores antigos a navegação é instantânea e normal, e o prerender por speculationrules, já ativo, garante que a página seguinte esteja quente.

## tecnicas
O QUE NÃO ENTRA, com honestidade: Three.js, React Three Fiber, GSAP, Framer Motion e Lenis são dependências externas, vetadas pela Constituição, e num portal de texto lido em celular intermediário seriam só custo de INP e LCP sem ganho de leitura. WebGL e WebGPU não têm objeto aqui, um shader de fundo seria espetáculo, o oposto desta tese. WebAssembly e Rust fazem sentido em ferramenta de linha de comando (otimização de imagem em ferramentas/), nunca no navegador do leitor. Smooth scroll de biblioteca é substituído por rolagem nativa, que o site já trata (scroll-behavior com exceção para reduced motion).

O QUE ENTRA, tudo vanilla, cada item com fallback: 1) Cross-document View Transitions com morph de imagem por view-transition-name; fallback: navegação comum, já é assim hoje. 2) Scroll-driven animation para a barra de progresso, já em produção com @supports; fallback: barra ausente. 3) IntersectionObserver para reveals, já em produção; fallback: conteúdo visível de imediato. 4) clamp() para tipo fluido; fallback universal, suporte total. 5) font-variant-numeric para old-style e tabular; fallback: numerais padrão, inerte se a fonte não tiver a feature. 6) initial-letter para capitular, dentro de @supports; fallback: letra normal no Firefox. 7) clip-path animado no reveal da foto de capa; fallback: animação não roda e a foto aparece pronta (keyframe CSS termina no estado final). 8) text-wrap:balance e pretty, já em produção. 9) speculationrules com prerender moderado, já em produção, é o que faz a troca de página parecer nativa. 10) Fallback de fonte com métrica ajustada: dois @font-face locais (Newsreader-fb sobre Georgia com size-adjust aprox. 105%, Archivo-fb sobre Arial com size-adjust aprox. 97%, mais ascent-override/descent-override calibrados), inseridos na pilha para zerar o salto de layout na troca de fonte; fallback: comportamento atual do swap.

## riscos
PERFORMANCE: a manchete em Newsreader torna o arquivo da fonte crítico para o LCP; a URL nova adiciona aprox. 50KB em 2 woff2. Mitigar com preload do CSS do Google Fonts, display=swap já presente e os @font-face de fallback com size-adjust, que seguram o CLS da troca perto de zero. Medir antes e depois no PageSpeed com throttling móvel; se o LCP piorar mais de 200ms, cortar o itálico da carga e sintetizar oblíqua só na linha fina. O morph de view transition tira snapshot da página; com iframes de AdSense na tela pode haver flash do slot, testar com anúncio servido e, se piorar, restringir o morph só à imagem (root sem crossfade). A coreografia de capa usa clip-path animado, que é barato mas deve ficar restrito a um elemento por página.

ACESSIBILIDADE: risco de regressão zero por design, o kill switch global de reduced motion já cobre as animações novas por serem CSS. A remoção do carrossel elimina a obrigação da 2.2.2 na home. Pontos de atenção: chips do Modo de Leitura sobre fundo claro precisam de novo par de contraste (fundo --breu, texto --espuma, 14:1); o rail sticky da matéria não pode criar armadilha de foco (é só texto e âncoras, ordem do DOM preservada); capitular via initial-letter mantém o texto íntegro para leitor de tela, ao contrário de truques com span. Conferir contraste do numeral --sol 2rem sobre --mar no semanal (par já usado hoje em texto menor, revalidar na AA para texto grande, que exige 3:1 e passa).

MANUTENÇÃO: a capa estática exige escolha editorial de 3 chamadas a cada ciclo, trabalho que o carrossel escondia; mitigar com bloco HTML comentado e ordem fixa (líder, sub 1, sub 2) que o agente de notícias preenche. A home assimétrica tem mais classes de posição que a grade uniforme atual, orçar aprox. 180 linhas novas em estilo.css, comentadas em português no padrão da casa. O morph de imagem exige que card e topo de matéria usem o mesmo arquivo de imagem ou pelo menos o mesmo enquadramento, vale registrar no CLAUDE.md como convenção. Firefox não tem view transitions nem initial-letter: o site fica correto e mais sóbrio lá, e isso precisa estar dito na proposta para o editor não achar que quebrou.