# MediTech - Plataforma de Consultas Médicas

Uma plataforma web de agendamento de consultas médicas, desenvolvida como projeto acadêmico.

## 📋 Integrantes

| Nome | RA |
|------|-----|
| Humebrto Filho | 2402662 |
| Anderson | 2403321 |
| Jullya Nigro| 2402577 |
| Melissa ferreira| 2403008 |

## 🛠️ Tecnologias

- **Python 3.12** + **Flask**
- **PostgreSQL 16**
- **Flask-JWT-Extended**
- **Docker Compose**

## 📁 Estrutura

O backend segue arquitetura em camadas para separar responsabilidades e facilitar manutencao.

### Visao Rapida do Fluxo

```text
HTTP Request
	 -> Controller (application/controllers)
	 -> Input DTO (usecases/*/*_input.py)
	 -> UseCase (usecases/*/*_usecase.py)
	 -> Repository Contract (domain/contracts)
	 -> Repository SQLAlchemy (repositories + mapeamento ORM -> dominio)
	 -> PostgreSQL (infrastructure/config/database.py + infrastructure/models)
```

### Responsabilidade de Cada Camada

- `src/application/app_factory.py`
	- Cria e configura a aplicacao Flask.
	- Registra controllers, extensoes e inicializacao geral.

- `src/application/controllers`
	- Recebe requisicoes HTTP.
	- Faz parse dos dados de entrada.
	- Chama os use cases.
	- Traduz erros para codigos HTTP (422, 401, 500 etc.).

- `src/usecases`
	- Implementa regras de negocio.
	- Nao depende de Flask.
	- Usa Input DTOs para validar/normalizar dados de entrada.

- `src/domain/models`
	- Entidades de dominio (conceitos de negocio).

- `src/domain/contracts`
	- Interfaces de repositorio usadas pelos use cases.
	- Desacopla regra de negocio da tecnologia de persistencia.

- `src/repositories`
	- Implementacoes concretas dos contratos.
	- Encapsula acesso ao banco via SQLAlchemy.
	- Faz mapeamento entre modelos ORM e entidades de dominio.

- `src/infrastructure`
	- Camada tecnica com adaptadores e configuracoes.
	- `config/`: configuracao do banco (`database.py`).
	- `models/`: modelos ORM SQLAlchemy.
	- `services/`: servicos tecnicos (ex.: hash/verificacao de senha).

## 🚀 Como Executar

### Com Docker Compose (recomendado)
```bash
docker compose up --build
```

### Reiniciar banco do zero (apaga dados)

Se você remove apenas os containers, os dados do PostgreSQL continuam no volume nomeado `postgres_data`.

Para remover containers e volumes:

```bash
docker compose down -v --remove-orphans
docker compose up --build
```

### Localmente
```bash
pip install -r requirements.txt
python run.py
```

Acesse: http://localhost:5000

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto baseado em `.env.example`.

Principais variáveis:

- `DB_HOST` (local: `localhost`; em Docker Compose o serviço da API sobrescreve para `db` automaticamente)
- `DB_PORT` (padrão: `5432`)
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `SECRET_KEY`
- `JWT_SECRET_KEY`

Observação Docker:

- API publicada em `localhost:5000`
- PostgreSQL publicado em `localhost:5433` (porta interna do container continua `5432`)

### Carga Inicial de Dados

Popula o banco com dados de exemplo: 10 especialidades, 1 admin, 50 médicos ativos e 10 inativos (com especialidades e horários).

**Senha padrão de todos os usuários:** `Meditech@2026`

#### Opção 1 — Comando Flask (local ou Docker)

```bash
# Local (venv ativo, banco rodando)
flask carga-inicial

# Dentro do container da API
docker compose exec api flask carga-inicial

# Para usar uma senha diferente
flask carga-inicial --senha "OutraSenha@123"
```

#### Opção 2 — Script SQL direto no banco

```bash
# Local
psql -U <DB_USER> -d <DB_NAME> -f scripts/carga_inicial.sql

# Via Docker Compose (banco rodando)
docker compose exec -T db psql -U <DB_USER> -d <DB_NAME> < scripts/carga_inicial.sql
```

> Ambas as opções são idempotentes: podem ser executadas mais de uma vez sem duplicar dados.

### Documentacao da API (Swagger)

- UI: `http://localhost:5000/apidocs`
- Spec: `http://localhost:5000/apispec_1.json`

Regra de manutencao:

- Sempre que criar ou alterar rota, atualize a documentacao Swagger/OpenAPI correspondente no controller.

### Estrutura de Pastas (Resumo)

```text
src/
	application/
		app_factory.py
		controllers/
		dependencies/
		docs/
	domain/
		models/
		contracts/
	usecases/
		cadastrar_usuario/
		login_usuario/
		cadastrar_consulta/
		listar_consultas/
	repositories/
	infrastructure/
		config/
		models/
		services/
```
