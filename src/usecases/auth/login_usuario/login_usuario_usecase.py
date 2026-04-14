from src.domain.contracts.password_service_contract import PasswordServiceContract
from src.domain.contracts.token_service_contract import TokenServiceContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.usecases.auth.login_usuario.login_usuario_input import LoginUsuarioInput


class InvalidCredentialsError(Exception):
    pass


class LoginUsuarioUseCase:

    def __init__(
        self,
        repository: UsuarioRepositoryContract,
        password_service: PasswordServiceContract,
        token_service: TokenServiceContract,
    ):
        self.repository = repository
        self.password_service = password_service
        self.token_service = token_service

    def executar(self, input_data: LoginUsuarioInput) -> dict:
        usuario = self.repository.buscar_por_email(input_data.email)

        if not usuario or not self.password_service.verify(input_data.senha, usuario.senha):
            raise InvalidCredentialsError("E-mail ou senha invalidos.")

        if not usuario.ativo:
            raise InvalidCredentialsError("Conta inativa. Entre em contato com o administrador.")

        nome_completo = f"{usuario.nome} {usuario.sobrenome}"
        token = self.token_service.generate_access_token(usuario)

        return {
            "access_token": token,
        }
