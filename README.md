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
