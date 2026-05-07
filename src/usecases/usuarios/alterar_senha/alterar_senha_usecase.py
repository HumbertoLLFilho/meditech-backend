from src.domain.contracts.password_service_contract import PasswordServiceContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import TipoUsuario
from src.usecases.usuarios.alterar_senha.alterar_senha_input import AlterarSenhaInput


class AlterarSenhaUseCase:

    def __init__(
        self,
        usuario_repository: UsuarioRepositoryContract,
        password_service: PasswordServiceContract,
    ):
        self.usuario_repository = usuario_repository
        self.password_service = password_service

    def executar(self, input_data: AlterarSenhaInput, id_logado: int, tipo_logado: str) -> dict:
        usuario = self.usuario_repository.buscar_por_id(input_data.usuario_id)
        if not usuario:
            raise ValueError("Usuario nao encontrado.")

        is_admin = tipo_logado == TipoUsuario.ADMIN.value
        is_proprio = id_logado == input_data.usuario_id

        if not is_admin and not is_proprio:
            raise PermissionError("Acesso negado.")

        if not is_admin:
            if not input_data.senha_atual:
                raise ValueError("Campo obrigatorio ausente: senha_atual")
            if not self.password_service.verify(input_data.senha_atual, usuario.senha):
                raise ValueError("Senha atual incorreta.")

        nova_hash = self.password_service.hash(input_data.nova_senha)
        self.usuario_repository.atualizar_senha(input_data.usuario_id, nova_hash)

        return {"mensagem": "Senha alterada com sucesso."}
