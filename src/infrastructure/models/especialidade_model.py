from src.infrastructure.config.database import db


medico_especialidades = db.Table(
    "medico_especialidades",
    db.Column("medico_id", db.Integer, db.ForeignKey("usuarios.id"), primary_key=True),
    db.Column("especialidade_id", db.Integer, db.ForeignKey("especialidades.id"), primary_key=True),
)


class EspecialidadeModel(db.Model):
    __tablename__ = "especialidades"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)

    medicos = db.relationship(
        "UsuarioModel",
        secondary=medico_especialidades,
        backref="especialidades",
    )
