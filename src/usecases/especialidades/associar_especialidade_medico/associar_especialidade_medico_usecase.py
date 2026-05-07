from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import TipoUsuario
from src.usecases.especialidades.associar_especialidade_medico.associar_especialidade_medico_input import AssociarEspecialidadeMedicoInput


class AssociarEspecialidadeMedicoUseCase:

    def __init__(
        self,
        especialidade_repository: EspecialidadeRepositoryContract,
        usuario_repository: UsuarioRepositoryContract,
    ):
        self.especialidade_repository = especialidade_repository
        self.usuario_repository = usuario_repository

    def executar(self, input_data: AssociarEspecialidadeMedicoInput) -> dict:
        medico = self.usuario_repository.buscar_por_id(input_data.medico_id)
        if not medico:
            raise ValueError("Medico nao encontrado.")
        if medico.tipo != TipoUsuario.MEDICO:
            raise ValueError("Usuario informado nao e um medico.")

        especialidade = self.especialidade_repository.buscar_por_id(input_data.especialidade_id)
        if not especialidade:
            raise ValueError("Especialidade nao encontrada.")

        self.especialidade_repository.associar_medico(input_data.medico_id, input_data.especialidade_id)

        return {"mensagem": f"Especialidade '{especialidade.nome}' associada ao medico com sucesso."}
