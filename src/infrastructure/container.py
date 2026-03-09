from src.adapters.repositories.usuario_repository import UsuarioRepository
from src.usecases.cadastrar_usuario_usecase import CadastrarUsuarioUseCase
from src.usecases.login_usuario_usecase import LoginUsuarioUseCase


def get_cadastrar_usuario_use_case() -> CadastrarUsuarioUseCase:
    repository = UsuarioRepository()
    return CadastrarUsuarioUseCase(repository)


def get_login_usuario_use_case() -> LoginUsuarioUseCase:
    repository = UsuarioRepository()
    return LoginUsuarioUseCase(repository)
