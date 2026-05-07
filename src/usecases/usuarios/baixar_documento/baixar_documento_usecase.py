from src.domain.contracts.documento_repository_contract import DocumentoRepositoryContract
from src.domain.models.usuario import TipoUsuario
from src.usecases.usuarios.baixar_documento.baixar_documento_input import BaixarDocumentoInput


class BaixarDocumentoUseCase:

    def __init__(self, documento_repository: DocumentoRepositoryContract):
        self.documento_repository = documento_repository

    def executar(self, input_data: BaixarDocumentoInput) -> dict:
        documento = self.documento_repository.buscar_por_id(input_data.documento_id)

        if not documento:
            raise ValueError("Documento nao encontrado.")

        eh_admin = input_data.tipo_solicitante == TipoUsuario.ADMIN.value
        eh_dono = documento.usuario_id == input_data.usuario_id

        if not eh_admin and not eh_dono:
            raise PermissionError("Voce nao tem permissao para baixar este documento.")

        return {
            "conteudo": documento.conteudo,
            "mime_type": documento.mime_type,
            "nome_arquivo": documento.nome_arquivo,
        }
