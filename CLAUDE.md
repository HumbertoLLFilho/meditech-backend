# MediTech Backend — Contexto para Claude

## Visão geral

API REST em Flask para uma plataforma de agendamento de consultas médicas, desenvolvida como projeto acadêmico no 4º semestre de AeS.

**Stack:** Python 3.12, Flask 3.0, SQLAlchemy, PostgreSQL, Flask-JWT-Extended, Flasgger (Swagger UI).

**Integrantes:**
- Humberto Filho (RA 2402662)
- Anderson (RA 2403321)
- Jullya Nigro (RA 2402577)
- Melissa Ferreira (RA 2403008)

---

## Como rodar

```bash
# Copiar e preencher variáveis de ambiente
cp .env.example .env

# Local (com venv ativo)
pip install -r requirements.txt
python run.py           # http://127.0.0.1:5000

# Docker
docker compose up --build
```

**Swagger UI:** `http://127.0.0.1:5000/apidocs`
**Spec JSON:** `http://127.0.0.1:5000/apispec_1.json`

> Docker: `DB_HOST=db` e `DB_PORT=5432` (o host `5433` é só para acesso local da máquina). O app usa sempre porta 5432 dentro da rede Docker.

---

## Variáveis de ambiente obrigatórias (.env)

| Variável        | Descrição                        |
|-----------------|----------------------------------|
| `DB_HOST`       | Host do banco (ex: `localhost`)  |
| `DB_PORT`       | Porta (default `5432`)           |
| `DB_NAME`       | Nome do banco                    |
| `DB_USER`       | Usuário do banco                 |
| `DB_PASSWORD`   | Senha do banco                   |
| `JWT_SECRET_KEY`| Chave secreta do JWT             |
| `SECRET_KEY`    | Chave secreta do Flask           |

---

## Arquitetura em camadas

```
src/
├── application/
│   ├── app_factory.py          ← create_app(): configura Flask, DB, JWT, Swagger, blueprints
│   ├── controllers/            ← Endpoints HTTP (Blueprints Flask)
│   ├── dependencies/
│   │   └── container.py        ← Injeção de dependência manual; cache por req via flask.g
│   └── docs/                   ← Dicts Python com specs Swagger (@swag_from)
├── domain/
│   ├── models/                 ← Entidades de negócio (dataclasses puras, sem ORM)
│   └── contracts/              ← Interfaces/contratos (ABCs) de repositórios e serviços
├── infrastructure/
│   ├── config/database.py      ← Instância SQLAlchemy (db)
│   ├── models/                 ← Modelos SQLAlchemy (mapeados para tabelas)
│   └── services/               ← Adaptadores: PasswordService (bcrypt), JwtTokenService
├── repositories/               ← Implementações dos contratos; mapeiam ORM → domínio
└── usecases/                   ← Regras de negócio; NÃO importam Flask
```

**Regra cardinal:** use cases nunca importam de `application/` nem de `flask`. Dependências entram por injeção via `container.py`.

---

## Entidades de domínio

### Usuario (`src/domain/models/usuario.py`)
```python
@dataclass
class Usuario:
    nome, sobrenome, data_nascimento, genero: Genero
    email, senha (hash), cpf, telefone
    tipo: TipoUsuario  # "admin" | "medico" | "paciente"
    ativo: bool        # médico recém-cadastrado nasce ativo=False
    id: int | None = None
    data_cadastro: datetime | None = None
```

### Consulta (`src/domain/models/consulta.py`)
```python
@dataclass
class Consulta:
    paciente_id, medico_id, especialidade_id: int
    data_agendada: date
    hora: str          # "HH:MM"
    id, data_cadastrada, cancelada
```

### Especialidade (`src/domain/models/especialidade.py`)
```python
@dataclass
class Especialidade:
    nome: str
    id: int | None = None
```

### HorarioDisponivel (`src/domain/models/horario_disponivel.py`)
```python
@dataclass
class HorarioDisponivel:
    medico_id: int
    especialidade_id: int
    dia_semana: int    # 0=segunda … 6=domingo (Python date.weekday())
    periodo: str       # "manha" | "tarde" | "noite"
    id: int | None = None
    medico: "Usuario | None" = field(default=None, compare=False)
    especialidade: "Especialidade | None" = field(default=None, compare=False)
```

---

## Banco de dados (SQLAlchemy)

| Tabela                  | Modelo SQLAlchemy              |
|-------------------------|--------------------------------|
| `usuarios`              | `UsuarioModel`                 |
| `consulta`              | `ConsultaModel`                |
| `especialidades`        | `EspecialidadeModel`           |
| `medico_especialidades` | tabela associativa (many-many) |
| `horarios_disponiveis`  | `HorarioDisponivelModel`       |

`HorarioDisponivelModel` tem `UniqueConstraint(medico_id, especialidade_id, dia_semana, periodo, name="uq_medico_esp_dia_periodo")`. Um médico pode ter o mesmo dia/período para especialidades distintas.
Tabelas criadas automaticamente no `create_app()` via `db.create_all()`.

---

## Endpoints e rotas

### Autenticação — `/auth`
| Método | Rota          | Auth | Descrição        |
|--------|---------------|------|------------------|
| POST   | `/auth/login` | —    | Login, retorna JWT |

### Usuários — `/usuarios`
| Método | Rota                | Auth         | Descrição                              |
|--------|---------------------|--------------|----------------------------------------|
| POST   | `/usuarios`         | —            | Cadastrar paciente (`tipo=paciente`, `ativo=True`) |
| POST   | `/usuarios/admin`   | JWT (admin)  | Cadastrar admin                        |
| POST   | `/usuarios/medico`  | —            | Cadastrar médico (`ativo=False`)       |
| GET    | `/usuarios`         | JWT (admin)  | Listar usuários (filtros: tipo, ativo, nome, cpf, ordem) |

### Consultas — `/consultas`
| Método | Rota         | Auth | Descrição                             |
|--------|--------------|------|---------------------------------------|
| POST   | `/consultas` | JWT  | Agendar consulta (paciente_id do JWT) |
| GET    | `/consultas` | JWT  | Listar consultas do usuário logado    |

### Especialidades — `/especialidades`
| Método | Rota                              | Auth         | Descrição                          |
|--------|-----------------------------------|--------------|------------------------------------|
| GET    | `/especialidades`                 | JWT          | Listar todas as especialidades     |
| POST   | `/especialidades`                 | JWT (admin)  | Cadastrar especialidade            |
| GET    | `/especialidades/medico/<id>`     | JWT          | Listar especialidades de um médico |
| POST   | `/especialidades/medico/<id>`     | JWT (admin)  | Associar especialidade ao médico   |

### Horários Disponíveis — `/horarios-disponiveis`
| Método | Rota                                   | Auth              | Descrição                                         |
|--------|----------------------------------------|-------------------|---------------------------------------------------|
| POST   | `/horarios-disponiveis`                | JWT (medico/admin) | Adicionar período disponível ao médico           |
| GET    | `/horarios-disponiveis/medico/<id>`    | JWT               | Listar horários disponíveis do médico             |
| DELETE | `/horarios-disponiveis/<id>`           | JWT (medico/admin) | Remover horário (médico só remove o próprio)     |
| GET    | `/horarios-disponiveis/disponivel`     | JWT               | Consultar slots livres (especialidade+data+período) |

---

## Autenticação e autorização

- JWT gerado via `JwtTokenService.generate_access_token()` usando `create_access_token` do Flask-JWT-Extended.
- Token salvo: `identity = str(usuario.id)`, `additional_claims = {email, nome, tipo}`.
- Expiração: 24h.
- Controllers protegidos com `@jwt_required()`.
- Papel do usuário extraído via `get_jwt().get("tipo")` e comparado com `TipoUsuario.ADMIN.value`, etc.
- Erros JWT já mapeados em `app_factory.py`: missing token → 401, expirado → 401, inválido → 422.

---

## Use cases

| Pasta                         | Classe UseCase                     | Responsabilidade                                     |
|-------------------------------|------------------------------------|------------------------------------------------------|
| `cadastrar_usuario/`          | `CadastrarUsuarioUseCase`          | Valida unicidade de e-mail/CPF, faz hash da senha    |
| `login_usuario/`              | `LoginUsuarioUseCase`              | Verifica senha, gera token                           |
| `listar_usuarios/`            | `ListarUsuariosUseCase`            | Listagem filtrada (admin only via controller)        |
| `cadastrar_consulta/`         | `CadastrarConsultaUseCase`         | Valida especialidade do médico, slot disponível, conflito 1h |
| `listar_consultas/`           | `ListarConsultaUseCase`            | Retorna consultas do usuário logado                  |
| `cadastrar_especialidade/`    | `CadastrarEspecialidadeUseCase`    | Cria especialidade (unicidade tratada no repositório)|
| `associar_especialidade_medico/` | `AssociarEspecialidadeMedicoUseCase` | Valida médico e especialidade, faz associação     |
| `adicionar_horario_disponivel/` | `AdicionarHorarioDisponivelUseCase` | Valida tipo médico, unicidade do período           |
| `listar_horarios_disponivel_medico/` | `ListarHorariosDisponivelMedicoUseCase` | Lista horários de um médico              |
| `listar_especialidades/`      | `ListarEspecialidadesUseCase`      | Lista todas as especialidades                        |
| `listar_especialidades_medico/` | `ListarEspecialidadesMedicoUseCase` | Lista especialidades de um médico                 |
| `consultar_disponibilidade/`  | `ConsultarDisponibilidadeUseCase`  | Retorna slots livres por especialidade/data/período  |

### Input DTOs
Cada use case tem um `*_input.py` com um `@dataclass` e método estático `from_dict(data)` ou `from_args(args)` que valida e converte os dados brutos. Erros de validação levantam `ValueError`.

---

## Lógica de horários (`src/usecases/horario_utils.py`)

```python
SLOTS_POR_PERIODO = {
    "manha": ["06:00" … "11:00"],   # 30min
    "tarde": ["13:00" … "17:00"],
    "noite": ["19:00" … "01:00"],
}

def sobrepostos(hora_a, hora_b) -> bool:
    # True se as consultas de 1h iniciadas em hora_a e hora_b se sobreponham
    # Considera wrap de meia-noite
```

---

## Injeção de dependências (`container.py`)

Sem biblioteca externa. Usa `flask.g` para cache por requisição (`_scoped(key, factory)`). Fora de contexto de requisição (testes, CLI), retorna um dict vazio (semântica best-effort).

Funções públicas: `get_cadastrar_usuario_use_case()`, `get_login_usuario_use_case()`, `get_cadastrar_consulta_use_case()`, `get_listar_consultas()`, `get_listar_usuarios()`, `get_cadastrar_especialidade()`, `get_listar_especialidades()`, `get_listar_especialidades_medico()`, `get_associar_especialidade_medico()`, `get_adicionar_horario_disponivel()`, `get_listar_horarios_disponivel_medico()`, `get_consultar_disponibilidade()`, `get_horario_disponivel_repository()`.

---

## Swagger / OpenAPI

- Habilitado via Flasgger; UI em `/apidocs`.
- Cada rota usa `@swag_from(ALGUM_DOC_DICT)`.
- Dicts de spec ficam em `src/application/docs/` separados por domínio:
  - `auth_docs.py` → `AUTH_LOGIN_DOC`
  - `consultas_docs.py` → `CONSULTA_CADASTRAR_DOC`, `CONSULTA_LISTAR_DOC`
  - `especialidades_docs.py` → `ESPECIALIDADE_*`
  - `horarios_disponiveis_docs.py` → `HORARIO_*`, `DISPONIBILIDADE_*`
  - `usuarios_docs.py` → `USUARIO_*`
- **Obrigatório:** qualquer rota nova ou alterada deve ter doc Swagger atualizado antes de fechar a tarefa.

---

## Códigos HTTP esperados

| Situação                       | Código |
|--------------------------------|--------|
| Cadastro bem-sucedido          | 201    |
| Operação/consulta bem-sucedida | 200    |
| Credenciais inválidas          | 401    |
| Token ausente/expirado         | 401    |
| Acesso negado (role)           | 403    |
| Erro de validação / ValueError | 422    |
| Token inválido (malformado)    | 422    |
| Erro inesperado                | 500    |

---

## Padrões de código

- Controllers: traduzem HTTP ↔ use cases; capturam `ValueError` → 422, `InvalidCredentialsError` → 401, `Exception` genérica → 500.
- Repositories: fazem `db.session.flush()` + `commit()`; em falha fazem `rollback()`.
- Repositories mapeiam modelos ORM para entidades de domínio (`_to_domain()`); jamais retornam objetos ORM para use cases.
- Use cases: Python puro, sem Flask.
- Nunca retornar objeto ORM fora do repositório.

---

## Comandos úteis

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar local
python run.py

# Rodar com Docker
docker compose up --build

# Derrubar containers e volumes
docker compose down -v
```

---

## Checklist antes de finalizar qualquer tarefa

- [ ] Use cases sem importação de Flask.
- [ ] Validações de input no DTO (`from_dict` / `from_args`).
- [ ] Controller mapeia todos os erros para HTTP correto.
- [ ] Repositório faz rollback em caso de falha.
- [ ] Toda rota nova/alterada tem Swagger doc atualizado.
- [ ] Endpoints retornam JSON válido nos códigos HTTP esperados.
- [ ] Fluxo local e Docker continuam funcionando.
