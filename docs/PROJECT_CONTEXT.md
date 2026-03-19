# MediTech Backend - Project Context

## Stack
- Python 3.12
- Flask 3
- Flask-SQLAlchemy
- Flask-JWT-Extended
- PostgreSQL 16
- Docker Compose

## Execucao
### Local
1. Criar .env a partir de .env.example
2. pip install -r requirements.txt
3. python run.py

Entry point atual: run.py -> src/application/app_factory.py:create_app

### Docker
1. docker compose up --build
2. API em http://localhost:5000

## Variaveis de Ambiente
- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD
- SECRET_KEY
- JWT_SECRET_KEY

## Endpoints Principais
### GET /
- Health simples da API

### POST /usuarios/cadastrar
- Cadastra usuario
- Campos: nome, sobrenome, data_nascimento(YYYY-MM-DD), genero, email, senha, cpf

### POST /usuarios/login
- Autentica usuario
- Campos: email, senha
- Retorna access_token

### POST /consultas
- Cria consulta para usuario autenticado
- Header: Authorization: Bearer <token>
- Campos: especialidade, medico, data(YYYY-MM-DD), horario

### GET /consultas
- Lista consultas do usuario autenticado
- Header: Authorization: Bearer <token>

## Fluxo de Arquitetura
Controller -> Input DTO -> UseCase -> Repository Contract -> Repository -> SQLAlchemy Model

## Regras de Dominio Importantes
- Senha e salva com hash (werkzeug.security.generate_password_hash).
- Login valida hash com check_password_hash.
- Email e CPF nao podem repetir no cadastro.
- Genero deve ser um valor do Enum Genero.

## Estrutura de Pastas (Atual)
- src/application/controllers
- src/repositories
- src/domain/models
- src/domain/contracts
- src/usecases
- src/infrastructure

## Debitos Tecnicos Observados
- Repositories retornam modelos ORM em buscas, em vez de entidades de dominio.
- Nao ha suite de testes automatizados no repositorio atual.
