# Prompt do agente de notícias · Santa Informa

Rotina agendada que roda duas vezes por dia, às 6h e às 18h de Brasília
(09h e 21h em UTC, que é o fuso do agendador).

Para criar: `/schedule` e cole o bloco de prompt abaixo.
Para conferir depois: `/schedule` e peça a lista.
Para desligar: https://claude.ai/code/routines

## Antes de criar: conectar o GitHub

O agente roda NA NUVEM, não nesta máquina. Ele recebe um checkout do
repositório, então a conta do GitHub precisa estar conectada ao Claude,
senão a criação é recusada com erro 401. Rode `/web-setup` no Claude Code,
ou instale o app do Claude no repositório:
https://claude.ai/code/onboarding?magic=github-app-setup

## Dois limites da nuvem, já embutidos no prompt

1. **Sem Pexels.** O `.env` fica fora do Git, então a chave da API não existe
   na nuvem e o `buscar-imagem.py` não roda lá. O agente usa foto oficial
   (`foto-oficial.py`, que não precisa de chave) ou a ilustração SVG da marca,
   que são as duas melhores opções da Constituição de qualquer jeito.
2. **Sem caminho local.** Nada de `/Users/...` no prompt: o agente trabalha na
   raiz do checkout.

---

```
Crie um agente agendado chamado "Santa Informa · ciclo de notícias" que roda duas
vezes por dia, às 6h e às 18h no horário de Brasília, no diretório
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

LIMITE DA NUVEM: o `.env` não existe lá, então `buscar-imagem.py` (Pexels)
NÃO funciona. Use `python3 ferramentas/foto-oficial.py` para foto de
divulgação, ou a ilustração SVG da marca, copiando o padrão das matérias 04
e 12. As ferramentas usam Pillow; se faltar, `pip install pillow`.
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

## Por que 6h e 18h, e não a cada 48 horas

A janela do sitemap do Google News é de 48 horas, mas isso é o prazo de validade
das entradas, não a periodicidade de execução. Rodando a cada 48 horas, matéria
publicada logo depois de uma execução ficaria fora do sitemap por dois dias, e
matéria vencida ficaria dentro, o que o Google acusa como erro.

Com duas execuções diárias, o intervalo máximo é de 12 horas, bem dentro da
janela de 48. A das 6h pega o que os órgãos publicaram na véspera à noite e deixa
a matéria no ar antes do horário de maior leitura. A das 18h pega o expediente
inteiro da Prefeitura e da Câmara.

## Sobre custo

São 2 execuções por dia, cerca de 60 por mês. A seção 11 do CLAUDE.md diz que,
enquanto não houver receita, o padrão é ciclo assistido e automação tem orçamento
separado. Vale medir o custo na primeira semana. Se ainda pesar, dá para ficar só
com a das 18h, que é a que pega o expediente fechado.
