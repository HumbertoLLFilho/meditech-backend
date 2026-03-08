"""
MediTech - Plataforma de Consultas Médicas
Aplicação Flask simples
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
db_user = os.getenv('DB_USER', 'postgres')
db_password = quote(os.getenv('DB_PASSWORD', 'postgres'), safe='')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '5432')
db_name = os.getenv('DB_NAME', 'meditech')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

db = SQLAlchemy(app)


# Rota de teste
@app.route('/')
def index():
    return {
        'message': 'Bem-vindo ao MediTech',
        'version': '0.1.0',
        'status': 'running'
    }


# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
