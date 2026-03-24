from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.usecases.consultar_disponibilidade.consultar_disponibilidade_input import ConsultarDisponibilidadeInput


def _in_periodo(hora: str, periodo: str) -> bool:
    if periodo == "manha":
        return "06:00" <= hora <= "11:59"
    if periodo == "tarde":
        return "13:00" <= hora <= "18:00"
    if periodo == "noite":
        return hora >= "19:00" or hora <= "02:00"
    return False


class ConsultarDisponibilidadeUseCase:

    def __init__(
        self,
        horario_repository: HorarioDisponivelRepositoryContract,
        consulta_repository: ConsultaRepositoryContract,
    ):
        self.horario_repository = horario_repository
        self.consulta_repository = consulta_repository

    def executar(self, input_data: ConsultarDisponibilidadeInput) -> list[dict]:
        dia_semana = input_data.data.weekday()

        horarios = self.horario_repository.listar_por_especialidade_e_dia(
            input_data.especialidade_id, dia_semana
        )

        resultado: dict[int, list[str]] = {}

        for h in horarios:
            if not _in_periodo(h.hora, input_data.periodo):
                continue
            if self.consulta_repository.existe_consulta_ativa(h.medico_id, input_data.data, h.hora):
                continue

            resultado.setdefault(h.medico_id, []).append(h.hora)

        return [
            {"medico_id": medico_id, "horarios": horarios_livres}
            for medico_id, horarios_livres in resultado.items()
        ]
