from datetime import datetime

from src.infrastructure.config.database import db


class ConsultaModel(db.Model):
    __tablename__ = "consulta"

    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    data_agendada = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(30), nullable=False)
    especialidade_id = db.Column(db.Integer, db.ForeignKey("especialidades.id"), nullable=False)
    data_cadastrada = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    cancelada = db.Column(db.Boolean, default=False, nullable=False)
