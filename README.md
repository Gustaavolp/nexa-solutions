# Sistema de Chamados — Nexa Solutions

API de chamados internos desenvolvida em Django e Django REST Framework, com
uma interface HTML simples para consulta e cadastro. Projeto da disciplina
de Manutenção e Evolução de Software.

## Tecnologias

- Python 3.12 / Django 5 / Django REST Framework
- PostgreSQL 16
- Docker e Docker Compose
- Git / GitHub (issues, branches e Pull Requests)

## Estrutura

```text
backend/   # API Django (app "chamados")
frontend/  # Interface HTML simples
docs/      # Documentação e demandas da empresa
```

## Como executar

### 1. Configurar variáveis de ambiente

Copie o arquivo de exemplo e ajuste os valores se necessário:

```bash
cp .env.example .env
```

O `.env` nunca deve ser versionado (já está no `.gitignore`); apenas o
`.env.example`, com valores fictícios, faz parte do repositório.

### 2. Subir com Docker Compose

```bash
docker compose up --build
```

O comando sobe dois serviços:

- `db`: PostgreSQL 16, com dados persistidos em volume nomeado (`pgdata`).
- `api`: aplicação Django, que aguarda o banco ficar saudável
  (`healthcheck`/`depends_on`), aplica as migrações automaticamente e sobe
  em `http://localhost:8000`.

A API estará disponível em `http://localhost:8000/api/chamados/`.

Para acompanhar os logs: `docker compose logs -f api`.
Para encerrar: `docker compose down` (os dados do banco continuam no
volume; use `docker compose down -v` para descartá-los).

### Frontend

`frontend/index.html` é uma página estática sem build. Basta abrir o
arquivo diretamente no navegador com a API rodando em `localhost:8000`.

## Executando os testes

Com os containers no ar:

```bash
docker compose exec api python manage.py test
```

## Endpoints

| Método | Rota | Descrição |
| --- | --- | --- |
| `GET` | `/api/chamados/` | Lista chamados. Aceita filtro opcional `?status=ABERTO\|EM_ANDAMENTO\|CONCLUIDO`. Status inválido retorna `400`. |
| `POST` | `/api/chamados/` | Cria um chamado. `titulo` é obrigatório; ausência ou valor em branco retorna `400`. |
| `GET` | `/api/chamados/<id>/` | Detalha um chamado. |
| `PATCH` | `/api/chamados/<id>/` | Atualiza parcialmente um chamado. |
| `GET` | `/api/indicadores/` | Retorna `total`, `abertos`, `em_andamento` e `concluidos`. |

Exemplo de cadastro:

```bash
curl -X POST http://localhost:8000/api/chamados/ \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Impressora não liga", "descricao": "Sem energia"}'
```

## Decisões técnicas

- **PostgreSQL em vez de SQLite**: atende ao requisito de ambiente
  reproduzível e mais próximo de produção; credenciais e nome do banco vêm
  de variáveis de ambiente (`POSTGRES_*`), nunca fixas no código.
- **Migração automática no start do container**: o `CMD` do `Dockerfile`
  roda `migrate` antes do `runserver`, então `docker compose up --build`
  já entrega o banco pronto para uso, sem passo manual extra.
- **`depends_on` com `condition: service_healthy`**: evita que a API tente
  conectar ao banco antes dele aceitar conexões (`pg_isready`).
- **`python-dotenv`**: usado apenas para carregar o `.env` em execuções
  locais fora do Docker (ex.: `manage.py test` na máquina do
  desenvolvedor); dentro dos containers as variáveis já chegam via
  `env_file` do Compose.
- **Sem CORS/serviço de frontend no Compose**: o critério de indicadores é
  atendido pelo endpoint `GET /api/indicadores/`; a página estática em
  `frontend/index.html` pode ser aberta diretamente no navegador.

## Fluxo de contribuição

Alterações não são feitas diretamente na `main`. Cada demanda de
`docs/issues.md` virou uma issue no GitHub, tratada em uma branch própria e
integrada via Pull Request:

- `fix/inc-05-variaveis-ambiente`
- `feat/inc-04-docker-postgres`
- `fix/inc-01-validacao-titulo`
- `feat/inc-02-filtro-status`
- `feat/inc-06-indicadores`
- `test/inc-07-testes-automatizados`
- `docs/inc-03-documentacao`

## Evidências

- `docker compose up --build` executado com sucesso, subindo `db` e `api`.
- `docker compose exec api python manage.py test` executando a suíte
  automatizada sem falhas.
