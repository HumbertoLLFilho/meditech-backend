from src.infrastructure.database import db


class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default="paciente")

    # Relacionamento com documentos
    documentos = db.relationship('DocumentoModel', backref='usuario', lazy=True, cascade='all, delete-orphan')
