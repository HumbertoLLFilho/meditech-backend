from src.infrastructure.config.database import db


class HorarioDisponivelModel(db.Model):
    __tablename__ = "horarios_disponiveis"
    __table_args__ = (
        db.UniqueConstraint("medico_id", "especialidade_id", "dia_semana", "periodo", name="uq_medico_esp_dia_periodo"),
    )

    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    especialidade_id = db.Column(db.Integer, db.ForeignKey("especialidades.id"), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)
    periodo = db.Column(db.String(10), nullable=False)
