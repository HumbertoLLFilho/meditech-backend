from src.adapters.repositories.consulta_repository import ConsultaRepository
from src.adapters.repositories.usuario_repository import UsuarioRepository
from src.usecases.cadastrar_consulta_usecase import CadastrarConsultaUseCase
from src.usecases.cadastrar_usuario_usecase import CadastrarUsuarioUseCase
from src.usecases.listar_consultas_usecase import ListarConsultaUseCase
from src.usecases.login_usuario_usecase import LoginUsuarioUseCase


def get_cadastrar_usuario_use_case() -> CadastrarUsuarioUseCase:
    repository = UsuarioRepository()
    return CadastrarUsuarioUseCase(repository)

def get_login_usuario_use_case() -> LoginUsuarioUseCase:
    repository = UsuarioRepository()
    return LoginUsuarioUseCase(repository)

def get_cadastrar_consulta_use_case() -> CadastrarConsultaUseCase:
    repository = ConsultaRepository()
    return CadastrarConsultaUseCase(repository)

def get_listar_consultas() -> ListarConsultaUseCase:
    repository = ConsultaRepository()
    return ListarConsultaUseCase(repository)