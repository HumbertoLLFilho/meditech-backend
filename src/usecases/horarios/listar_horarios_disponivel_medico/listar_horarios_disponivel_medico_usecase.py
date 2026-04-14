from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract


class ListarHorariosDisponivelMedicoUseCase:

    def __init__(self, repository: HorarioDisponivelRepositoryContract):
        self.repository = repository

    def listar(self, medico_id: int) -> list[dict]:
        horarios = self.repository.listar_por_medico(medico_id)

        return [
            {
                "id": h.id,
                "especialidade_id": h.especialidade_id,
                "especialidade_nome": h.especialidade.nome if h.especialidade else None,
                "dia_semana": h.dia_semana,
                "periodo": h.periodo,
            }
            for h in horarios
        ]
