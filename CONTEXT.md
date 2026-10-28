# Contexto do projeto TickerBR

Atualizado em 27/10/2026. Este arquivo registra o estado para retomada em outra sessão.

## Objetivo

Construir o TickerBR como uma API aberta de dados do mercado brasileiro. O projeto foi iniciado em Django e deverá separar duas responsabilidades: um coletor em segundo plano consulta as fontes e grava observações; a API lê essas observações e as entrega aos clientes. Ainda não há banco de dados de aplicação, modelos, API de mercado nem agendamento implementados.

## Estado atual

- Há um projeto Django inicial e o app `market_data`.
- O primeiro coletor em implementação é o BTG Pactual. A página pública segue o padrão `https://content.btgpactual.com/research/ativo/{TICKER}/`.
- `market_data/sources/btg.py` consulta a página, extrai o preço-alvo, a recomendação e a data do relatório mais recente que apresenta o mesmo preço-alvo. Também registra a data de consolidação mostrada na página.
- O comando `probe_btg` faz consultas de leitura e não grava no banco. Exemplo: `uv run python manage.py probe_btg PETR4`.
- O coletor foi consultado ao vivo em 27/10/2026. PETR4 retornou R$ 65,00 (análise de 20/10/2026); VALE3, R$ 90,00 (16/10/2026); ITUB4, R$ 54,00 (26/10/2026). PETR4 também foi consultado como `petr4`, com espaços e como `PETR4.SA`, mantendo o mesmo resultado.
- A implementação experimental do Inter foi removida. O Inter permanece apenas no README de inventário histórico das fontes dos repositórios antigos; não está implementado como coletor do TickerBR.
- Os arquivos de teste adicionados durante a exploração foram removidos a pedido do usuário. Não adicionar testes ou executar a suíte de testes sem solicitação.
- Não criar banco de dados ou tabelas sem pedido explícito. O arquivo `db.sqlite3` não existe.

## Fonte do universo de tickers

O BTG consulta um ticker por vez, então o produto precisará de um catálogo de instrumentos separado da cobertura do BTG. A fonte candidata é o Cadastro de Instrumentos Listados da B3, filtrado para o escopo do produto (inicialmente ações e units, salvo decisão diferente). O Hub de dados públicos da B3 informa que coleta automatizada é vedada; antes de automatizar essa carga, confirmar um canal autorizado ou licença. A BrAPI documenta `/api/v2/tickers` como alternativa prática para protótipo, mas a lista representa a cobertura da BrAPI, não necessariamente o cadastro oficial completo, e cria dependência de um produto concorrente.

## Decisões e cuidados de dados

- Diferenciar data da análise publicada e data da coleta. Uma cotação recente não prova que o preço-alvo foi atualizado recentemente.
- Não misturar preço-alvo fundamentalista com `Alvo (Gain)` técnico. Cada observação deverá guardar fonte, URL, tipo de alvo, moeda, data da análise e data de coleta.
- Preservar histórico de mudanças de alvos; a API deve poder retornar o valor mais recente sem apagar observações anteriores.
- Tickers sem alvo no BTG devem ser classificados como sem cobertura/dado, e não como ticker inválido.

## Próximos passos sugeridos

1. Definir o escopo de instrumentos (ações, units e se entram BDRs, FIIs e ETFs).
2. Resolver uma fonte autorizada para carregar e atualizar o catálogo de tickers.
3. Continuar validando o coletor BTG em mais tickers, verificando datas, alvos ausentes, recomendações e mudanças de layout.
4. Só depois modelar no banco o catálogo, as execuções do coletor e o histórico das observações.
5. Implementar o agendamento do coletor e a API de leitura.

## Arquivos relevantes

- `market_data/sources/btg.py` — cliente e parser do BTG.
- `market_data/management/commands/probe_btg.py` — comando de consulta manual.
- `README.md` — inventário das fontes encontradas nos repositórios antigos; não representa funcionalidades já implementadas.
- `pyproject.toml` e `uv.lock` — dependências Python.
