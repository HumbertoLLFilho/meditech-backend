# MediTech - Plataforma de Consultas Médicas

Uma plataforma web de agendamento de consultas médicas online, similar ao Doutor Consulta, desenvolvida como projeto acadêmico.

## 📋 Integrantes

| Nome | RA |
|------|-----|
| Humebrto Filho| 2402662|
| | |
| | |
| | |

## 💡 Sobre o Projeto

MediTech é uma aplicação web que permite:
- 🏥 Pacientes agendar consultas com médicos
- 👨‍⚕️ Médicos gerenciarem sua agenda
- 📅 Gerenciamento de agendamentos em tempo real
- 👤 Autenticação e perfis de usuário
- 📱 Interface intuitiva e responsiva

## 🛠️ Tecnologias

### Backend
- **Python 3.9+**
- **Flask** - Framework web
- **MySQL** - Banco de dados relacional
- **SQLAlchemy** - ORM (Object-Relational Mapping)
- **Flask-Login** - Gerenciamento de autenticação
- **python-dotenv** - Variáveis de ambiente

### Frontend
- HTML5
- CSS3/Bootstrap
- JavaScript

## 📦 Instalação

### Pré-requisitos
- Python 3.9 ou superior
- MySQL 5.7+ ou MariaDB
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**
   ```bash
   git clone <seu-repositorio>
   cd meditech-backend
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**
   
   No Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   No Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Instale as dependências**
   ```bash
   pip install flask
   pip install flask-sqlalchemy
   pip install flask-login
   pip install python-dotenv
   pip install mysql-connector-python
   ```
   
   Ou use o arquivo requirements.txt (quando disponível):
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure o banco de dados**
   - Crie um arquivo `.env` na raiz do projeto com:
     ```
     DATABASE_URL=mysql+mysqlconnector://usuario:senha@localhost:3306/meditech
     SECRET_KEY=sua_chave_secreta_aqui
     FLASK_ENV=development
     ```
   - Substitua `usuario`, `senha` com suas credenciais MySQL

6. **Execute a aplicação**
   ```bash
   python app.py
   ```
   A aplicação estará disponível em `http://localhost:5000`

## 📁 Estrutura do Projeto

```
MediTech/
├── src/
│   ├── app.py                 # Arquivo principal
│   ├── models/                # Modelos de dados (User, Doctor, Appointment, etc)
│   ├── routes/                # Rotas da API
│   ├── templates/             # Templates HTML
│   ├── static/                # Arquivos estáticos (CSS, JS, imagens)
│   └── config.py              # Configurações
├── requirements.txt           # Dependências Python
├── .env                       # Variáveis de ambiente (não versionado)
├── .gitignore                 # Arquivos ignorados pelo Git
└── README.md                  # Este arquivo
```

## 🗄️ Banco de Dados

### Tabelas principais
- **users** - Usuários do sistema (pacientes e médicos)
- **doctors** - Informações de médicos
- **specialties** - Especialidades médicas
- **appointments** - Agendamentos de consultas
- **availability** - Horários disponíveis dos médicos

## 🚀 Como Executar

Enable your Python environment and run:
```bash
python src/app.py
```

## 🤝 Contribuindo

Como se trata de um projeto universitário, solicite permissão antes de fazer grandes alterações.

## 📝 Notas de Desenvolvimento

- Mantenha o código limpo e bem comentado
- Siga a PEP 8 para estilo de código Python
- Crie branches para novas features
- Documente suas alterações

## 📄 Licença

Este projeto é fornecido para fins educacionais.

---
