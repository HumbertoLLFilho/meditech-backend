from src.domain.contracts.password_service_contract import PasswordServiceContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.usecases.login_usuario.login_usuario_input import LoginUsuarioInput


class LoginUsuarioUseCase:

    def __init__(self, repository: UsuarioRepositoryContract, password_service: PasswordServiceContract):
        self.repository = repository
        self.password_service = password_service

    def executar(self, input_data: LoginUsuarioInput) -> dict:
        usuario = self.repository.buscar_por_email(input_data.email)

        if not usuario or not self.password_service.verify(input_data.senha, usuario.senha):
            raise ValueError("E-mail ou senha invalidos.")

        return {
            "id": usuario.id,
            "email": usuario.email,
            "cpf": usuario.cpf,
            "nome": f"{usuario.nome} {usuario.sobrenome}",
        }
