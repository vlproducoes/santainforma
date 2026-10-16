# Publicidade vendida direto

Esta pasta guarda as peças de campanhas vendidas direto (fora do AdSense) e o
registro de cada contrato, em `registro.json`.

## Campanha no ar

**PI 33113.26 · Avança Itapema, Prevenção El Niño · Prefeitura de Itapema**

- O PI marca 15/10/2026 a 13/11/2026 (30 dias). A publicação não saiu no
  dia 15, então, por decisão do editor, as peças entraram em 16/10/2026 e
  ficam até 14/11/2026: o dia perdido no começo foi compensado no fim. A
  Ômega Comunicação vai mandar PI novo com essas datas; quando chegar,
  registre o número em `registro.json`, campo `ajuste_de_datas`
- Peças: Super Banner 970x250 (celular 320x100) logo abaixo da capa do index,
  e Retângulo 300x250 no Resumo Semanal do index
- Retirada em duas camadas: (1) o visual.js esconde no navegador todo
  `.anuncio.pago` cujo `data-fim` já passou no fuso de Brasília, então à 0h
  de 15/11/2026 o anúncio some sozinho para quem visita o site; (2) a
  limpeza do repositório apaga os blocos `.pago` do index.html e devolve os
  placeholders "Espaço disponível" guardados em comentário ao lado de cada
  bloco. Não existe rotina agendada externa: a camada 2 é disparada pelo
  editor, pedindo a limpeza em qualquer sessão a partir de 15/11/2026

## Campanhas encerradas

- **PI 33092.26 · Saúde 24h, Telemedicina Itapema · Fundo Municipal de Saúde
  de Itapema.** No ar de 08/09/2026 a 07/10/2026, com reexibição a pedido do
  editor em 13/10/2026 até as 19h. Blocos apagados do index.html em
  16/10/2026, quando o PI 33113.26 entrou nos mesmos espaços

## Formato do data-fim

- `AAAA-MM-DD`: último dia no ar. A peça some à meia-noite do dia seguinte.
- `AAAA-MM-DDTHH:MM`: hora exata da retirada, no fuso de Brasília. A peça
  some nessa hora, e o visual.js confere de minuto em minuto para quem deixou
  a página aberta.

Qualquer outro formato é ignorado e a peça fica no ar. Para reexibir uma
campanha por algumas horas, basta trocar o `data-fim` dos blocos `.pago`.

## O que sai e o que fica na retirada

Saem: os dois blocos `.pago` do index.html (com seus comentários) e a
campanha da seção "Campanha no ar" deste arquivo, que passa para "Campanhas
encerradas". Ficam: os JPG e o registro.json (arquivo do contrato; acrescente
`"retirada_em"` ao registro), as regras `.anuncio.pago` do estilo.css e o
bloco PUBLICIDADE VENDIDA DIRETO do visual.js, que são infraestrutura da casa
para campanhas futuras.

## Artes

**PI 33113.26.** Artes da agência entregues pelo editor no chat em
16/10/2026, em resolução maior que o formato. Cada peça foi reduzida para o
tamanho do contrato e para o dobro (sufixo `-2x`, servido pelo `srcset` a
telas de alta densidade):

- `avanca-itapema-el-nino-970x250.jpg` e `-970x250-2x.jpg`
- `avanca-itapema-el-nino-320x100.jpg` e `-320x100-2x.jpg`
- `avanca-itapema-el-nino-300x250.jpg` e `-300x250-2x.jpg`

**PI 33092.26.** Artes finais da agência, entregues pelo editor em
08/09/2026 pela pasta TELEMEDICINA no Google Drive:

- `saude-24h-telemedicina-970x250.jpg`
- `saude-24h-telemedicina-320x100.jpg`
- `saude-24h-telemedicina-300x250.jpg`

Toda peça vendida direto precisa ser estática, sem script e sem pixel de
terceiro: é a promessa feita ao leitor no aviso de cookies (anúncio sempre
não personalizado, sem rastreamento).

## Regra da casa

Conteúdo pago leva selo e nome do pagante (seção 8 do CLAUDE.md). O selo mora
no próprio slot, classe `.anuncio.pago`, escrito direto no HTML, porque o
rótulo automático do visual.js só funciona para blocos do AdSense.
