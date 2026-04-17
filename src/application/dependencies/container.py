from flask import g, has_request_context

from src.infrastructure.services.jwt_token_service import JwtTokenService
from src.infrastructure.services.password_service import PasswordService
from src.repositories.consulta_repository import ConsultaRepository
from src.repositories.documento_repository import DocumentoRepository
from src.repositories.especialidade_repository import EspecialidadeRepository
from src.repositories.horario_disponivel_repository import HorarioDisponivelRepository
from src.repositories.usuario_repository import UsuarioRepository
from src.usecases.consultas.cancelar_consulta.cancelar_consulta_usecase import CancelarConsultaUseCase
from src.usecases.horarios.adicionar_horario_disponivel.adicionar_horario_disponivel_usecase import AdicionarHorarioDisponivelUseCase
from src.usecases.usuarios.alterar_status_usuario.alterar_status_usuario_usecase import AlterarStatusUsuarioUseCase
from src.usecases.especialidades.associar_especialidade_medico.associar_especialidade_medico_usecase import AssociarEspecialidadeMedicoUseCase
from src.usecases.consultas.cadastrar_consulta.cadastrar_consulta_usecase import CadastrarConsultaUseCase
from src.usecases.horarios.consultar_disponibilidade.consultar_disponibilidade_usecase import ConsultarDisponibilidadeUseCase
from src.usecases.horarios.listar_horarios_disponivel_medico.listar_horarios_disponivel_medico_usecase import ListarHorariosDisponivelMedicoUseCase
from src.usecases.especialidades.cadastrar_especialidade.cadastrar_especialidade_usecase import CadastrarEspecialidadeUseCase
from src.usecases.usuarios.cadastrar_usuario.cadastrar_usuario_usecase import CadastrarUsuarioUseCase
from src.usecases.consultas.listar_consultas.listar_consultas_usecase import ListarConsultaUseCase
from src.usecases.especialidades.listar_especialidades.listar_especialidades_usecase import ListarEspecialidadesUseCase
from src.usecases.especialidades.listar_especialidades_medico.listar_especialidades_medico_usecase import ListarEspecialidadesMedicoUseCase
from src.usecases.usuarios.listar_usuarios.listar_usuarios_usecase import ListarUsuariosUseCase
from src.usecases.usuarios.buscar_usuario.buscar_usuario_usecase import BuscarUsuarioUseCase
from src.usecases.usuarios.baixar_documento.baixar_documento_usecase import BaixarDocumentoUseCase
from src.usecases.usuarios.editar_usuario.editar_usuario_usecase import EditarUsuarioUseCase
from src.usecases.auth.login_usuario.login_usuario_usecase import LoginUsuarioUseCase
from src.usecases.usuarios.alterar_senha.alterar_senha_usecase import AlterarSenhaUseCase
from src.usecases.usuarios.excluir_conta.excluir_conta_usecase import ExcluirContaUseCase
from src.usecases.usuarios.upload_documento.upload_documento_usecase import UploadDocumentoUseCase
from src.usecases.especialidades.desassociar_especialidade_medico.desassociar_especialidade_medico_usecase import DesassociarEspecialidadeMedicoUseCase


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


def _get_especialidade_repository() -> EspecialidadeRepository:
    return _scoped("especialidade_repository", EspecialidadeRepository)


def _get_horario_disponivel_repository() -> HorarioDisponivelRepository:
    return _scoped("horario_disponivel_repository", HorarioDisponivelRepository)


def get_horario_disponivel_repository() -> HorarioDisponivelRepository:
    return _get_horario_disponivel_repository()


def _get_password_service() -> PasswordService:
    return _scoped("password_service", PasswordService)


def _get_token_service() -> JwtTokenService:
    return _scoped("token_service", JwtTokenService)

def _get_documento_repository() -> DocumentoRepository:
    return _scoped("documento_repository", DocumentoRepository)


def get_cadastrar_usuario_use_case() -> CadastrarUsuarioUseCase:
    return _scoped(
        "cadastrar_usuario_use_case",
        lambda: CadastrarUsuarioUseCase(
            _get_usuario_repository(),
            _get_password_service(),
            _get_documento_repository(),
            _get_especialidade_repository(),
        ),
    )


def get_login_usuario_use_case() -> LoginUsuarioUseCase:
    return _scoped(
        "login_usuario_use_case",
        lambda: LoginUsuarioUseCase(
            _get_usuario_repository(),
            _get_password_service(),
            _get_token_service(),
        ),
    )


def get_cadastrar_consulta_use_case() -> CadastrarConsultaUseCase:
    return _scoped(
        "cadastrar_consulta_use_case",
        lambda: CadastrarConsultaUseCase(
            _get_consulta_repository(),
            _get_especialidade_repository(),
            _get_horario_disponivel_repository(),
        ),
    )


def get_listar_usuarios() -> ListarUsuariosUseCase:
    return _scoped(
        "listar_usuarios_use_case",
        lambda: ListarUsuariosUseCase(_get_usuario_repository()),
    )


def get_cancelar_consulta() -> CancelarConsultaUseCase:
    return _scoped(
        "cancelar_consulta_use_case",
        lambda: CancelarConsultaUseCase(_get_consulta_repository()),
    )


def get_listar_consultas() -> ListarConsultaUseCase:
    return _scoped(
        "listar_consultas_use_case",
        lambda: ListarConsultaUseCase(_get_consulta_repository()),
    )


def get_cadastrar_especialidade() -> CadastrarEspecialidadeUseCase:
    return _scoped(
        "cadastrar_especialidade_use_case",
        lambda: CadastrarEspecialidadeUseCase(_get_especialidade_repository()),
    )


def get_listar_especialidades() -> ListarEspecialidadesUseCase:
    return _scoped(
        "listar_especialidades_use_case",
        lambda: ListarEspecialidadesUseCase(_get_especialidade_repository()),
    )


def get_listar_especialidades_medico() -> ListarEspecialidadesMedicoUseCase:
    return _scoped(
        "listar_especialidades_medico_use_case",
        lambda: ListarEspecialidadesMedicoUseCase(_get_especialidade_repository()),
    )


def get_adicionar_horario_disponivel() -> AdicionarHorarioDisponivelUseCase:
    return _scoped(
        "adicionar_horario_disponivel_use_case",
        lambda: AdicionarHorarioDisponivelUseCase(
            _get_horario_disponivel_repository(),
            _get_usuario_repository(),
            _get_especialidade_repository(),
        ),
    )


def get_listar_horarios_disponivel_medico() -> ListarHorariosDisponivelMedicoUseCase:
    return _scoped(
        "listar_horarios_disponivel_medico_use_case",
        lambda: ListarHorariosDisponivelMedicoUseCase(_get_horario_disponivel_repository()),
    )


def get_consultar_disponibilidade() -> ConsultarDisponibilidadeUseCase:
    return _scoped(
        "consultar_disponibilidade_use_case",
        lambda: ConsultarDisponibilidadeUseCase(
            _get_horario_disponivel_repository(),
            _get_consulta_repository(),
        ),
    )


def get_buscar_usuario() -> BuscarUsuarioUseCase:
    return _scoped(
        "buscar_usuario_use_case",
        lambda: BuscarUsuarioUseCase(_get_usuario_repository()),
    )


def get_associar_especialidade_medico() -> AssociarEspecialidadeMedicoUseCase:
    return _scoped(
        "associar_especialidade_medico_use_case",
        lambda: AssociarEspecialidadeMedicoUseCase(
            _get_especialidade_repository(),
            _get_usuario_repository(),
        ),
    )

def get_alterar_status_usuario_use_case() -> AlterarStatusUsuarioUseCase:
    return _scoped(
        "alterar_status_usuario_use_case",
        lambda: AlterarStatusUsuarioUseCase(_get_usuario_repository()),
    )


def get_baixar_documento() -> BaixarDocumentoUseCase:
    return _scoped(
        "baixar_documento_use_case",
        lambda: BaixarDocumentoUseCase(_get_documento_repository()),
    )


def get_editar_usuario() -> EditarUsuarioUseCase:
    return _scoped(
        "editar_usuario_use_case",
        lambda: EditarUsuarioUseCase(
            _get_usuario_repository(),
            _get_especialidade_repository(),
        ),
    )


def get_alterar_senha_use_case() -> AlterarSenhaUseCase:
    return _scoped(
        "alterar_senha_use_case",
        lambda: AlterarSenhaUseCase(
            _get_usuario_repository(),
            _get_password_service(),
        ),
    )


def get_excluir_conta_use_case() -> ExcluirContaUseCase:
    return _scoped(
        "excluir_conta_use_case",
        lambda: ExcluirContaUseCase(_get_usuario_repository()),
    )


def get_upload_documento() -> UploadDocumentoUseCase:
    return _scoped(
        "upload_documento_use_case",
        lambda: UploadDocumentoUseCase(
            _get_documento_repository(),
            _get_usuario_repository(),
        ),
    )


def get_desassociar_especialidade_medico() -> DesassociarEspecialidadeMedicoUseCase:
    return _scoped(
        "desassociar_especialidade_medico_use_case",
        lambda: DesassociarEspecialidadeMedicoUseCase(
            _get_especialidade_repository(),
            _get_usuario_repository(),
            _get_horario_disponivel_repository(),
        ),
    )
