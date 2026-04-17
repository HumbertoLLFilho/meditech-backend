from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.models.usuario import TipoUsuario
from src.usecases.consultas.cancelar_consulta.cancelar_consulta_input import CancelarConsultaInput


class CancelarConsultaUseCase:

    def __init__(self, consulta_repository: ConsultaRepositoryContract):
        self.consulta_repository = consulta_repository

    def executar(self, input_data: CancelarConsultaInput, tipo_usuario: str) -> dict:
        consulta = self.consulta_repository.buscar_por_id(input_data.consulta_id)
        if not consulta:
            raise ValueError("Consulta nao encontrada.")

        if consulta.cancelada:
            raise ValueError("Consulta ja esta cancelada.")

        eh_admin = tipo_usuario == TipoUsuario.ADMIN.value
        eh_paciente_dono = (
            tipo_usuario == TipoUsuario.PACIENTE.value
            and consulta.paciente_id == input_data.usuario_id
        )
        eh_medico_dono = (
            tipo_usuario == TipoUsuario.MEDICO.value
            and consulta.medico_id == input_data.usuario_id
        )
        if not eh_admin and not eh_paciente_dono and not eh_medico_dono:
            raise PermissionError("Voce nao tem permissao para cancelar esta consulta.")

        cancelada = self.consulta_repository.cancelar(input_data.consulta_id, descricao=input_data.descricao)

        return {
            "id": cancelada.id,
            "paciente_id": cancelada.paciente_id,
            "medico_id": cancelada.medico_id,
            "especialidade_id": cancelada.especialidade_id,
            "data_agendada": cancelada.data_agendada.strftime("%Y-%m-%d"),
            "hora": cancelada.hora,
            "cancelada": cancelada.cancelada,
            "descricao_cancelamento": cancelada.descricao_cancelamento,
            "mensagem": "Consulta cancelada com sucesso.",
        }
