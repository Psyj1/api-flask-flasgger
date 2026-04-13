```markdown
# API de Acervo de Sacolas

API para gerenciamento de sacolas de supermercado.

## Tecnologias

- Python 3.12
- Flask
- Flasgger
- SQLAlchemy
- PostgreSQL
- Docker
- Alembic
- Pydantic

## Estrutura

```
apps/backend/
├── src/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   ├── schemas/
│   └── scripts/seed.py
├── migrations/
├── .env
├── alembic.ini
└── pyproject.toml
```

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/api-flask-flasgger.git
cd api-flask-flasgger
```

### 2. Suba o banco de dados

```bash
docker-compose up -d
```

### 3. Configure o arquivo .env

Crie `apps/backend/.env`:

```
DATABASE_URL=postgresql://devuser:devpassword@localhost:5432/sacolas
```

### 4. Instale as dependências e execute as migrations

```bash
cd apps/backend
uv sync
uv run alembic upgrade head
```

### 5. Popule o banco de dados

```bash
uv run python src/scripts/seed.py
```

### 6. Execute a API

```bash
uv run python src/app.py
```

A API estará disponível em `http://localhost:5000`

## Documentação

Swagger: `http://localhost:5000/apidocs`

## Endpoints

### Sacolas

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/sacolas/ | Lista todas |
| GET | /api/sacolas/{id} | Busca uma |
| GET | /api/sacolas/{id}/supermercados | Lista supermercados que usam a sacola |
| POST | /api/sacolas/ | Cria |
| PUT | /api/sacolas/{id} | Atualiza |
| DELETE | /api/sacolas/{id} | Remove |

### Supermercados

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/supermercados/ | Lista todos |
| GET | /api/supermercados/{id} | Busca um |
| GET | /api/supermercados/{id}/materiais | Lista materiais do supermercado |
| POST | /api/supermercados/ | Cria |
| PUT | /api/supermercados/{id} | Atualiza |
| DELETE | /api/supermercados/{id} | Remove |

### Materiais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/materiais/ | Lista todos |
| GET | /api/materiais/{id} | Busca um |
| POST | /api/materiais/ | Cria |
| PUT | /api/materiais/{id} | Atualiza |
| DELETE | /api/materiais/{id} | Remove |

### Resgates

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/resgates/ | Lista todos |
| GET | /api/resgates/{id} | Busca um |
| POST | /api/resgates/ | Registra resgate |
| POST | /api/resgates/reset | Reseta progresso |
| PUT | /api/resgates/{id} | Atualiza |
| DELETE | /api/resgates/{id} | Remove |

## Comandos úteis

```bash
# Parar o banco
docker-compose down

# Recriar banco do zero
docker-compose down -v
docker-compose up -d
uv run alembic upgrade head
uv run python src/scripts/seed.py

# Criar nova migration
uv run alembic revision --autogenerate -m "nome_da_migration"
```