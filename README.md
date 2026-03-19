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

## 📁 Estrutura

Estrutura principal do backend Flask organizada em camadas:

- `src/application/app_factory.py`: setup e application factory do Flask
- `src/application/controllers`: endpoints HTTP e parse de request
- `src/repositories`: implementacoes de persistencia (SQLAlchemy)
- `src/domain/models`: entidades de dominio
- `src/domain/contracts`: contratos de repositorio
- `src/usecases`: regras de negocio
- `src/infrastructure`: banco, modelos e container de dependencias
