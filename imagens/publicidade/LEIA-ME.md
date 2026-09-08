# Publicidade vendida direto

Esta pasta guarda as peças de campanhas vendidas direto (fora do AdSense) e o
registro de cada contrato, em `registro.json`.

## Campanha no ar

**PI 33092.26 · Saúde 24h, Telemedicina Itapema · Fundo Municipal de Saúde de Itapema**

- Veiculação: 08/09/2026 a 07/10/2026 (30 dias)
- Peças: Super Banner 970x250 (celular 320x100) logo abaixo da capa do index,
  e Retângulo 300x250 no Resumo Semanal do index
- Retirada em duas camadas: (1) o visual.js esconde no navegador todo
  `.anuncio.pago` cujo `data-fim` já passou no fuso de Brasília, então em
  08/10/2026 o anúncio some sozinho para quem visita o site; (2) a limpeza
  do repositório apaga os blocos `.pago` do index.html e devolve os
  placeholders "Espaço disponível" guardados em comentário ao lado de cada
  bloco

## ATENÇÃO: artes provisórias

Os três PNG desta pasta foram gerados pelo próprio portal, só com os dados
oficiais da campanha (texto, telefone 0800 333 7973 e endereço do site da
Prefeitura), sem os logos do anunciante, porque os arquivos finais da agência
não chegaram ao repositório. Antes de aprovar a publicação, substitua cada
PNG pelo arquivo final da agência Ômega, mantendo o mesmo nome:

- `saude-24h-telemedicina-970x250.png`
- `saude-24h-telemedicina-320x100.png`
- `saude-24h-telemedicina-300x250.png`

Se a arte final vier em JPG, converta para PNG ou ajuste os `src` no
index.html. A peça precisa ser estática, sem script e sem pixel de terceiro:
é a promessa feita ao leitor no aviso de cookies (anúncio sempre não
personalizado, sem rastreamento).

## Regra da casa

Conteúdo pago leva selo e nome do pagante (seção 8 do CLAUDE.md). O selo mora
no próprio slot, classe `.anuncio.pago`, escrito direto no HTML, porque o
rótulo automático do visual.js só funciona para blocos do AdSense.
