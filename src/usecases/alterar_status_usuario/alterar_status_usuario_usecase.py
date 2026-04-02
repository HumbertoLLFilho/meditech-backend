from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.usecases.alterar_status_usuario.alterar_status_usuario_input import AlterarStatusUsuarioInput


class AlterarStatusUsuarioUseCase:
    def __init__(self, usuario_repository: UsuarioRepositoryContract):
        self.usuario_repository = usuario_repository

    def executar(self, input_data: AlterarStatusUsuarioInput) -> dict:
        # Verificar se o usuario existe
        usuario = self.usuario_repository.buscar_por_id(input_data.usuario_id)
        if not usuario:
            raise ValueError("Usuario nao encontrado")

        # Alterar o status
        usuario.ativo = input_data.ativo
        self.usuario_repository.atualizar(usuario)

        return {"mensagem": "Status do usuario alterado com sucesso", "usuario_id": usuario.id, "ativo": usuario.ativo}