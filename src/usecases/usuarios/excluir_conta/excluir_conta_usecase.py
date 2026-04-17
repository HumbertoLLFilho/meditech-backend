from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import TipoUsuario
from src.usecases.usuarios.excluir_conta.excluir_conta_input import ExcluirContaInput


class ExcluirContaUseCase:

    def __init__(self, usuario_repository: UsuarioRepositoryContract):
        self.usuario_repository = usuario_repository

    def executar(self, input_data: ExcluirContaInput, id_logado: int, tipo_logado: str) -> dict:
        usuario = self.usuario_repository.buscar_por_id(input_data.usuario_id)
        if not usuario:
            raise ValueError("Usuario nao encontrado.")

        is_admin = tipo_logado == TipoUsuario.ADMIN.value
        is_proprio = id_logado == input_data.usuario_id

        if not is_admin and not is_proprio:
            raise PermissionError("Acesso negado.")

        if is_admin and is_proprio:
            raise ValueError("Admin nao pode excluir a propria conta.")

        self.usuario_repository.excluir(input_data.usuario_id)

        return {"mensagem": "Conta excluida com sucesso."}
