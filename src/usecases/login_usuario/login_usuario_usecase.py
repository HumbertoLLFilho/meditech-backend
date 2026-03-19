from werkzeug.security import check_password_hash
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.usecases.login_usuario.login_usuario_input import LoginUsuarioInput


class LoginUsuarioUseCase:

    def __init__(self, repository: UsuarioRepositoryContract):
        self.repository = repository

    def executar(self, input_data: LoginUsuarioInput) -> dict:
        usuario = self.repository.buscar_por_email(input_data.email)

        if not usuario or not check_password_hash(usuario.senha, input_data.senha):
            raise ValueError("E-mail ou senha invalidos.")

        return {
            "id": usuario.id,
            "email": usuario.email,
            "cpf": usuario.cpf,
            "nome": f"{usuario.nome} {usuario.sobrenome}",
        }
