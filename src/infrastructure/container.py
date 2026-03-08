from src.adapters.repoositories.usuario_repository import UsuarioRepository
from src.usecases.cadastrar_usuario_usecase import CadastrarUsuarioUseCase


def get_cadastrar_usuario_use_case() -> CadastrarUsuarioUseCase:
    repository = UsuarioRepository()
    return CadastrarUsuarioUseCase(repository)
