from src.infrastructure.config.database import db

class DocumentoModel(db.Model):
    __tablename__ = "documentos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo = db.Column(db.String(30), nullable=False)
    nome_arquivo = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    conteudo = db.Column(db.LargeBinary, nullable=False)

    # Index para garantir unicidade de documentos
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'tipo', name='uq_documento_usuario_tipo'),
    )
