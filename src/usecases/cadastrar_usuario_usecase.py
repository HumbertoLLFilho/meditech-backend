from werkzeug.security import generate_password_hash

from src.adapters.controllers.usuario_request import CadastrarUsuarioRequest
from src.application.usuario_repository_port import UsuarioRepositoryPort
from src.domain.documento import Documento, TipoDocumento
from src.domain.usuario import Genero, TipoUsuario, Usuario


class CadastrarUsuarioUseCase:

    def __init__(self, repository: UsuarioRepositoryPort):
        self.repository = repository

    def executar(self, request: CadastrarUsuarioRequest) -> Usuario:
        if self.repository.buscar_por_email(request.email):
            raise ValueError("E-mail já cadastrado.")

        for doc_request in request.documentos:
            if self.repository.buscar_por_documento(doc_request.tipo, doc_request.numero):
                raise ValueError(f"Documento {doc_request.tipo.upper()} '{doc_request.numero}' já cadastrado.")

        try:
            genero_enum = Genero(request.genero)
        except ValueError:
            valores = [g.value for g in Genero]
            raise ValueError(f"Gênero inválido. Valores aceitos: {valores}")

        try:
            tipo_enum = TipoUsuario(request.tipo)
        except ValueError:
            valores = [t.value for t in TipoUsuario]
            raise ValueError(f"Tipo de usuário inválido. Valores aceitos: {valores}")

        documentos = []
        for doc_request in request.documentos:
            try:
                tipo_doc_enum = TipoDocumento(doc_request.tipo)
            except ValueError:
                valores = [t.value for t in TipoDocumento]
                raise ValueError(f"Tipo de documento inválido: '{doc_request.tipo}'. Valores aceitos: {valores}")
            
            documentos.append(Documento(
                tipo=tipo_doc_enum,
                numero=doc_request.numero,
            ))

        # Hash da senha
        senha_hash = generate_password_hash(request.senha)

        usuario = Usuario(
            nome=request.nome,
            sobrenome=request.sobrenome,
            data_nascimento=request.data_nascimento,
            genero=genero_enum,
            email=request.email,
            senha=senha_hash,
            tipo=tipo_enum,
            documentos=documentos,
        )

        return self.repository.salvar(usuario)
