"""
MediTech - Plataforma de Consultas Médicas
Aplicação Flask - Application Factory
"""
import os
from urllib.parse import quote

from dotenv import load_dotenv
from flask import Flask

from src.infrastructure.database import db

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    _configure_database(app)
    _init_extensions(app)
    _register_models()
    _register_blueprints(app)
    _register_routes(app)
    _create_tables(app)

    return app


def _configure_database(app: Flask) -> None:
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = quote(os.getenv('DB_PASSWORD', 'postgres'), safe='')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'meditech')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')


def _init_extensions(app: Flask) -> None:
    db.init_app(app)


def _register_models() -> None:
    import src.infrastructure.usuario_model  # noqa: F401
    import src.infrastructure.documento_model  # noqa: F401


def _register_blueprints(app: Flask) -> None:
    from src.adapters.controllers.usuario_controller import usuario_bp
    app.register_blueprint(usuario_bp)


def _register_routes(app: Flask) -> None:
    @app.route('/')
    def index():
        return {
            'message': 'Bem-vindo ao MediTech',
            'version': '0.1.0',
            'status': 'running'
        }


def _create_tables(app: Flask) -> None:
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
