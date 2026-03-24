from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract


class ListarHorariosDisponivelMedicoUseCase:

    def __init__(self, repository: HorarioDisponivelRepositoryContract):
        self.repository = repository

    def listar(self, medico_id: int) -> list[dict]:
        horarios = self.repository.listar_por_medico(medico_id)

        return [
            {"id": h.id, "dia_semana": h.dia_semana, "periodo": h.periodo}
            for h in horarios
        ]
