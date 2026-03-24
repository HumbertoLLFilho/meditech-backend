from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.usecases.listar_consultas.listar_consultas_input import ListarConsultasInput


class ListarConsultaUseCase:

    def __init__(self, repository: ConsultaRepositoryContract):
        self.repository = repository

    def listar(self, input_data: ListarConsultasInput) -> list[dict]:
        consultas = self.repository.listar_por_usuario(input_data.usuario_id)

        return [
            {
                "id": c.id,
                "paciente_id": c.paciente_id,
                "medico_id": c.medico_id,
                "especialidade_id": c.especialidade_id,
                "data_agendada": c.data_agendada.strftime("%Y-%m-%d"),
                "hora": c.hora,
                "data_cadastrada": c.data_cadastrada.strftime("%Y-%m-%dT%H:%M:%S") if c.data_cadastrada else None,
                "cancelada": c.cancelada,
            }
            for c in consultas
        ]
