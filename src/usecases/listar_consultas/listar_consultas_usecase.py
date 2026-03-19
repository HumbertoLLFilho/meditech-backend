from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.models.consulta import Consulta
from src.usecases.listar_consultas.listar_consultas_input import ListarConsultasInput


class ListarConsultaUseCase:

    def __init__(self, repository: ConsultaRepositoryContract):
        self.repository = repository

    def listar(self, input_data: ListarConsultasInput) -> list[Consulta]:
        return self.repository.listar_por_usuario(input_data.usuario_id)
