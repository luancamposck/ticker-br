# TickerBR

Inventário das fontes encontradas nos repositórios analisados. A tabela descreve o que esses projetos consultam ou referenciam; ela não significa que o TickerBR já coleta esses dados.

| Link da fonte | O que buscamos nessa fonte | Nome da fonte |
|---|---|---|
| https://content.btgpactual.com/research/home/acoes/ativo/{ticker} | Para o ticker, preço-alvo, recomendação e data da análise (`queue_stocks`, `server_stocks`). | BTG Pactual |
| https://interinvest.inter.co/acoes | Pesquisa pelo ticker; preço-alvo, recomendação e data (`queue_stocks`, `server_stocks`). | Inter Invest |
| https://www.safra.com.br/resultado-de-busca.htm?query={ticker} | Busca de relatórios pelo ticker; preço-alvo, recomendação e data (`scraping_acoes`, `queue_stocks`, `server_stocks`). | Banco Safra |
| https://conteudos.xpi.com.br/acoes/{ticker} | Para o ticker, preço-alvo, recomendação e data da análise (`queue_stocks`, `server_stocks`). | XP |
| https://analisa.genialinvestimentos.com.br/acoes/ | O módulo tenta obter recomendação e preço-alvo; existe em `server_stocks`, mas não está conectado ao fluxo ativo. | Genial Investimentos |
| https://www.economiaemdia.com.br/SiteEconomiaEmDia/Projecoes/Longo-Prazo | Data, anos e projeções cambiais de longo prazo (`server_stocks`). O resultado é salvo no Firebase sob a chave `bradesco`. | Economia em Dia |
| https://www.itau.com.br/itaubba-pt/analises-economicas/projecoes | Página que publica uma planilha; o código extrai a série de projeções cambiais por ano (`server_stocks`). | Itaú BBA |
| https://www.bcb.gov.br/content/focus/focus/R20240301.pdf | Relatório Focus referenciado como imagem estática no dashboard de `scraping_stocks`; os repositórios analisados não baixam esse relatório por código. | Banco Central do Brasil (BCB) |
| https://www.tradingview.com/ | O dashboard de `scraping_stocks` filtra registros do Supabase com `src = "Tranding View"`; não identificamos scraper nem chamada direta ao TradingView nos repositórios analisados. | TradingView (rótulo no banco) |
| https://brapi.dev/api/quote/list | Consulta de busca/listagem de ativos via API no projeto `stock_market`; não é scraping de uma instituição financeira. | BrAPI |
