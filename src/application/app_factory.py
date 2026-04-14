"""
MediTech - Plataforma de Consultas Medicas
Application Factory
"""
import os
import socket
from datetime import timedelta
from urllib.parse import quote

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
import click
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from src.infrastructure.config.database import db


load_dotenv()
jwt = JWTManager()

_REQUIRED_ENV_VARS = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_NAME",
    "JWT_SECRET_KEY",
]


def _validate_env_vars() -> None:
    missing = [var for var in _REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing:
        raise EnvironmentError(
            f"Variaveis de ambiente obrigatorias nao configuradas: {', '.join(missing)}"
        )


def create_app() -> Flask:
    _validate_env_vars()
    app = Flask(__name__)
    CORS(app)
    _configure_database(app)
    _init_extensions(app)
    _register_models()
    _register_blueprints(app)
    _register_routes(app)
    _register_commands(app)
    _create_tables(app)

    return app


def _configure_database(app: Flask) -> None:
    db_user = os.getenv("DB_USER")
    db_password = quote(os.getenv("DB_PASSWORD"), safe="")
    db_host = _resolve_db_host(os.getenv("DB_HOST"))
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)


def _resolve_db_host(configured_host: str) -> str:
    # Fora da rede Docker, o alias "db" nao existe; usa localhost no desenvolvimento local.
    if configured_host != "db":
        return configured_host

    if os.path.exists("/.dockerenv"):
        return configured_host

    try:
        socket.gethostbyname(configured_host)
        return configured_host
    except socket.gaierror:
        return "localhost"


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    jwt.init_app(app)
    _init_swagger(app)


def _init_swagger(app: Flask) -> None:
    app.config["SWAGGER"] = {
        "title": "MediTech API",
        "uiversion": 3,
        "openapi": "3.0.2",
    }

    template = {
        "openapi": "3.0.2",
        "info": {
            "title": "MediTech API",
            "version": "0.1.0",
            "description": "API para usuarios e consultas medicas.",
        },
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }
        },
    }

    Swagger(app, template=template)


def _register_models() -> None:
    import src.infrastructure.models.usuario_model  # noqa: F401
    import src.infrastructure.models.consulta_model  # noqa: F401
    import src.infrastructure.models.documento_model  # noqa: F401
    import src.infrastructure.models.especialidade_model  # noqa: F401
    import src.infrastructure.models.horario_disponivel_model  # noqa: F401


def _register_blueprints(app: Flask) -> None:
    from src.application.controllers.auth_controller import auth_bp
    from src.application.controllers.consulta_controller import consulta_bp
    from src.application.controllers.especialidade_controller import especialidade_bp
    from src.application.controllers.horario_disponivel_controller import horario_disponivel_bp
    from src.application.controllers.usuario_controller import usuario_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(especialidade_bp)
    app.register_blueprint(horario_disponivel_bp)

    _register_medico_pendente_restriction(app)


def _register_medico_pendente_restriction(app: Flask) -> None:
    from flask import jsonify, request
    from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

    from src.domain.models.usuario import StatusAprovacao, TipoUsuario

    @app.before_request
    def _restricao_medico_pendente():
        try:
            verify_jwt_in_request(optional=True)
        except Exception:
            return  # Token invalido sera tratado pelo decorator da rota

        claims = get_jwt()
        if not claims:
            return  # Rota publica

        tipo = claims.get("tipo")
        status = claims.get("status_aprovacao")

        if tipo == TipoUsuario.MEDICO.value and status != StatusAprovacao.APROVADO.value:
            usuario_id = get_jwt_identity()
            rota_permitida = f"/usuarios/{usuario_id}"
            if request.method == "GET" and request.path == rota_permitida:
                return  # Permite acesso ao proprio perfil
            return jsonify({"erro": "Acesso restrito. Seu cadastro ainda esta em analise."}), 403


def _register_routes(app: Flask) -> None:
    @app.route("/")
    def index():
        return {
            "message": "Bem-vindo ao MediTech",
            "version": "0.1.0",
            "status": "running",
        }


@jwt.unauthorized_loader
def _jwt_missing_token(reason: str):
    return {"erro": "Token ausente ou invalido.", "detalhe": reason}, 401


@jwt.invalid_token_loader
def _jwt_invalid_token(reason: str):
    return {"erro": "Token invalido.", "detalhe": reason}, 401


@jwt.expired_token_loader
def _jwt_expired_token(_jwt_header, _jwt_payload):
    return {"erro": "Token expirado."}, 401


def _create_tables(app: Flask) -> None:
    with app.app_context():
        db.create_all()
        _migrate_drop_sobre_mim()
        _migrate_add_status_aprovacao()


def _migrate_drop_sobre_mim() -> None:
    from sqlalchemy import text
    try:
        db.session.execute(text("ALTER TABLE usuarios DROP COLUMN IF EXISTS sobre_mim"))
        db.session.commit()
    except Exception:
        db.session.rollback()


def _migrate_add_status_aprovacao() -> None:
    from sqlalchemy import text
    try:
        db.session.execute(text(
            "ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS status_aprovacao VARCHAR(20)"
        ))
        db.session.execute(text(
            "UPDATE usuarios SET status_aprovacao = 'aprovado' "
            "WHERE tipo = 'medico' AND ativo = TRUE AND status_aprovacao IS NULL"
        ))
        db.session.execute(text(
            "UPDATE usuarios SET status_aprovacao = 'novo' "
            "WHERE tipo = 'medico' AND ativo = FALSE AND status_aprovacao IS NULL"
        ))
        db.session.commit()
    except Exception:
        db.session.rollback()


def _register_commands(app: Flask) -> None:
    @app.cli.command("carga-inicial")
    @click.confirmation_option(prompt="Isso vai inserir dados iniciais no banco. Continuar?")
    def carga_inicial():
        """Insere carga inicial executando scripts/carga_inicial.sql."""
        from sqlalchemy import text

        sql_path = os.path.join(os.path.dirname(os.path.dirname(app.root_path)), "scripts", "carga_inicial.sql")
        if not os.path.exists(sql_path):
            click.echo(f"Arquivo SQL não encontrado: {sql_path}", err=True)
            raise SystemExit(1)

        sql = open(sql_path, encoding="utf-8").read()

        with db.engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()

        click.echo("Carga inicial concluída. Senha padrão: Meditech@2026")
