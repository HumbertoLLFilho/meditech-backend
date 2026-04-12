from src.domain.contracts.documento_repository_contract import DocumentoRepositoryContract
from src.domain.models.documento import Documento, TipoDocumento
from src.infrastructure.config.database import db
from src.infrastructure.models.documento_model import DocumentoModel



class DocumentoRepository(DocumentoRepositoryContract):

    @staticmethod
    def _to_domain(model: DocumentoModel) -> Documento:
        return Documento(
            id=model.id,
            usuario_id=model.usuario_id,
            tipo=TipoDocumento(model.tipo),
            nome_arquivo=model.nome_arquivo,
            mime_type=model.mime_type,
            conteudo=model.conteudo,
        )

    def salvar(self, documento: Documento) -> Documento:
        model = DocumentoModel(
            usuario_id=documento.usuario_id,
            tipo=documento.tipo.value if hasattr(documento.tipo, 'value') else documento.tipo,
            nome_arquivo=documento.nome_arquivo,
            mime_type=documento.mime_type,
            conteudo=documento.conteudo,
        )

        db.session.add(model)
        db.session.flush()  # Para obter o ID antes de commitar
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return self._to_domain(model)

    def buscar_por_id(self, documento_id: int) -> Documento | None:
        model = DocumentoModel.query.get(documento_id)
        if not model:
            return None
        return self._to_domain(model)

    def listar_por_usuario_id(self, usuario_id: int) -> list[Documento]:
        modelos = DocumentoModel.query.filter_by(usuario_id=usuario_id).all()
        return [self._to_domain(model) for model in modelos]

    def listar_por_usuario(self, usuario_id: int) -> list[Documento]:
        return self.listar_por_usuario_id(usuario_id)

    def buscar_por_usuario_e_tipo(self, usuario_id: int, tipo: str) -> Documento | None:
        models = DocumentoModel.query.filter_by(usuario_id=usuario_id, tipo=tipo).first()
        if not models:
            return None
        return self._to_domain(models)
