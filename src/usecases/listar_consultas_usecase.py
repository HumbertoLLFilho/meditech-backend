from src.application.consulta_repository_port import ConsultaRepositoryPort
from src.domain.consulta import Consulta


class ListarConsultaUseCase:

    def __init__(self, repository: ConsultaRepositoryPort):
        self.repository = repository

    def listar(self, usuario_id: int) -> list[Consulta]:
        return self.repository.listar_por_usuario(usuario_id)