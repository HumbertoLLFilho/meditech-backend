from src.domain.contracts.documento_repository_contract import DocumentoRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.documento import Documento
from src.domain.models.usuario import TipoUsuario
from src.usecases.usuarios.upload_documento.upload_documento_input import UploadDocumentoInput


class UploadDocumentoUseCase:

    def __init__(
        self,
        documento_repository: DocumentoRepositoryContract,
        usuario_repository: UsuarioRepositoryContract,
    ):
        self.documento_repository = documento_repository
        self.usuario_repository = usuario_repository

    def executar(self, input_data: UploadDocumentoInput, id_logado: int, tipo_logado: str) -> dict:
        is_admin = tipo_logado == TipoUsuario.ADMIN.value
        is_proprio = id_logado == input_data.usuario_id

        if not is_admin and not is_proprio:
            raise PermissionError("Acesso negado.")

        usuario = self.usuario_repository.buscar_por_id(input_data.usuario_id)
        if not usuario:
            raise ValueError("Usuario nao encontrado.")

        existente = self.documento_repository.buscar_por_usuario_e_tipo(
            input_data.usuario_id, input_data.tipo.value
        )
        if existente:
            self.documento_repository.deletar(existente.id)

        documento = Documento(
            usuario_id=input_data.usuario_id,
            tipo=input_data.tipo,
            nome_arquivo=input_data.nome_arquivo,
            mime_type=input_data.mime_type,
            conteudo=input_data.conteudo,
        )
        salvo = self.documento_repository.salvar(documento)

        return {
            "id": salvo.id,
            "tipo": salvo.tipo.value,
            "nome_arquivo": salvo.nome_arquivo,
            "usuario_id": salvo.usuario_id,
        }
