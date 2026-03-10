from src.application.usuario_repository_port import UsuarioRepositoryPort
from src.domain.documento import Documento, TipoDocumento
from src.domain.usuario import Genero, TipoUsuario, Usuario
from src.infrastructure.database import db
from src.infrastructure.documento_model import DocumentoModel
from src.infrastructure.usuario_model import UsuarioModel


class UsuarioRepository(UsuarioRepositoryPort):

    def salvar(self, usuario: Usuario) -> Usuario:
        # Criar o modelo de usuário
        model = UsuarioModel(
            nome=usuario.nome,
            sobrenome=usuario.sobrenome,
            data_nascimento=usuario.data_nascimento,
            genero=usuario.genero.value,
            email=usuario.email,
            senha=usuario.senha,
            tipo=usuario.tipo.value,
        )
        db.session.add(model)
        db.session.flush()  # Para obter o ID antes de commitar

        # Adicionar documentos
        for doc in usuario.documentos:
            doc_model = DocumentoModel(
                usuario_id=model.id,
                tipo=doc.tipo.value,
                numero=doc.numero,
            )
            db.session.add(doc_model)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        usuario.id = model.id

        # Atualizar IDs dos documentos por tipo e número para garantir correspondência correta
        doc_map = {(doc.tipo, doc.numero): doc for doc in model.documentos}
        for doc in usuario.documentos:
            doc_model = doc_map.get((doc.tipo.value, doc.numero))
            if doc_model:
                doc.id = doc_model.id
                doc.usuario_id = model.id

        return usuario

    def buscar_por_email(self, email: str) -> Usuario | None:
        model = UsuarioModel.query.filter_by(email=email).first()
        return self._para_dominio(model) if model else None

    def buscar_por_documento(self, tipo: str, numero: str) -> Usuario | None:
        """Busca usuário por tipo e número de documento"""
        doc_model = DocumentoModel.query.filter_by(tipo=tipo, numero=numero).first()
        if not doc_model:
            return None
        return self._para_dominio(doc_model.usuario)

    def _para_dominio(self, model: UsuarioModel) -> Usuario:
        # Converter documentos
        documentos = [
            Documento(
                id=doc.id,
                usuario_id=doc.usuario_id,
                tipo=TipoDocumento(doc.tipo),
                numero=doc.numero,
            )
            for doc in model.documentos
        ]

        return Usuario(
            id=model.id,
            nome=model.nome,
            sobrenome=model.sobrenome,
            data_nascimento=model.data_nascimento,
            genero=Genero(model.genero),
            email=model.email,
            senha=model.senha,
            tipo=TipoUsuario(model.tipo),
            documentos=documentos,
        )
