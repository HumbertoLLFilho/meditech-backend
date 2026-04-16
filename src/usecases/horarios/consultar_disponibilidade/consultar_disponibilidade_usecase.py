from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.usecases.horarios.consultar_disponibilidade.consultar_disponibilidade_input import ConsultarDisponibilidadeInput
from src.usecases.horario_utils import SLOTS_POR_PERIODO, sobrepostos


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

        horarios = self.horario_repository.listar_medicos_por_especialidade_dia_periodo(
            input_data.especialidade_id, dia_semana, input_data.periodo
        )

        resultado = []
        for horario in horarios:
            consultas_do_dia = self.consulta_repository.listar_por_medico_e_data(
                horario.medico_id, input_data.data
            )
            horas_ocupadas = [c.hora for c in consultas_do_dia]

            slots_livres = [
                slot for slot in SLOTS_POR_PERIODO[input_data.periodo]
                if not any(sobrepostos(slot, ocupado) for ocupado in horas_ocupadas)
            ]

            if slots_livres:
                resultado.append({
                    "medico_id": horario.medico_id,
                    "medico_nome": horario.medico.nome if horario.medico else None,
                    "medico_sobrenome": horario.medico.sobrenome if horario.medico else None,
                    "especialidade_id": horario.especialidade_id,
                    "especialidade_nome": horario.especialidade.nome if horario.especialidade else None,
                    "horarios": slots_livres,
                })

        return resultado
