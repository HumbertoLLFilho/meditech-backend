from src.infrastructure.database import db


class ConsultaModel(db.Model):
    __tablename__ = "consulta"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    especialidade = db.Column(db.String(150), nullable=False)
    medico = db.Column(db.String(150), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(30), nullable=False)
