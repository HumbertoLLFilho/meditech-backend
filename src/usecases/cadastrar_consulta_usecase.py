from src.adapters.controllers.consulta_request import CadastrarConsultaRequest
from src.application.consulta_repository_port import ConsultaRepositoryPort
from src.domain.consulta import Consulta


class CadastrarConsultaUseCase:

    def __init__(self, repository: ConsultaRepositoryPort):
        self.repository = repository

    def executar(self, request: CadastrarConsultaRequest, usuario_id: int) -> Consulta:

        consulta = Consulta(
            usuario_id=usuario_id,
            especialidade=request.especialidade,
            medico=request.medico,
            data=request.data,
            horario=request.horario,
        )

        return self.repository.salvar(consulta)
