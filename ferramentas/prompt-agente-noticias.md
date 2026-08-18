# Prompt do agente de notícias · Santa Informa

Cole o bloco abaixo no Claude Code, dentro de `/Users/viniciusdelego/Documents/santainforma`.
Ele cria um agente agendado que roda de 6 em 6 horas.

Para criar: `/schedule` e cole o prompt.
Para conferir depois: `/schedule` e peça a lista.
Para desligar: `/schedule` e peça para apagar a rotina "Santa Informa · ciclo de notícias".

---

```
Crie um agente agendado chamado "Santa Informa · ciclo de notícias" que roda de
6 em 6 horas (00h, 06h, 12h e 18h no horário de Brasília), no diretório
/Users/viniciusdelego/Documents/santainforma.

A cada execução, faça exatamente isto, nesta ordem:

## 1. Leia as regras antes de qualquer coisa
Leia o CLAUDE.md do repositório. Ele manda. Em especial: nunca use travessão,
escreva em português falado e simples, e respeite as linhas vermelhas da seção 8.
Leia também a matéria mais recente (a de número mais alto) para copiar a
estrutura exata: chapéu, título, linha fina, painel "Em 30 segundos", figura de
topo com legenda e crédito, "Entenda o assunto", box "O que ainda está em
aberto", lista "Os números que importam", os três colunistas (Clara, Seu
Prudêncio e Caco), fontes linkadas, o bloco .pub-google e os espaços .anuncio.

## 2. Procure pauta nas fontes oficiais
Nesta ordem de prioridade:
1. Prefeitura de Itapema (itapema.sc.gov.br) e Câmara de Itapema
2. Governo de SC, corpos oficiais estaduais, MPSC, IMA
3. Agência Brasil / EBC para pauta nacional que converse com o leitor daqui

Compare com o que já está publicado: liste os títulos das matérias existentes
antes de decidir, para não repetir assunto já coberto.

## 3. Decida se publica, e quantas
Publique de zero a três matérias por execução, conforme houver fato novo real.

REGRA QUE NÃO SE QUEBRA: se não houver fato novo, NÃO PUBLIQUE NADA. Encerre a
execução dizendo que não havia pauta. É melhor não publicar do que inventar,
esticar assunto velho ou repetir o que já está no ar. Nunca crie dado,
declaração ou número que não esteja na fonte.

Outras travas:
- Nada de conteúdo eleitoral, nem a favor nem contra ninguém.
- Postura de bandeira branca: informe sem bater de frente com o poder público.
  Quando houver conflito (ação judicial, cobrança de órgão), registre o fato de
  forma neutra e traga a posição das duas partes, sem tom de denúncia.
- Nada de exposição de pessoa comum sem interesse público claro.
- Saúde e segurança só com fonte oficial.
- Na dúvida, não publica.

## 4. Imagem
Ordem: foto própria, depois divulgação oficial identificada (crédito completo
com órgão e ano), depois banco gratuito como "imagem ilustrativa", depois a
ilustração SVG da marca.

- Governo de SC é direito reservado: NÃO USAR.
- Foto de portal de notícia: nunca.
- Na Agência Brasil, confira foto a foto: se trouxer "Proibida reprodução", não usa.
- OLHE a imagem antes de aplicar. Se houver criança em quadro, ou rosto de pessoa
  comum em primeiro plano, recorte ou escolha outra.
- Foto com mais de 3 anos não ilustra mudança recente de paisagem. O ano vai no
  crédito, sempre.

Ferramentas: `python3 ferramentas/foto-oficial.py` para foto oficial e
`python3 ferramentas/buscar-imagem.py "termo" --listar` para o banco gratuito.
Gere sempre as versões WebP e as miniaturas m<NN>-card.jpg e m<NN>-mini.jpg.

## 5. Publique
Para cada matéria nova, com o número seguinte ao mais alto existente:
- Crie materia-NN-slug.html copiando a estrutura da matéria mais recente
- Corpo entre 300 e 500 palavras
- JSON-LD NewsArticle completo: headline, description, datePublished E
  dateModified com hora e fuso (-03:00), author (Redação Santa Informa), image
  em URL absoluta, publisher e mainEntityOfPage
- Inclua o bloco .pub-google antes de "Os números que importam"
- Ligue nas listagens: carrossel e grade do index.html (o mais antigo sai), a
  editoria certa, e as páginas noticias*.html (o arquivo é de 6 por página, e
  incluir no topo empurra tudo; crie página nova se precisar, e acerte
  paginação, títulos e o contador "página N de M")
- Acrescente ao sitemap.xml

## 6. Regenere o sitemap de notícias SEMPRE
Rode `python3 ferramentas/sitemap-noticias.py` em TODA execução, mesmo quando
não publicar nada. Ele só aceita as últimas 48 horas: se não rodar, matéria
vencida fica no arquivo e o Google acusa erro.

## 7. Confira antes de publicar
Rode uma checagem que reprove o commit se algo falhar:
- Toda página: title, meta description, canonical, Open Graph, o Analytics
  G-PQKY68PE07 e link para anuncie.html
- Exatamente um <h1> por página
- Tags balanceadas (main, section, div, span, article, figure, ul, li, p, a,
  table, time, ins, script)
- Nenhum travessão no conteúdo
- JSON-LD válido em todas, e com todos os campos acima
- Todo <img> com width, height, loading e alt descritivo de verdade
- Nenhum link interno quebrado
- Nenhum data-agora dentro de span.quando (data de publicação é fixa, nunca
  relógio)
- Nenhum bloco .pub-google fora de página de matéria
- estilo.css com chaves balanceadas
- As imagens citadas no JSON-LD existem mesmo no disco

CUIDADO CONHECIDO: nunca edite HTML ou CSS com regex de regra inteira nem com
`.*?` entre duas âncoras. Isso já quebrou este site duas vezes, apagando corpo de
regra agrupada e pondo relógio na data de publicação de cards. Recorte o bloco
alvo pela extensão real (contando abertura e fechamento) e edite dentro dele.
Depois de qualquer edição em lote, compare o diff com o commit anterior e
confirme que só as linhas pretendidas mudaram.

## 8. Varredura de chave
O repositório é público. Antes do commit, confira que a chave do .env não está
na árvore nem no histórico do git. Se estiver, PARE e não publique.

## 9. Commit e deploy
Commit em português, explicando o que foi publicado e por quê, terminando com:
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>

Depois `git push origin main`. O Cloudflare Pages publica sozinho.

## 10. Verifique no ar
O Cloudflare tem propagação de borda: faça várias leituras por URL, com
cache-busting (?cb=aleatório) e Cache-Control: no-cache, repetindo até passar ou
até 8 tentativas. Confira que cada matéria nova responde, que a home linka para
ela e que o sitemap-noticias.xml no ar traz as matérias certas.
Use grep -F em textos com R$ ou outros caracteres especiais.

## 11. Relate
Ao fim, diga em poucas linhas: quantas matérias saíram e quais, ou que não havia
pauta; quantas entradas ficaram no sitemap de notícias; e qualquer coisa que
tenha ficado pendente ou duvidosa. Se você tomou alguma decisão editorial
difícil (recusou uma pauta, rejeitou uma foto), diga qual e por quê.
```

---

## Por que 6 horas e não 48

A janela do sitemap do Google News é de 48 horas, mas isso é o prazo de validade
das entradas, não a periodicidade de execução. Rodando de 6 em 6 horas, matéria
nova entra no sitemap em no máximo 6 horas e matéria vencida sai antes de o
Google reclamar. Rodando a cada 48 horas, os dois problemas apareceriam.

## Sobre custo

São 4 execuções por dia, cerca de 120 por mês. A seção 11 do CLAUDE.md diz que,
enquanto não houver receita, o padrão é ciclo assistido e automação tem
orçamento separado. Vale medir o custo na primeira semana antes de deixar rodando
em definitivo. Se pesar, dá para baixar para 2 execuções por dia (12h e 18h)
sem prejudicar o sitemap, já que a janela é de 48 horas.
