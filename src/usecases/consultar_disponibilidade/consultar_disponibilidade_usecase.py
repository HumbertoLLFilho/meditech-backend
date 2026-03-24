from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.usecases.consultar_disponibilidade.consultar_disponibilidade_input import ConsultarDisponibilidadeInput
from src.usecases.horario_utils import SLOTS_POR_PERIODO, sobrepostos


class ConsultarDisponibilidadeUseCase:

    def __init__(
        self,
        horario_repository: HorarioDisponivelRepositoryContract,
        consulta_repository: ConsultaRepositoryContract,
        usuario_repository: UsuarioRepositoryContract,
    ):
        self.horario_repository = horario_repository
        self.consulta_repository = consulta_repository
        self.usuario_repository = usuario_repository

    def executar(self, input_data: ConsultarDisponibilidadeInput) -> list[dict]:
        dia_semana = input_data.data.weekday()

        medico_ids = self.horario_repository.listar_medicos_por_especialidade_dia_periodo(
            input_data.especialidade_id, dia_semana, input_data.periodo
        )

        resultado = []
        for medico_id in medico_ids:
            consultas_do_dia = self.consulta_repository.listar_por_medico_e_data(
                medico_id, input_data.data
            )
            horas_ocupadas = [c.hora for c in consultas_do_dia]

            slots_livres = [
                slot for slot in SLOTS_POR_PERIODO[input_data.periodo]
                if not any(sobrepostos(slot, ocupado) for ocupado in horas_ocupadas)
            ]

            if slots_livres:
                medico = self.usuario_repository.buscar_por_id(medico_id)
                resultado.append({
                    "medico_id": medico_id,
                    "medico_nome": medico.nome if medico else None,
                    "medico_sobrenome": medico.sobrenome if medico else None,
                    "horarios": slots_livres,
                })

        return resultado
