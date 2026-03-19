from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.models.consulta import Consulta
from src.usecases.cadastrar_consulta.cadastrar_consulta_input import CadastrarConsultaInput


class CadastrarConsultaUseCase:

    def __init__(self, repository: ConsultaRepositoryContract):
        self.repository = repository

    def executar(self, input_data: CadastrarConsultaInput) -> Consulta:
        consulta = Consulta(
            usuario_id=input_data.usuario_id,
            especialidade=input_data.especialidade,
            medico=input_data.medico,
            data=input_data.data,
            horario=input_data.horario,
        )

        return self.repository.salvar(consulta)
