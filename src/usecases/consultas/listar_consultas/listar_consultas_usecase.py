from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.usecases.consultas.listar_consultas.listar_consultas_input import ListarConsultasInput


class ListarConsultaUseCase:

    def __init__(self, repository: ConsultaRepositoryContract):
        self.repository = repository

    def listar(self, input_data: ListarConsultasInput) -> list[dict]:
        consultas = self.repository.listar_por_usuario_com_detalhes(input_data.usuario_id, input_data.tipo_usuario)

        return [
            {
                "id": c.id,
                "data_agendada": c.data_agendada.strftime("%Y-%m-%d"),
                "hora": c.hora,
                "cancelada": c.cancelada,
                "data_cadastrada": (
                    c.data_cadastrada.strftime("%Y-%m-%dT%H:%M:%S")
                    if c.data_cadastrada else None
                ),
                "medico": {
                    "id": c.medico.id,
                    "nome": c.medico.nome,
                    "sobrenome": c.medico.sobrenome,
                    "email": c.medico.email,
                    "telefone": c.medico.telefone,
                },
                "paciente": {
                    "id": c.paciente.id,
                    "nome": c.paciente.nome,
                    "sobrenome": c.paciente.sobrenome,
                },
                "especialidade": {
                    "id": c.especialidade.id,
                    "nome": c.especialidade.nome,
                },
            }
            for c in consultas
        ]
