## nome
LITORAL VIVO

## conceito
Nenhum portal de notícias do Brasil tem identidade de lugar, e o Santa Informa tem um lugar com identidade sobrando: o mar de Itapema. A direção transforma a praia em sistema de design. O site respira no fuso do leitor: o céu do cabeçalho segue a hora de Brasília, o sol da marca nasce e se põe de verdade, e uma faixa de mar real (WebGL 2 vanilla, shader GLSL escrito à mão) vive entre o cabeçalho e a notícia. Tudo é camada progressiva sobre o HTML estático que já existe: sem JS o site continua inteiro e com a cara de hoje, com JS ele passa a viver. O movimento mora nas bordas (céu, divisórias, micro-respostas) e nunca disputa com a leitura, com o anúncio ou com o LCP.

## hero
O MOMENTO ASSINATURA. O leitor abre a home às 6h40 de Itapema. O cabeçalho está em amanhecer: o gradiente vai de um breu levemente aquecido no topo até coral com sol na base. O sol do logotipo, que hoje já tem a animação "nascer", está baixo, encostado na linha d'água da própria marca. Abaixo da navegação, uma faixa de mar de 160px (96px no celular) ondula em tempo real: superfície com brilho granulado, cristas com espuma, e um reflexo vertical dourado (o "caminho do sol") alinhado horizontalmente com o sol do logotipo. A crista da água do canvas morre exatamente sob a onda divisória SVG, que cobre a borda inferior do canvas: a emenda entre GPU e página é invisível. No desktop, mover o mouse sobre a faixa cria uma ondulação amortecida de no máximo 6px que se desfaz em 2s. À noite (19h às 5h) a água fica quase breu com cintilado em mar-claro, e no logotipo a lua (símbolo #i-lua, que já existe no sprite) assume o lugar do sol. A faixa é decorativa e aria-hidden; o único elemento interativo é o botão "Pausar o mar" no canto, padrão .pausa-anima.

DESENHO TÉCNICO DO SHADER. Geometria: um único triângulo de 3 vértices cobrindo o clip space, sem depth, sem stencil, sem textura. Fragment (~150 linhas comentadas em português): fbm de ruído de valor para o granulado da superfície, linha d'água por soma de 3 senos com fases primas entre si, espuma por smoothstep na crista, reflexo do sol como faixa vertical com decaimento exponencial. Oitavas por #define OCTAVAS na compilação: 3 no celular, 5 no desktop.

Uniforms: u_tempo (float, segundos com módulo 3600 para não degradar a precisão do float), u_res (vec2 do buffer), u_fase (float 0..1, hora do dia normalizada), u_ceu_alto, u_ceu_baixo, u_agua, u_espuma, u_sol (vec3 cada, lidos por getComputedStyle das custom properties na montagem e a cada virada de estado: a paleta continua morando só no estilo.css), u_solx (float, posição do reflexo, casada com o sol do logotipo), u_ponteiro (vec2) e u_forca (float) para a ondulação de resposta, amortecida no JS com lerp de 0.08 por quadro e zerada em tela de toque para nunca brigar com a rolagem.

Custo e orçamento de GPU: 40 a 70 operações ALU por pixel; buffer de 1280×160 com DPR limitado a 1.5 no desktop e 1.0 no celular dá cerca de 460 mil pixels. Alvo: 1,5 ms por quadro a 30fps (4,5% de um quadro de 33 ms), teto duro de 3 ms. Medição por EXT_disjoint_timer_query_webgl2 quando o driver expõe; senão, proxy pelo intervalo entre rAFs. Se 10 quadros seguidos passarem de 12 ms, rebaixa sozinho (30fps vira 15, depois cai para a camada SVG) e não volta no mesmo pageview.

Quando monta: depois do evento load, dentro de requestIdleCallback com timeout de 2500 ms, e só se todas as condições valem: sem prefers-reduced-motion, sem pausa gravada em localStorage (si-mar), faixa dentro do viewport, WebGL2 disponível. Contexto criado com alpha:true, antialias:false, depth:false, stencil:false, powerPreference:'low-power'. O canvas só aparece (fade de 600 ms) depois de compilar e desenhar o primeiro quadro: nunca pisca canvas preto. Quando desmonta ou pausa: IntersectionObserver cancela o rAF com a faixa fora da tela; visibilitychange pausa na aba oculta; webglcontextlost derruba para a camada SVG definitivamente naquele pageview; o botão de pausa congela o quadro atual e grava a escolha.

Camadas de fallback, de baixo para cima: camada 0, sempre no HTML, gradiente CSS mais SVG estático de duas ondas (~2 KB inline), que é o que o leitor sem JS, o Google e quem pediu menos movimento veem; camada 1, as duas ondas ganham loop de translateX (o padrão .corre que o estilo.css já tem), 26s e 34s; camada 2, o canvas WebGL por cima. LCP intocado: a faixa tem altura reservada em CSS (CLS zero), não contém texto nem imagem candidata a LCP, e nada do shader executa antes do load.

## home
Seção por seção, sobre a estrutura atual do index.html:

1. CABEÇALHO-CÉU. O bloco escuro do header vira céu: background linear-gradient(var(--ceu-alto), var(--ceu-baixo)), com valores padrão iguais ao breu de hoje (sem JS, nada muda). Umas 10 linhas no visual.js, penduradas no relógio que já atualiza a cada minuto, calculam a hora em America/Sao_Paulo e escrevem as variáveis no html. O sol do logotipo ganha posição vertical por hora (translateY via custom property no grupo .sun) e a lua assume das 19h às 5h.

2. FAIXA DO MAR. Novo bloco de 160px (desktop) e 96px (celular) entre a navegação de editorias e a onda divisória, aria-hidden, com as três camadas descritas no hero. A onda divisória atual (.onda) passa a cobrir a base do canvas e ganha ondulação própria: dois paths duplicados a 200% de largura em loop de translateX (26s e 34s, só transform, compositor). No celular a faixa de 96px mantém o primeiro slide do carrossel dentro da dobra de 360×640, o que preserva o elemento LCP atual.

3. MANCHETES. O carrossel continua exatamente como é (setas, pontos, pausa, WCAG 2.2.2 já resolvidos). Ajuste único: uma linha d'água de 1px em espuma com brilho sol na base do gradiente de cada slide, e o h3 do slide sobe para clamp(1.35rem, 2.6vw, 1.7rem) para dar mais hierarquia à manchete.

4. SUPER BANNER. Intocado. É receita e já tem altura reservada por aspect-ratio.

5. GRADE ITAPEMA E COSTA ESMERALDA. Mantém a grade com bordas de areia e a "maré de entrada" (o reveal com IntersectionObserver e stagger de 70ms que já existe). Novidade: linha da maré, um traço de 2px em sol sob o título do card que expande por scaleX em 320ms no hover e no focus-visible. Só transform.

6. RESUMO SEMANAL. O bloco escuro fica cravado no estado "anoitecer" da paleta (gradiente fixo de mar para breu), sem seguir a hora: é a âncora de identidade constante da página. Números 01 a 07 seguem em sol. Nada de movimento novo aqui.

7. FERRAMENTAS DO LITORAL. Cards .d atuais, apenas com a linha da maré no hover. Sem animação ambiente: perto do rodapé ninguém precisa de mar.

8. RODAPÉ FUNDO DO MAR. A onda divisória espelhada verticalmente faz a entrada do rodapé, estática. O breu continua. A linha de 1px em areia sobre o legal fecha a metáfora sem custo algum.

Regras transversais: content-visibility:auto com contain-intrinsic-size nas seções abaixo da dobra (Resumo Semanal, Ferramentas, rodapé), zero requests novos, todo o código entra inline nos três arquivos que já existem.

## materia
A matéria é território de leitura e de AdSense, então o orçamento de GPU inteiro fica na home: nenhum canvas aqui.

1. HERO DA MATÉRIA. Herda o céu por hora de graça, porque usa as mesmas custom properties do cabeçalho (custo zero, é o mesmo gradiente). Chapéu, H1, linha fina e Modo de Leitura permanecem na estrutura atual do modelo canônico (materia-01).

2. ONDA DIVISÓRIA. A mesma camada 1 CSS da home (loop translateX), entre o hero escuro e o texto claro. Para com reduced-motion e com o botão global de pausa.

3. BARRA DE PROGRESSO. A .progresso existente (scroll-timeline, já com @supports) vira "linha do sol": gradiente de sol para coral. Uma linha de CSS.

4. FIGURA DE TOPO. Continua sendo o candidato a LCP da página e nada monta, anima ou pinta por cima dela. loading eager como já está no modelo.

5. MODO DE LEITURA. Chips e painel atuais, com o crossfade de 200ms que já existe. Cada colunista ganha assinatura cromática dentro da paleta: Clara com borda sol, Seu Prudêncio com borda mar, Caco com borda coral, tanto no painel quanto nos blocos "Outros jeitos de ler". Pictograma pequeno do sprite ao lado do nome (i-sol para Clara, i-balanca para Prudêncio, i-olho para Caco).

6. TÍTULOS DE SEÇÃO. "Entenda o assunto" e "Os números que importam" ganham a linha da maré estática de 2px em sol sob o título, sem animação: só ritmo visual que amarra com a home.

7. BOX "O QUE AINDA ESTÁ EM ABERTO" (.destaque), números, fontes, Leia também e os dois blocos de anúncio: intocados. Nenhum efeito encosta em área de anúncio, por política do AdSense e por CLS.

## tipografia_cor
TIPOGRAFIA. Archivo 400/600/800 e Newsreader com eixo óptico permanecem, sem nenhum peso novo (cada peso é rede no celular do leitor típico). Evoluções: h3 do slide ativo do carrossel sobe para clamp(1.35rem, 2.6vw, 1.7rem); o H1 da matéria já usa clamp e fica como está; linhas finas seguem em Newsreader com opsz alto, sem adicionar o eixo itálico (custaria bytes por um ganho pequeno).

COR. Nenhum hex novo em nenhum arquivo, regra dura. Os quatro estados do céu são misturas das cores existentes via color-mix() em srgb, sempre com o valor fixo atual declarado antes como fallback:

- Noite (19h às 5h): topo breu puro, base color-mix(in srgb, var(--breu) 85%, var(--mar) 15%). Água quase breu, cintilado em mar-claro, lua no logotipo.
- Amanhecer (5h às 8h): topo color-mix(var(--breu) 70%, var(--mar) 30%), base color-mix(var(--coral) 55%, var(--sol) 45%). Reflexo do sol no shader no máximo.
- Dia (8h às 17h): topo var(--mar), base color-mix(var(--mar) 45%, var(--mar-claro) 55%). Espuma cheia na água.
- Entardecer (17h às 19h): topo color-mix(var(--breu) 75%, var(--coral) 25%), base color-mix(var(--coral) 60%, var(--sol) 40%).

Regra de contraste que governa tudo: o texto do cabeçalho (espuma e mar-claro) apoia sempre no terço superior do gradiente, e o topo nunca clareia além do tom de --mar. Espuma sobre mar rende cerca de 8:1, então o pior caso continua acima de AA com folga; a base, que pode ir a coral com sol, nunca recebe texto, só água e onda. As variáveis de céu são registradas com @property (syntax '<color>') para permitir transição de 1200ms na virada de estado; sem suporte a @property, a troca é seca uma vez por minuto, imperceptível. O Resumo Semanal fica cravado no estado anoitecer como âncora fixa da marca.

## motion
Sistema de movimento em quatro andares, do sempre-presente ao opcional. Regra de física única: só transform, opacity e color; nada de animar layout ou pintura. Curva da casa: cubic-bezier(.2,.7,.3,1), a mesma que o site já usa. Escala de durações: micro-respostas 160 a 320ms, entradas 600ms, ambiente 20 a 34s em loop, mar contínuo a 30fps.

1. SOL DA MARCA. Nasce com o keyframe atual no load; a posição de repouso vem da hora (custom property). Técnica: CSS puro pilotado por variável.
2. CÉU. Transição de cor de 1200ms a cada atualização do relógio (que já roda por minuto). Técnica: @property com transition; fallback troca seca.
3. MAR WEBGL. 30fps com acumulador de tempo, monta em idle pós-load, pausa fora do viewport e em aba oculta, rebaixa sozinho sob pressão, morre em contextlost. Técnica: WebGL2 cru, descrita no hero.
4. ONDA DIVISÓRIA. Loop translateX de 26s e 34s nos dois paths, compositor puro. Técnica: o padrão .corre já existente no estilo.css.
5. MARÉ DE ENTRADA. O reveal atual com IntersectionObserver, stagger de 70ms limitado a 5 irmãos, redes de segurança já escritas no visual.js. Mantido como está.
6. LINHA DA MARÉ. scaleX de 0 a 1 em 320ms no hover e focus-visible de cards e ferramentas. Técnica: pseudo-elemento com transform.
7. TRANSIÇÃO ENTRE PÁGINAS. View Transitions com cabeçalho e rodapé estáveis, já implementada, mantida.
8. PAINEL DO MODO DE LEITURA. Crossfade de 200ms existente, mantido.
9. ONDULAÇÃO DE RESPOSTA. pointermove na faixa do mar, rAF-throttled e passive, amortecimento por lerp 0.08, amplitude máxima 6px, desligada em tela de toque.

Governança: um botão "Pausar o mar" na faixa controla canvas e ondas divisórias de uma vez, grava em localStorage e vale para o site inteiro na sessão seguinte; o carrossel mantém o botão próprio que já tem. prefers-reduced-motion desliga os andares 2, 3, 4, 6 e 9 na raiz (o bloco global de reduced-motion do estilo.css já zera animation e transition, os novos efeitos entram nesse mesmo guarda-chuva) e impede a montagem do canvas antes de qualquer byte de shader compilar.

## tecnicas
Cada técnica com seu fallback:

1. WebGL 2 vanilla (mar do hero). Fallback em cascata: canvas com problema ou ausente cai para SVG animado por CSS; sem JS ou com reduced-motion fica o SVG estático com gradiente, que já está no HTML. Peso: ~6 KB de shader e orquestração dentro do visual.js.
2. CSS custom properties + color-mix() (céu por hora). Fallback: valor fixo atual declarado antes na cascata; navegador sem color-mix vê o site de hoje.
3. @property com transição de cor. Fallback: troca seca por minuto.
4. Scroll-driven animations (barra de progresso). Já protegida por @supports (animation-timeline: scroll()); sem suporte, sem barra.
5. View Transitions API. Já protegida por @view-transition com media de reduced-motion; sem suporte, navegação normal.
6. requestIdleCallback (montagem do mar). Fallback setTimeout de 2500ms.
7. IntersectionObserver (reveal e pausa do mar). As redes de segurança do visual.js já cobrem falha: tudo aparece em até 2s de qualquer jeito.
8. Intl com timeZone (hora de Brasília). Sem Intl, o céu fica no estado padrão e o site tem a cara de hoje.
9. content-visibility:auto + contain-intrinsic-size (seções abaixo da dobra). Sem suporte, nada acontece, só se perde a otimização de render.
10. EXT_disjoint_timer_query_webgl2 (medição de GPU). Fallback: proxy pelo intervalo entre rAFs.
11. SVG. Já é a espinha do site (sprite, logotipo, cenas .anima) e vira a camada de fallback oficial do mar.

Honestidade sobre a lista pedida: Three.js e React Three Fiber não entram, pela constituição e por mérito, seriam centenas de KB para desenhar um retângulo com fragment shader, e WebGL2 cru resolve com 6 KB. GSAP e Framer Motion não entram: WAAPI, transitions CSS e scroll-timeline cobrem tudo que esta direção precisa, e Framer Motion nem se aplica porque não há React. Lenis (scroll suave sequestrado) é rejeitado por mérito próprio, além da regra: sequestrar a rolagem num portal de notícias piora INP e a leitura, o scroll nativo fica. WebGPU não compensa hoje: ganho nulo para um shader 2D simples e suporte irregular justamente no Android intermediário do leitor típico; fica anotado como caminho futuro atrás de navigator.gpu, sem código agora. WebAssembly e Rust não têm papel: não existe carga de CPU que justifique, o gargalo do site é rede e o peso dos scripts de anúncio. Orçamento total da direção: cerca de 7 KB gzip somando JS e CSS novos, zero requests adicionais, tudo inline nos três arquivos existentes.

## riscos
PERFORMANCE. O risco número um é o shader disputar GPU e CPU com os scripts do AdSense no Android intermediário. Mitigações: mar só na home, 30fps, montagem em idle depois do load, DPR 1.0 no celular, 3 oitavas no mobile, teto de 3ms por quadro com rebaixamento automático e sem retorno no pageview. Segundo risco: a faixa do mar empurrar o carrossel (elemento LCP) para fora da dobra em telas de 360×640; mitigação: faixa de 96px no celular e teste de dobra obrigatório antes da aprovação. CLS: zero por construção, todas as alturas reservadas em CSS. INP: pointermove passive e rAF-throttled, sem scroll hijack, nenhum listener novo em elemento de leitura. Verificação em campo: acompanhar CrUX e Search Console por 28 dias após o deploy, com killswitch de uma linha (atributo data-mar="off" no html, que impede a montagem do canvas) para reverter sem novo deploy.

ACESSIBILIDADE. Canvas e ondas são aria-hidden e nada de conteúdo mora neles; o botão "Pausar o mar" cumpre a 2.2.2 e persiste a escolha; reduced-motion impede a montagem antes de qualquer código de shader rodar. O risco real é contraste: os estados de céu precisam de auditoria de espuma e mar-claro sobre o terço superior de cada gradiente (meta 4.5:1 mínimo em tudo, 7:1 no topo onde há texto) antes de ir ao ar, com o entardecer como pior caso. Movimento de água pode incomodar quem tem sensibilidade vestibular mesmo sem a preferência ativada: amplitude baixa (6px na resposta ao mouse), velocidade lenta e pausa visível são a resposta. Nenhuma regressão permitida no que já existe: carrossel pausável, skip link, foco visível e alvos de toque ficam como estão.

MANUTENÇÃO. O shader é o único trecho do repositório que exige conhecimento específico. Mitigações: bloco único e removível no visual.js, comentado linha a linha em português, constantes nomeadas no topo, e a remoção completa se resume a apagar um bloco de JS e uma div; o site volta ao estado atual sem cicatriz. O céu por hora pega carona no relógio que já existe, sem duplicar lógica de fuso. Risco de deriva de paleta: a regra "nenhum hex novo, toda cor derivada por color-mix das variáveis" precisa entrar no CLAUDE.md junto com a aprovação. Por fim, tudo isto é proposta: nada vai ao ar sem o editor humano aprovar, e a implementação deve nascer atrás do killswitch para o editor poder desligar o mar sozinho.