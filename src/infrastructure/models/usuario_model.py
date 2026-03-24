from datetime import datetime

from src.infrastructure.config.database import db


class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    tipo = db.Column(db.String(30), nullable=False)
    ativo = db.Column(db.Boolean, default=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    consultas_paciente = db.relationship(
        "ConsultaModel",
        foreign_keys="ConsultaModel.paciente_id",
        backref="paciente",
    )
    consultas_medico = db.relationship(
        "ConsultaModel",
        foreign_keys="ConsultaModel.medico_id",
        backref="medico",
    )
    horarios_disponiveis = db.relationship(
        "HorarioDisponivelModel",
        foreign_keys="HorarioDisponivelModel.medico_id",
        backref="medico_horarios",
    )