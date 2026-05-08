# Sales Data Warehouse

Pipeline ETL que carrega dados de vendas do [Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) em um data warehouse PostgreSQL seguindo um modelo de star schema.

## Arquitetura

O projeto segue a estrutura clássica de **star schema**:

```
                    ┌──────────────┐
                    │  dim_date    │
                    └──────┬───────┘
                           │
┌──────────────┐    ┌──────▼───────┐    ┌──────────────┐
│ dim_customer ├────►  fact_sales  ◄────┤ dim_product  │
└──────────────┘    └──────┬───────┘    └──────────────┘
                           │
                    ┌──────▼───────┐
                    │ dim_location │
                    └──────────────┘
```

## Estrutura do Projeto

```
sales_data_warehouse/
├── sql/
│   ├── schema.sql            # DDL de todas as tabelas
│   └── analytics_queries.sql # Queries analíticas prontas para uso
├── src/
│   ├── pipeline.py           # Ponto de entrada — executa o ETL completo
│   ├── extract.py            # Leitura do CSV bruto
│   ├── transform.py          # Limpeza e modelagem das dimensões e tabela fato
│   └── load_warehouse.py     # Carga dos dados no PostgreSQL
├── compose.yaml              # Docker Compose para a instância do Postgres
├── requirements.txt          # Dependências Python
├── superstore_sales.csv      # Dados de origem (não versionado)
└── .env                      # Variáveis de ambiente (não versionado)
```

## Pré-requisitos

- Python 3.9+
- Docker e Docker Compose
- Arquivo `superstore_sales.csv` na raiz do projeto

## Configuração

**1. Subir o banco de dados**

```bash
docker compose up -d
```

Isso inicia uma instância do PostgreSQL 15 na porta `5434`.

**2. Criar o arquivo `.env`**

```env
DATABASE_URL=postgresql://<usuario>:<senha>@<host>:<porta>/<banco>
```

**3. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**4. Criar o schema**

```bash
psql -h localhost -p 5434 -U postgres -d sales -f sql/schema.sql
```

**5. Executar o pipeline**

```bash
cd src
python pipeline.py
```

## Fluxo ETL

| Etapa | Arquivo | Descrição |
|---|---|---|
| Extract | `extract.py` | Lê o `superstore_sales.csv` em um DataFrame |
| Transform | `transform.py` | Remove duplicatas e modela as 4 dimensões e a tabela fato |
| Load | `load_warehouse.py` | Insere as dimensões primeiro, depois resolve as chaves substitutas para montar a `fact_sales` |

## Queries Analíticas

Queries prontas disponíveis em `sql/analytics_queries.sql`:

- **Receita total por trimestre** — receita agregada por trimestre e ano
- **Top 10 produtos por margem** — razão lucro/venda em ordem decrescente
- **Receita por região e categoria** — visão cruzada entre dimensões
- **Crescimento mês a mês** — variação percentual MoM com window function

## Conexão com o Banco

| Parâmetro | Valor |
|---|---|
| Host | `localhost` |
| Porta | `5434` |
| Banco | `sales` |
| Usuário | `postgres` |
