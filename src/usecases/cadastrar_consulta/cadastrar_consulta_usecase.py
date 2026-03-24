from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.models.consulta import Consulta
from src.usecases.cadastrar_consulta.cadastrar_consulta_input import CadastrarConsultaInput


class CadastrarConsultaUseCase:

    def __init__(self, repository: ConsultaRepositoryContract):
        self.repository = repository

    def executar(self, input_data: CadastrarConsultaInput) -> dict:
        consulta = Consulta(
            usuario_id=input_data.usuario_id,
            especialidade=input_data.especialidade,
            medico=input_data.medico,
            data=input_data.data,
            horario=input_data.horario,
        )

        salva = self.repository.salvar(consulta)

        return {
            "id": salva.id,
            "especialidade": salva.especialidade,
            "medico": salva.medico,
            "data": salva.data.strftime("%Y-%m-%d"),
            "horario": salva.horario,
            "mensagem": "Consulta realizada com sucesso!",
        }
