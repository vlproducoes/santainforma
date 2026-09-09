# CLAUDE.md · Santa Informa

Regras deste repositório. Leia antes de qualquer tarefa.

A lei completa está em `constituicao-santa-informa-v1.3.md`, na raiz. Em conflito,
a Constituição vence este arquivo. Só o editor humano altera a Constituição.

---

## 1. O que é este projeto

`santainforma.com.br`, portal de notícias do litoral catarinense. Foco em Itapema
e Costa Esmeralda, expandindo para Litoral Norte, Vales e Santa Catarina.
Nacional só quando conversa com o leitor daqui.

**Stack:** HTML estático, sem build. GitHub e Cloudflare Pages. Um arquivo por
página, na raiz. CSS único em `estilo.css`, JS único em `visual.js`. Exceção
única de servidor: `functions/clima.js`, função do Cloudflare Pages que
devolve a condição do tempo da região do visitante para o céu da capa
(decisão do editor em 22/08/2026). O ciclo de notícias NÃO toca em
`functions/`; erro de sintaxe ali reprova o deploy inteiro do Pages.

**Responsável público:** Lucas Esmerio Varela · CNPJ 51.087.731/0001-57 ·
vl7producoes@gmail.com · Itapema, Santa Catarina.

## 2. Regra que não se quebra

**O ciclo de notícias publica sozinho.** O agente agendado apura, escreve,
confere e dá `git push origin main`. O Cloudflare sobe. Não para para pedir
aprovação. Decisão do editor registrada em 18 de agosto de 2026.

**Autorização permanente de escrita em `main`.** O editor autoriza, de forma
permanente e sem precisar ser perguntado de novo a cada execução, que o ciclo de
notícias escreva direto na branch `main` deste repositório. Se a sessão vier
presa a uma branch `claude/`, ignore essa amarração e comece assim:

```
git fetch origin main
git checkout -B main origin/main
```

Trabalhe, commite e termine com `git push origin main`. Não abra branch, não abra
pull request e não termine a execução pedindo aprovação para publicar matéria do
ciclo. Decisão do editor registrada em 19 de agosto de 2026.

Se o push voltar erro de permissão do servidor, aí sim é bloqueio de verdade, e
não tem frase que resolva: commite na branch que der, avise no relatório que a
rotina precisa ser reconfigurada e não diga que publicou.

Publicar sozinho não é publicar sem trava. Só sai o que passar por todas estas,
e a ordem importa:

1. Sem fato novo, não publica. Assunto já coberto não vira matéria de novo.
2. As linhas vermelhas da seção 8 valem inteiras. Na dúvida, não publica.
3. `python3 ferramentas/checa-site.py` tem que sair com código 0. Reprovou,
   conserta. Não conseguiu consertar, não commita.
4. Nenhuma chave no commit. Encontrou, para tudo e avisa o editor.
5. Cada dado publicado saiu de página de fonte que abriu de verdade. Resumo de
   busca não confere dado.

**O que continua precisando de aprovação antes de ir ao ar:** tudo que não é
matéria do ciclo. Layout, CSS, página institucional, tabela de preços, política
editorial, texto sobre o próprio portal, conteúdo pago e qualquer mudança nesta
lista. Isso o agente prepara em branch e o editor aprova.

O editor tem palavra final depois, não antes. Matéria que não devia ter saído
sai com `git revert` e nota de correção, do jeito que manda a seção 18 da
Constituição.

## 3. Como escrever

- Português brasileiro falado, simples. Frases curtas, uma ideia por frase.
- **Nunca usar travessão.** Use vírgula, ponto ou parênteses.
- Evitar cara de IA: nada de "não é X, é Y", nada de paralelismo simétrico
  demais, nada de lista de três por vício de ritmo.
- Humor sem crueldade. Nunca rir da pessoa comum.
- Sem jargão, sem economês, sem juridiquês.
- Referência de tom: o jeito direto e popular de comunicar do Jorginho Mello,
  sem posição partidária.

## 4. Formato padrão da matéria

Todo arquivo de matéria segue `materia-NN-slug-do-assunto.html` e contém:

1. Chapéu (editoria e cidade)
2. Título SEO
3. Linha fina
4. **Modo de Leitura** com 5 versões: 30 segundos (padrão), completa, Clara,
   Seu Prudêncio, Caco
5. Figura de topo com legenda e crédito
6. Seção "Entenda o assunto", em texto corrido
7. Box "O que ainda está em aberto"
8. Lista "Os números que importam"
9. Fontes linkadas no rodapé
10. Dados estruturados `NewsArticle` em JSON-LD

Corpo entre 300 e 500 palavras. Copie a estrutura de
`materia-01-alargamento-meia-praia.html`, que é o modelo canônico.

## 5. Os três colunistas

São criações assumidas do portal, nunca apresentadas como pessoas reais.

**Clara, a otimista.** Enxerga oportunidade e lado bom, sem passar pano.

**Seu Prudêncio, o criterioso.** Examina prazo, custo, execução e manutenção com
rigor técnico. Aponta o que merece atenção e **fecha sempre reconhecendo o
benefício quando ele existe**. Postura de consultor que quer o projeto dar certo.
Vocabulário: "vale acompanhar", "merece atenção", "uma sugestão útil".
Proibido tom de denúncia. Proibido "quem paga a conta".
Limite: o miolo precisa levantar questão real. Elogio do começo ao fim destrói
o formato.

**Caco, o sarcástico.** Ri da situação, nunca da pessoa. Reclama e vira elogio
enviesado. Modelo: "tá lotado porque o lugar é bom", "tá ruim mas é progresso".

## 6. Imagem

Ordem de preferência:

1. **Foto própria.** Melhor opção sempre.
2. **Divulgação oficial identificada.** Crédito completo, com o órgão e o ano:
   `Foto: Prefeitura de Itapema/Divulgação, 2019`. Nunca só "Divulgação".
3. **Banco gratuito (Pexels).** Sempre como **imagem ilustrativa**, nunca como
   registro do fato. Crédito: `Imagem ilustrativa · Nome do Fotógrafo/Pexels`.
4. **Ilustração SVG da marca.** Já existe nas matérias 04 e 05. Use quando não
   houver imagem honesta disponível. É a saída mais segura.

**Regra da foto da fonte.** Quando a fonte oficial publica foto do próprio fato,
usar a foto dela, não banco de imagem. Foto real do evento vale mais que stock
bonito. Só cair para o Pexels quando a fonte não tiver foto, ou quando a foto
dela não puder ser usada.

O que cada fonte permite, conferido em 10 de agosto de 2026:

| Fonte | O que diz | Uso |
|---|---|---|
| Prefeitura de Itapema | sem termos publicados | Divulgação, com crédito completo |
| Câmara de Itapema | sem termos publicados | Divulgação, com crédito completo |
| Agência Brasil / EBC | "reprodução autorizada para veículos de comunicação com fins jornalísticos, mediante indicação da fonte" | Pode, creditando o fotógrafo |
| Governo de SC | "todos os direitos reservados" | **Não usar** sem autorização escrita |
| Portais de notícia | — | Nunca |

Na Agência Brasil, conferir foto a foto: parte do conteúdo vem de agência
parceira e às vezes traz "Proibida reprodução". Se tiver essa marca, não usa.

**Antes de aplicar qualquer foto, olhe a imagem.** Se houver criança em quadro,
recorte para tirá-la ou escolha outra. O mesmo vale para plateia e para rosto de
pessoa comum em primeiro plano: a regra de não expor vale mesmo quando foi o
órgão público que publicou.

**Proibido:** foto de terceiro sem licença, foto de portal de notícia, foto que
sugira documentar um fato que ela não documenta.

**Regra de idade.** Foto com mais de 3 anos não ilustra matéria sobre mudança
recente da paisagem. O ano vai no crédito, sempre.

Para baixar do Pexels:

```bash
python3 ferramentas/buscar-imagem.py "termo de busca" --listar
python3 ferramentas/buscar-imagem.py "termo de busca" --nome slug-do-arquivo --escolher 2
```

O script salva em `imagens/`, registra a origem em `imagens/creditos.json` e
imprime o bloco `<figure>` pronto. A chave da API fica em `.env`, que está no
`.gitignore`. **O repositório é público: nenhuma chave entra em arquivo versionado.**

## 7. Fontes

Toda matéria lista as fontes com link no rodapé. Camadas sugeridas:

1. Prefeitura e Câmara de Itapema, Rádio Cidade SC, Visor Notícias
2. Governo de SC, NSC, ND Mais, TVBV, Diarinho, Jornal Razão
3. Busca aberta e grandes veículos nacionais

**Reescrita 100% original.** Citação curta com crédito pode. Parágrafo copiado,
jamais.

## 8. Linhas vermelhas

Nunca, em hipótese nenhuma:

- Data retroativa. Nenhuma matéria recebe data anterior à publicação real.
- Dado inventado ou declaração que não existiu.
- Acusação sem documento oficial ou duas fontes independentes.
- Expor pessoa comum sem interesse público claro.
- Sensacionalismo com tragédia.
- Pauta de saúde ou segurança sem fonte oficial.
- Conteúdo eleitoral. Nada de pedir voto, promover ou atacar candidato.
- Publicidade disfarçada de matéria. Conteúdo pago leva selo e nome do pagante.
- Prometer resultado que não dá para validar.

**Na dúvida, não publica.**

## 9. Convenções de código

- **HTML:** indentação de 2 espaços. Todo `<img>` com `width`, `height`,
  `loading` e `alt` descritivo de verdade. Nada de `alt=""` em foto editorial.
- **CSS:** só `estilo.css`. Use as variáveis que já existem: as da marca
  (`--breu`, `--marinho`, `--sol-logo`, `--mar-logo`, `--grafite`, `--pedra`,
  `--papel`, `--coral`, `--areia`, `--suave`), a camada semântica (`--fundo`,
  `--superficie`, `--tinta`, `--fio-cor`, `--link`) e a paleta editorial
  (`--ed-*`, seção 9.5). Cor nova fora dessas variáveis, só com aprovação do
  editor. `--mar`, `--sol`, `--mar-claro` e `--espuma` são apelidos: existem
  porque 156 pedaços de HTML trazem `style="color:var(--mar)"` cravado. Não
  use os apelidos em código novo.
- **JS:** só `visual.js`. Sem framework, sem dependência externa. Exceção
  registrada: `functions/clima.js` (servidor, ver seção 1).
- **Acentuação:** os HTML são UTF-8. Escreva com acento correto no conteúdo.
- **Nomes de arquivo:** minúsculo, sem acento, separado por hífen.

## 9.5 O layout (redesign de 06/09/2026, site todo claro desde 09/09)

A estrutura do index.html continua a mesma de 19/08/2026: pacote de capa no
lugar do carrossel, com manchete dominante, rio de últimas, sub-destaques,
seção com líder e pilha, Resumo Semanal e ferramentas. A ordem e a regra de
rotação estão comentadas no próprio index.html e no prompt do agente
(`ferramentas/prompt-agente-noticias.md`). O que mudou em 06/09 foi a
vestimenta: o `estilo.css` foi reescrito com anatomia de jornal (faixa de
marca, barra de editorias que gruda, régua dupla nos títulos de seção,
cards brancos com fio) e acabamento de restrição (ar entre blocos, raio
máximo de 12px, sombra só no hover, folha branca). Depois do primeiro
resultado no ar, a cor foi revista três vezes: os tons do leque, que estavam
escuros demais e faziam o site ler como preto e branco; a marca, porque o azul
esverdeado e o amarelo davam ao site a cara de material gerado por IA; e por
fim o site inteiro, que ficou claro do topo ao rodapé, com o topo no jeito do
site da Apple e sem as ondas. O registro das três está em
`proposta/17-redesign-layout-set-2026.md`.

Regras do layout:

- **O site é todo claro (decisão do editor, 09/09/2026).** Não existe faixa
  escura, bloco escuro nem modo escuro. Nada de `@media prefers-color-scheme`
  no `estilo.css`: se alguém precisar de modo escuro de novo, é conversa com o
  editor. O Resumo Semanal e a leitura do horóscopo, que eram os dois blocos
  escuros, hoje são faixas em `--superficie-2`. A classe `.escuro` continua no
  HTML e o nome mente: hoje quer dizer "faixa de fundo chapado".
- **A marca é o azul marinho.** `--marinho` é a cor da marca: letras do logo,
  link, foco, item ativo e régua. `--breu` é a tinta do texto. `--coral` é só
  urgência (bolinha de Últimas, erro, 404, sublinhado de link no hover).
  `--grafite`, `--pedra`, `--papel`, `--areia` e `--suave` são os neutros, sem
  fundo ciano: cinza esverdeado é metade da cara de template.
- **O logo guarda as cores do desenho.** O sol é sol (`--sol-logo`) e o mar é
  mar (`--mar-logo`), e essas duas variáveis não aparecem em mais lugar nenhum
  do site. As letras vão em `--marinho`. O SVG das 185 páginas traz os hex
  antigos como atributo de apresentação, que perde para qualquer regra de CSS,
  então quem pinta o logo é o bloco 4. Página nova que o ciclo gerar copiando o
  cabeçalho antigo já nasce com a cor certa, sem ninguém mexer.
- **O topo é no jeito Apple.** Barra branca e translúcida com blur por trás,
  tipo pequeno em peso 400, hairline de 1px embaixo e nada mais. Nada de faixa
  colorida, gradiente, sombra ou logo grande. Depois de rolar sobra só a barra
  de editorias, com 44px. Alvo de toque de 44px continua valendo: mexeu no
  padding da nav, roda a auditoria.
- **Sem ondas.** A faixa `.horizonte` da capa, o botão de pausa e o selo saíram
  em 09/09. O HTML continua com a `<div class="horizonte">` (não mexemos em
  página), então o CSS a esconde. Não reponha onda em lugar nenhum.
- **Paleta editorial aprovada.** As oito cores da marca continuam intocadas.
  Além delas existem doze cores de editoria (`--ed-poder-publico`,
  `--ed-economia`, `--ed-infraestrutura`, `--ed-santa-catarina`,
  `--ed-turismo`, `--ed-meio-ambiente`, `--ed-servico`, `--ed-brasil`,
  `--ed-cultura`, `--ed-esporte`, `--ed-clima`, `--ed-saude`), mais
  `--ed-cidade`, que é apelido de `--ed-servico`. Cada uma tem três tons e só
  três: o tom vivo (`--ed-X`, que é o que o site usa), o `-claro` (7:1 ou mais
  sobre breu, que hoje nenhuma regra usa: ficou pronto caso o modo escuro
  volte) e o `-tint` (fundo pálido).
  `--ed-X-texto` não existe mais como tom separado: virou apelido do tom
  vivo. Todos com contraste medido no bloco 1 do `estilo.css`. Para conferir,
  `python3 ferramentas/contraste.py` lê a paleta do CSS, mede tom por tom nos
  dois modos e sai com código 1 se algum par cair abaixo de 4,5:1. Cor fora
  dessa lista, só com aprovação do editor.
- **O tom precisa parecer cor.** A primeira paleta ficava entre 6,5:1 e
  10,5:1: passava no AA de sobra e, em caixa alta de 12px, lia como preto.
  A faixa de trabalho é de 4,6:1 a 5,2:1 sobre branco, e o piso é 4,5:1 em
  todos os fundos onde o tom vive. Tom novo entra medido pelo
  `ferramentas/contraste.py`, nessa faixa, nunca "no olho".
- **A cor identifica editoria, nunca decora.** Ela entra no chapéu (texto e
  ponto), no fio de 3px no topo do card, no fio à esquerda das chamadas da
  pilha, no filete da manchete, no ícone e no item ativo da barra de
  editorias, no topo da página de editoria (tint mais fio de 4px), na barra
  de leitura da matéria, no painel de 30 segundos, no box "o que ainda está
  em aberto", na régua dos colunistas e no rótulo do Resumo Semanal. Nunca em
  título de chamada, corpo de texto ou fundo de seção inteira.
- Componente novo usa a camada semântica (`--fundo`, `--superficie`,
  `--tinta`, `--tinta-2`, `--tinta-3`, `--fio-cor`, `--link`) e a cor viva
  (`--ed`, `--ed-texto`, `--ed-claro`, `--ed-tint`), nunca hex direto.
- Tamanho, espaço e forma saem dos tokens: `--t-*` (tipografia fluida),
  `--e-*` e `--esp-*` (espaço), `--raio`, `--raio-s`, `--pilula`.
- O chapéu das chamadas traz "Cidade · Assunto". O `visual.js` lê esse texto
  e escreve `data-editoria`, que é o que liga a cor. Assunto que não cai em
  regra nenhuma fica sem editoria: chapéu e fio na tinta da casa, que é o
  certo, porque vestir a cor de outra editoria seria mentira. Se um assunto
  novo começar a aparecer muito, acrescente o termo ao mapa no fim do
  `visual.js`.
- O céu por hora saiu junto com as ondas: com a faixa de marca branca não há
  onde pintar céu. O `visual.js` segue escrevendo as classes `ceu-*` e
  `tempo-*`, que hoje não pintam nada, e segue chamando o `/clima`. Se elas
  nunca mais forem usadas, essa chamada e o `functions/clima.js` podem sair,
  mas isso é decisão do editor.
- Movimento novo usa os tokens `--dur-*` e `--curva-*`. Estado invisível mora
  sempre no `from` do keyframe, nunca na regra do elemento. Nada de sombra em
  repouso, hover em foto ou raio maior que 12px.
- Nada de `transform` em repouso em `.chip`, `.signo`, `.manchete`, `.sub`,
  `.lider-sec`, `.pilha article` e `article.card.v2`: a mola do JS escreve
  `transform` neles no toque.
- Convenção de view transition: a imagem da chamada e a foto de topo da
  matéria compartilham o nome `capa-mNN`, os dois lados escritos pelo
  `visual.js` (no clique da chamada e no `pagereveal` da matéria). Nome único
  por página: só a primeira foto de topo entra.
- O material de design da equipe está na pasta `proposta/`.

## 10. Ao criar página nova

Toda página precisa de:

- `<title>`, `meta description`, `canonical`, Open Graph
- Cabeçalho e rodapé idênticos aos das outras páginas
- Link no rodapé, se for institucional
- Entrada em `sitemap.xml`

## 11. Onde cada coisa acontece

- **Projeto no Claude.ai:** estratégia, decisão, aprovação, matéria avulsa.
- **Claude Code (aqui):** construção do site, geração em lote, scripts.
- **Claude in Chrome:** pesquisa de pauta com sessão já logada. Nunca digita senha.
- **Postiz ou API oficial:** publicação em rede social.

**Regra de custo.** Enquanto não houver receita, o padrão é ciclo assistido: o
editor dispara, a IA executa, o editor aprova. Automação headless tem orçamento
separado e só entra depois de medida.
