from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import StatusAprovacao
from src.usecases.usuarios.alterar_status_usuario.alterar_status_usuario_input import AlterarStatusUsuarioInput


class AlterarStatusUsuarioUseCase:
    def __init__(self, usuario_repository: UsuarioRepositoryContract):
        self.usuario_repository = usuario_repository

    def executar(self, input_data: AlterarStatusUsuarioInput) -> dict:
        usuario = self.usuario_repository.buscar_por_id(input_data.usuario_id)
        if not usuario:
            raise ValueError("Usuario nao encontrado")

        usuario.status_aprovacao = input_data.status_aprovacao
        usuario.ativo = (input_data.status_aprovacao == StatusAprovacao.APROVADO)
        self.usuario_repository.atualizar(usuario)

        return {
            "mensagem": "Status do usuario alterado com sucesso",
            "usuario_id": usuario.id,
            "status_aprovacao": usuario.status_aprovacao.value,
            "ativo": usuario.ativo,
        }
