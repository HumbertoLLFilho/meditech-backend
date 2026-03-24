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
                "especialidade": c.especialidade,
                "medico": c.medico,
                "data": c.data.strftime("%Y-%m-%d"),
                "horario": c.horario,
            }
            for c in consultas
        ]
