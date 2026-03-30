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


def _register_commands(app: Flask) -> None:
    @app.cli.command("carga-inicial")
    @click.option("--senha", default="Meditech@2026", show_default=True, help="Senha padrão para todos os usuários criados.")
    @click.confirmation_option(prompt="Isso vai inserir dados iniciais no banco. Continuar?")
    def carga_inicial(senha):
        """Insere carga inicial: 10 especialidades, 1 admin, 50 medicos ativos e 10 inativos."""
        from datetime import date
        from src.domain.models.usuario import TipoUsuario
        from src.infrastructure.models.especialidade_model import EspecialidadeModel
        from src.infrastructure.models.horario_disponivel_model import HorarioDisponivelModel
        from src.infrastructure.models.usuario_model import UsuarioModel
        from src.infrastructure.services.password_service import PasswordService

        senha_hash = PasswordService().hash(senha)
        A = TipoUsuario.ADMIN.value
        M = TipoUsuario.MEDICO.value

        # fmt: off
        # (nome, sobrenome, data_nasc, genero, email, cpf, telefone, tipo, ativo)
        usuarios = [
            ("Admin",    "MediTech",  date(1990,  1,  1), "masculino", "admin@meditech.com",                "00000000001", "11900000001", A, True ),
            # ── Clínica Geral (10 ativos) ──────────────────────────────────────
            ("Ana",      "Lima",      date(1985,  3, 15), "feminino",  "ana.lima@meditech.com",             "00000000002", "11911110002", M, True ),
            ("Joao",     "Pereira",   date(1980,  8, 14), "masculino", "joao.pereira@meditech.com",         "00000000003", "11911110003", M, True ),
            ("Carlos",   "Mendes",    date(1975,  5, 20), "masculino", "carlos.mendes@meditech.com",        "00000000004", "11911110004", M, True ),
            ("Fernanda", "Costa",     date(1988, 11, 30), "feminino",  "fernanda.costa@meditech.com",       "00000000005", "11911110005", M, True ),
            ("Roberto",  "Alves",     date(1972,  4, 18), "masculino", "roberto.alves@meditech.com",        "00000000006", "11911110006", M, True ),
            ("Patricia", "Silva",     date(1990,  7, 25), "feminino",  "patricia.silva@meditech.com",       "00000000007", "11911110007", M, True ),
            ("Marcos",   "Santos",    date(1983,  9, 12), "masculino", "marcos.santos@meditech.com",        "00000000008", "11911110008", M, True ),
            ("Luciana",  "Ferreira",  date(1978,  2, 28), "feminino",  "luciana.ferreira@meditech.com",     "00000000009", "11911110009", M, True ),
            ("Eduardo",  "Rocha",     date(1986,  6, 15), "masculino", "eduardo.rocha@meditech.com",        "00000000010", "11911110010", M, True ),
            ("Camila",   "Oliveira",  date(1992, 12,  3), "feminino",  "camila.oliveira@meditech.com",      "00000000011", "11911110011", M, True ),
            # ── Cardiologia (5 ativos) ─────────────────────────────────────────
            ("Henrique", "Souza",     date(1970, 12,  3), "masculino", "henrique.souza@meditech.com",       "00000000012", "11911110012", M, True ),
            ("Marina",   "Barbosa",   date(1983,  7, 17), "feminino",  "marina.barbosa@meditech.com",       "00000000013", "11911110013", M, True ),
            ("Felipe",   "Castro",    date(1977,  3, 22), "masculino", "felipe.castro@meditech.com",        "00000000014", "11911110014", M, True ),
            ("Renata",   "Lima",      date(1985,  1, 14), "feminino",  "renata.lima@meditech.com",          "00000000015", "11911110015", M, True ),
            ("Thiago",   "Nunes",     date(1979,  8, 30), "masculino", "thiago.nunes@meditech.com",         "00000000016", "11911110016", M, True ),
            # ── Dermatologia (5 ativos) ────────────────────────────────────────
            ("Carla",    "Ferreira",  date(1990, 11,  8), "feminino",  "carla.ferreira@meditech.com",       "00000000017", "11911110017", M, True ),
            ("Gabriel",  "Ribeiro",   date(1987,  4, 25), "masculino", "gabriel.ribeiro@meditech.com",      "00000000018", "11911110018", M, True ),
            ("Isabela",  "Martins",   date(1987,  4,  7), "feminino",  "isabela.martins@meditech.com",      "00000000019", "11911110019", M, True ),
            ("Rafael",   "Teixeira",  date(1984,  9, 16), "masculino", "rafael.teixeira@meditech.com",      "00000000020", "11911110020", M, True ),
            ("Juliana",  "Gomes",     date(1993,  2, 19), "feminino",  "juliana.gomes@meditech.com",        "00000000021", "11911110021", M, True ),
            # ── Ortopedia (5 ativos) ───────────────────────────────────────────
            ("Bruno",    "Santos",    date(1978,  7, 22), "masculino", "bruno.santos@meditech.com",         "00000000022", "11911110022", M, True ),
            ("Fernando", "Rocha",     date(1988,  1, 25), "masculino", "fernando.rocha@meditech.com",       "00000000023", "11911110023", M, True ),
            ("Leticia",  "Cardoso",   date(1991,  5, 11), "feminino",  "leticia.cardoso@meditech.com",      "00000000024", "11911110024", M, True ),
            ("Andre",    "Monteiro",  date(1976, 10,  8), "masculino", "andre.monteiro@meditech.com",       "00000000025", "11911110025", M, True ),
            ("Tatiane",  "Correia",   date(1989,  3, 27), "feminino",  "tatiane.correia@meditech.com",      "00000000026", "11911110026", M, True ),
            # ── Pediatria (5 ativos) ───────────────────────────────────────────
            ("Elena",    "Costa",     date(1975,  9, 12), "feminino",  "elena.costa@meditech.com",          "00000000027", "11911110027", M, True ),
            ("Viviane",  "Pereira",   date(1986,  6, 20), "feminino",  "viviane.pereira@meditech.com",      "00000000028", "11911110028", M, True ),
            ("Leonardo", "Freitas",   date(1981, 11, 15), "masculino", "leonardo.freitas@meditech.com",     "00000000029", "11911110029", M, True ),
            ("Sandra",   "Moreira",   date(1974,  8,  7), "feminino",  "sandra.moreira@meditech.com",       "00000000030", "11911110030", M, True ),
            ("Rodrigo",  "Pinto",     date(1992,  4,  3), "masculino", "rodrigo.pinto@meditech.com",        "00000000031", "11911110031", M, True ),
            # ── Neurologia (5 ativos) ──────────────────────────────────────────
            ("Diego",    "Oliveira",  date(1982,  5, 30), "masculino", "diego.oliveira@meditech.com",       "00000000032", "11911110032", M, True ),
            ("Aline",    "Sousa",     date(1988,  9, 21), "feminino",  "aline.sousa@meditech.com",          "00000000033", "11911110033", M, True ),
            ("Marcelo",  "Cunha",     date(1975,  2, 14), "masculino", "marcelo.cunha@meditech.com",        "00000000034", "11911110034", M, True ),
            ("Priscila", "Lopes",     date(1991,  7,  8), "feminino",  "priscila.lopes@meditech.com",       "00000000035", "11911110035", M, True ),
            ("Gustavo",  "Ramos",     date(1979, 12, 25), "masculino", "gustavo.ramos@meditech.com",        "00000000036", "11911110036", M, True ),
            # ── Oftalmologia (5 ativos) ────────────────────────────────────────
            ("Beatriz",  "Araujo",    date(1986,  3, 18), "feminino",  "beatriz.araujo@meditech.com",       "00000000037", "11911110037", M, True ),
            ("Cesar",    "Nogueira",  date(1980, 11,  5), "masculino", "cesar.nogueira@meditech.com",       "00000000038", "11911110038", M, True ),
            ("Daniela",  "Fonseca",   date(1993,  6, 29), "feminino",  "daniela.fonseca@meditech.com",      "00000000039", "11911110039", M, True ),
            ("Emerson",  "Viana",     date(1977,  9, 13), "masculino", "emerson.viana@meditech.com",        "00000000040", "11911110040", M, True ),
            ("Fabiana",  "Azevedo",   date(1984,  1, 22), "feminino",  "fabiana.azevedo@meditech.com",      "00000000041", "11911110041", M, True ),
            # ── Ginecologia (5 ativos) ─────────────────────────────────────────
            ("Gabriela", "Alves",     date(1993,  6, 18), "feminino",  "gabriela.alves@meditech.com",       "00000000042", "11911110042", M, True ),
            ("Helena",   "Braga",     date(1978,  4, 15), "feminino",  "helena.braga@meditech.com",         "00000000043", "11911110043", M, True ),
            ("Igor",     "Campos",    date(1985,  8, 30), "masculino", "igor.campos@meditech.com",          "00000000044", "11911110044", M, True ),
            ("Joana",    "Dias",      date(1990,  2, 11), "feminino",  "joana.dias@meditech.com",           "00000000045", "11911110045", M, True ),
            ("Keila",    "Esteves",   date(1987, 10,  5), "feminino",  "keila.esteves@meditech.com",        "00000000046", "11911110046", M, True ),
            # ── Urologia (5 ativos) ────────────────────────────────────────────
            ("Leandro",  "Faria",     date(1973,  7, 19), "masculino", "leandro.faria@meditech.com",        "00000000047", "11911110047", M, True ),
            ("Milena",   "Galvao",    date(1989, 11, 28), "feminino",  "milena.galvao@meditech.com",        "00000000048", "11911110048", M, True ),
            ("Nathan",   "Henriques", date(1982,  5, 14), "masculino", "nathan.henriques@meditech.com",     "00000000049", "11911110049", M, True ),
            ("Olivia",   "Ribeiro",   date(1989, 11, 14), "feminino",  "olivia.ribeiro@meditech.com",       "00000000050", "11911110050", M, True ),
            ("Pedro",    "Jardim",    date(1976,  3,  7), "masculino", "pedro.jardim@meditech.com",         "00000000051", "11911110051", M, True ),
            # ── Inativos (10) ──────────────────────────────────────────────────
            ("Karine",   "Silva",     date(1995,  2, 20), "feminino",  "karine.silva@meditech.com",         "00000000052", "11922220052", M, False),
            ("Lucas",    "Nunes",     date(1992, 10,  5), "masculino", "lucas.nunes@meditech.com",          "00000000053", "11922220053", M, False),
            ("Nelson",   "Barbosa",   date(1976,  3, 28), "masculino", "nelson.barbosa@meditech.com",       "00000000054", "11922220054", M, False),
            ("Paulo",    "Mendes",    date(1984,  6,  9), "masculino", "paulo.mendes@meditech.com",         "00000000055", "11922220055", M, False),
            ("Rafaela",  "Teixeira",  date(1991,  9, 23), "feminino",  "rafaela.teixeira@meditech.com",     "00000000056", "11922220056", M, False),
            ("Silvia",   "Matos",     date(1988, 12, 17), "feminino",  "silvia.matos@meditech.com",         "00000000057", "11922220057", M, False),
            ("Tiago",    "Carvalho",  date(1981,  4, 26), "masculino", "tiago.carvalho@meditech.com",       "00000000058", "11922220058", M, False),
            ("Ursula",   "Peixoto",   date(1994,  7, 10), "feminino",  "ursula.peixoto@meditech.com",       "00000000059", "11922220059", M, False),
            ("Victor",   "Queiroz",   date(1979,  1, 15), "masculino", "victor.queiroz@meditech.com",       "00000000060", "11922220060", M, False),
            ("Wanda",    "Rezende",   date(1986,  5, 22), "feminino",  "wanda.rezende@meditech.com",        "00000000061", "11922220061", M, False),
        ]
        # fmt: on

        usuarios_inseridos = 0
        usuarios_pulados = 0
        for nome, sobrenome, data_nasc, genero, email, cpf, telefone, tipo, ativo in usuarios:
            if db.session.query(UsuarioModel).filter_by(email=email).first():
                usuarios_pulados += 1
                continue
            db.session.add(UsuarioModel(
                nome=nome, sobrenome=sobrenome, data_nascimento=data_nasc,
                genero=genero, email=email, senha=senha_hash,
                cpf=cpf, telefone=telefone, tipo=tipo, ativo=ativo,
            ))
            usuarios_inseridos += 1
        db.session.commit()

        # ── Especialidades ─────────────────────────────────────────────────────
        CG = "Clínica Geral"
        especialidades_nomes = [
            "Cardiologia", "Dermatologia", "Ortopedia", "Pediatria",
            "Neurologia", "Oftalmologia", "Ginecologia", "Urologia",
            CG, "Psiquiatria",
        ]
        for nome in especialidades_nomes:
            if not db.session.query(EspecialidadeModel).filter_by(nome=nome).first():
                db.session.add(EspecialidadeModel(nome=nome))
        db.session.commit()

        medico_map = {
            u.email: u
            for u in db.session.query(UsuarioModel).filter_by(tipo=M).all()
        }
        espec_map = {e.nome: e for e in db.session.query(EspecialidadeModel).all()}

        # ── Associações médico ↔ especialidade ────────────────────────────────
        associacoes = {
            # Clínica Geral
            "ana.lima@meditech.com":          [CG], "joao.pereira@meditech.com":       [CG],
            "carlos.mendes@meditech.com":     [CG], "fernanda.costa@meditech.com":     [CG],
            "roberto.alves@meditech.com":     [CG], "patricia.silva@meditech.com":     [CG],
            "marcos.santos@meditech.com":     [CG], "luciana.ferreira@meditech.com":   [CG],
            "eduardo.rocha@meditech.com":     [CG], "camila.oliveira@meditech.com":    [CG],
            # Cardiologia
            "henrique.souza@meditech.com":    ["Cardiologia"], "marina.barbosa@meditech.com":  ["Cardiologia"],
            "felipe.castro@meditech.com":     ["Cardiologia"], "renata.lima@meditech.com":     ["Cardiologia"],
            "thiago.nunes@meditech.com":      ["Cardiologia"],
            # Dermatologia
            "carla.ferreira@meditech.com":    ["Dermatologia"], "gabriel.ribeiro@meditech.com": ["Dermatologia"],
            "isabela.martins@meditech.com":   ["Dermatologia"], "rafael.teixeira@meditech.com": ["Dermatologia"],
            "juliana.gomes@meditech.com":     ["Dermatologia"],
            # Ortopedia
            "bruno.santos@meditech.com":      ["Ortopedia"],  "fernando.rocha@meditech.com":  ["Ortopedia"],
            "leticia.cardoso@meditech.com":   ["Ortopedia"],  "andre.monteiro@meditech.com":  ["Ortopedia"],
            "tatiane.correia@meditech.com":   ["Ortopedia"],
            # Pediatria
            "elena.costa@meditech.com":       ["Pediatria"],  "viviane.pereira@meditech.com": ["Pediatria"],
            "leonardo.freitas@meditech.com":  ["Pediatria"],  "sandra.moreira@meditech.com":  ["Pediatria"],
            "rodrigo.pinto@meditech.com":     ["Pediatria"],
            # Neurologia
            "diego.oliveira@meditech.com":    ["Neurologia"], "aline.sousa@meditech.com":     ["Neurologia"],
            "marcelo.cunha@meditech.com":     ["Neurologia"], "priscila.lopes@meditech.com":  ["Neurologia"],
            "gustavo.ramos@meditech.com":     ["Neurologia"],
            # Oftalmologia
            "beatriz.araujo@meditech.com":    ["Oftalmologia"], "cesar.nogueira@meditech.com":  ["Oftalmologia"],
            "daniela.fonseca@meditech.com":   ["Oftalmologia"], "emerson.viana@meditech.com":   ["Oftalmologia"],
            "fabiana.azevedo@meditech.com":   ["Oftalmologia"],
            # Ginecologia
            "gabriela.alves@meditech.com":    ["Ginecologia"], "helena.braga@meditech.com":    ["Ginecologia"],
            "igor.campos@meditech.com":       ["Ginecologia"], "joana.dias@meditech.com":      ["Ginecologia"],
            "keila.esteves@meditech.com":     ["Ginecologia"],
            # Urologia
            "leandro.faria@meditech.com":     ["Urologia"],   "milena.galvao@meditech.com":   ["Urologia"],
            "nathan.henriques@meditech.com":  ["Urologia"],   "olivia.ribeiro@meditech.com":  ["Urologia"],
            "pedro.jardim@meditech.com":      ["Urologia"],
            # Inativos
            "karine.silva@meditech.com":      ["Psiquiatria"], "lucas.nunes@meditech.com":     ["Psiquiatria"],
            "nelson.barbosa@meditech.com":    ["Ortopedia"],   "paulo.mendes@meditech.com":    ["Neurologia"],
            "rafaela.teixeira@meditech.com":  [CG],            "silvia.matos@meditech.com":    ["Dermatologia"],
            "tiago.carvalho@meditech.com":    ["Cardiologia"], "ursula.peixoto@meditech.com":  ["Pediatria"],
            "victor.queiroz@meditech.com":    ["Oftalmologia"],"wanda.rezende@meditech.com":   ["Ginecologia"],
        }
        for email, especialidades in associacoes.items():
            medico = medico_map.get(email)
            if not medico:
                continue
            for nome_espec in especialidades:
                espec = espec_map.get(nome_espec)
                if espec and espec not in medico.especialidades:
                    medico.especialidades.append(espec)
        db.session.commit()

        # ── Horários disponíveis (apenas médicos ativos) ───────────────────────
        # 8 padrões rotacionados pelos 50 médicos ativos (idx % 8)
        _PADROES = [
            [(0, "manha"), (2, "manha"), (4, "manha")],
            [(1, "tarde"), (3, "tarde")],
            [(0, "tarde"), (2, "tarde"), (4, "tarde")],
            [(1, "manha"), (3, "manha"), (5, "manha")],
            [(0, "manha"), (1, "tarde"), (3, "manha"), (4, "tarde")],
            [(2, "noite"), (3, "noite"), (4, "noite")],
            [(0, "manha"), (2, "tarde"), (4, "manha"), (1, "noite")],
            [(1, "manha"), (3, "tarde"), (5, "manha")],
        ]
        ativos = [u for u in usuarios if u[8] is True and u[7] == M]
        for idx, dado in enumerate(ativos):
            email = dado[4]
            medico = medico_map.get(email)
            if not medico:
                continue
            nomes_espec = associacoes.get(email, [])
            if not nomes_espec:
                continue
            espec = espec_map.get(nomes_espec[0])
            if not espec:
                continue
            for dia, periodo in _PADROES[idx % len(_PADROES)]:
                existe = db.session.query(HorarioDisponivelModel).filter_by(
                    medico_id=medico.id, especialidade_id=espec.id, dia_semana=dia, periodo=periodo
                ).first()
                if not existe:
                    db.session.add(HorarioDisponivelModel(
                        medico_id=medico.id, especialidade_id=espec.id, dia_semana=dia, periodo=periodo
                    ))
        db.session.commit()

        click.echo(f"\nCarga inicial concluída:")
        click.echo(f"  Usuários:       {usuarios_inseridos} inserido(s), {usuarios_pulados} ignorado(s)")
        click.echo(f"  Especialidades: {len(especialidades_nomes)} garantidas")
        click.echo(f"  Associações e horários: inseridos/atualizados")
        click.echo(f"  Senha padrão:   {senha}")
