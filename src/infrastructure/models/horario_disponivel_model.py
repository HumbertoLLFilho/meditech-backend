from src.infrastructure.config.database import db


class HorarioDisponivelModel(db.Model):
    __tablename__ = "horarios_disponiveis"
    __table_args__ = (
        db.UniqueConstraint("medico_id", "dia_semana", "hora", name="uq_medico_dia_hora"),
    )

    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)
    hora = db.Column(db.String(5), nullable=False)
