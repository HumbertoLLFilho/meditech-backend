from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.usecases.especialidades.desassociar_especialidade_medico.desassociar_especialidade_medico_input import DesassociarEspecialidadeMedicoInput


class DesassociarEspecialidadeMedicoUseCase:

    def __init__(
        self,
        especialidade_repository: EspecialidadeRepositoryContract,
        usuario_repository: UsuarioRepositoryContract,
        horario_disponivel_repository: HorarioDisponivelRepositoryContract,
    ):
        self.especialidade_repository = especialidade_repository
        self.usuario_repository = usuario_repository
        self.horario_disponivel_repository = horario_disponivel_repository

    def executar(self, input_data: DesassociarEspecialidadeMedicoInput) -> dict:
        medico = self.usuario_repository.buscar_por_id(input_data.medico_id)
        if not medico:
            raise ValueError("Medico nao encontrado.")

        especialidade = self.especialidade_repository.buscar_por_id(input_data.especialidade_id)
        if not especialidade:
            raise ValueError("Especialidade nao encontrada.")

        self.especialidade_repository.desassociar_medico(input_data.medico_id, input_data.especialidade_id)
        self.horario_disponivel_repository.deletar_por_medico_e_especialidade(
            input_data.medico_id, input_data.especialidade_id
        )

        return {"mensagem": "Especialidade desassociada e horarios removidos com sucesso."}
