from flask import g, has_request_context

from src.infrastructure.services.password_service import PasswordService
from src.repositories.consulta_repository import ConsultaRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.usecases.cadastrar_consulta.cadastrar_consulta_usecase import CadastrarConsultaUseCase
from src.usecases.cadastrar_usuario.cadastrar_usuario_usecase import CadastrarUsuarioUseCase
from src.usecases.listar_consultas.listar_consultas_usecase import ListarConsultaUseCase
from src.usecases.login_usuario.login_usuario_usecase import LoginUsuarioUseCase


def _get_request_cache() -> dict:
    """Mantem instancias no escopo da requisicao atual."""
    if not has_request_context():
        return {}

    cache = getattr(g, "_container_cache", None)
    if cache is None:
        cache = {}
        g._container_cache = cache
    return cache


def _scoped(key: str, factory):
    cache = _get_request_cache()
    if key not in cache:
        cache[key] = factory()
    return cache[key]


def _get_usuario_repository() -> UsuarioRepository:
    return _scoped("usuario_repository", UsuarioRepository)


def _get_consulta_repository() -> ConsultaRepository:
    return _scoped("consulta_repository", ConsultaRepository)


def _get_password_service() -> PasswordService:
    return _scoped("password_service", PasswordService)


def get_cadastrar_usuario_use_case() -> CadastrarUsuarioUseCase:
    return _scoped(
        "cadastrar_usuario_use_case",
        lambda: CadastrarUsuarioUseCase(_get_usuario_repository(), _get_password_service()),
    )


def get_login_usuario_use_case() -> LoginUsuarioUseCase:
    return _scoped(
        "login_usuario_use_case",
        lambda: LoginUsuarioUseCase(_get_usuario_repository(), _get_password_service()),
    )


def get_cadastrar_consulta_use_case() -> CadastrarConsultaUseCase:
    return _scoped(
        "cadastrar_consulta_use_case",
        lambda: CadastrarConsultaUseCase(_get_consulta_repository()),
    )


def get_listar_consultas() -> ListarConsultaUseCase:
    return _scoped(
        "listar_consultas_use_case",
        lambda: ListarConsultaUseCase(_get_consulta_repository()),
    )