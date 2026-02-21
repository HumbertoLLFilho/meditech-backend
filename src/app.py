"""
MediTech - Plataforma de Consultas Médicas
Aplicação Flask simples
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados SQLite
db_path = os.getenv('DATABASE_PATH', 'instance/meditech.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
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
