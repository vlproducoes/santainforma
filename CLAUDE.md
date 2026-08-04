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
página, na raiz. CSS único em `estilo.css`, JS único em `visual.js`.

**Responsável público:** Lucas Esmerio Varela · CNPJ 51.087.731/0001-57 ·
vl7producoes@gmail.com · Itapema, Santa Catarina.

## 2. Regra que não se quebra

**Nada vai ao ar sem aprovação do editor humano.** Você prepara, ele aprova.
Nenhum commit em `main` e nenhum deploy sem o editor mandar.

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
- **CSS:** só `estilo.css`. Use as variáveis que já existem (`--mar`, `--sol`,
  `--suave`, `--display`). Não crie paleta nova.
- **JS:** só `visual.js`. Sem framework, sem dependência externa.
- **Acentuação:** os HTML são UTF-8. Escreva com acento correto no conteúdo.
- **Nomes de arquivo:** minúsculo, sem acento, separado por hífen.

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
