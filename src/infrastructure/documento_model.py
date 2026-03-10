from src.infrastructure.database import db


class DocumentoModel(db.Model):
    __tablename__ = "documentos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    numero = db.Column(db.String(50), nullable=False)

    # Index para garantir unicidade de documentos
    __table_args__ = (
        db.UniqueConstraint('tipo', 'numero', name='uq_documento_tipo_numero'),
    )
