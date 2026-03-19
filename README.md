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
	 -> Repository SQLAlchemy (repositories)
	 -> PostgreSQL (infrastructure/database.py + models)
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

- `src/infrastructure`
	- Configuracao de banco, modelos ORM e container de dependencias.

### Fluxos Principais da API

1. Cadastro de usuario (`POST /usuarios/cadastrar`)
	 - Controller recebe payload.
	 - Input DTO valida formato e campos obrigatorios.
	 - Use case aplica regras (ex.: email/CPF unicos).
	 - Repository persiste no banco.
	 - Controller retorna `201` em sucesso.

2. Login (`POST /usuarios/login`)
	 - Controller recebe credenciais.
	 - Use case valida usuario e senha.
	 - Controller gera JWT com `create_access_token`.
	 - Retorno esperado: token e status `200`.

3. Consultas (`POST /consultas` e `GET /consultas`)
	 - Rotas protegidas com `@jwt_required()`.
	 - Usuario autenticado e identificado com `get_jwt_identity()`.
	 - Use cases cadastram/listam consultas do usuario.
	 - Retornos esperados: `201` para cadastro, `200` para listagem.

## 🔌 Endpoints Principais

- `GET /`
	- Health check simples da API.

- `POST /usuarios/cadastrar`
	- Cadastro de usuario.

- `POST /usuarios/login`
	- Autenticacao e retorno de JWT.

- `POST /consultas`
	- Cadastro de consulta para usuario autenticado.

- `GET /consultas`
	- Listagem de consultas do usuario autenticado.

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
```
