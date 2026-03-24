from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.models.consulta import Consulta
from src.usecases.cadastrar_consulta.cadastrar_consulta_input import CadastrarConsultaInput
from src.usecases.horario_utils import SLOTS_POR_PERIODO, sobrepostos


class CadastrarConsultaUseCase:

    def __init__(
        self,
        repository: ConsultaRepositoryContract,
        especialidade_repository: EspecialidadeRepositoryContract,
        horario_repository: HorarioDisponivelRepositoryContract,
    ):
        self.repository = repository
        self.especialidade_repository = especialidade_repository
        self.horario_repository = horario_repository

    def executar(self, input_data: CadastrarConsultaInput) -> dict:
        # 1. Especialidade pertence ao médico?
        especialidades_medico = self.especialidade_repository.listar_por_medico(input_data.medico_id)
        ids_especialidades = {e.id for e in especialidades_medico}
        if input_data.especialidade_id not in ids_especialidades:
            raise ValueError("Especialidade nao pertence ao medico informado.")

        # 2. Horário solicitado é um slot válido para o médico neste dia?
        dia_semana = input_data.data_agendada.weekday()
        periodos = self.horario_repository.listar_periodos_do_medico(input_data.medico_id, dia_semana)
        slots_validos = [slot for p in periodos for slot in SLOTS_POR_PERIODO[p]]
        if input_data.hora not in slots_validos:
            raise ValueError("O medico nao possui disponibilidade neste dia e horario.")

        # 3. Slot não conflita com outra consulta ativa (janela de 1h)?
        consultas_do_dia = self.repository.listar_por_medico_e_data(
            input_data.medico_id, input_data.data_agendada
        )
        if any(sobrepostos(input_data.hora, c.hora) for c in consultas_do_dia):
            raise ValueError("Este horario ja esta reservado para outro paciente.")

        consulta = Consulta(
            paciente_id=input_data.paciente_id,
            medico_id=input_data.medico_id,
            especialidade_id=input_data.especialidade_id,
            data_agendada=input_data.data_agendada,
            hora=input_data.hora,
        )

        salva = self.repository.salvar(consulta)

        return {
            "id": salva.id,
            "paciente_id": salva.paciente_id,
            "medico_id": salva.medico_id,
            "especialidade_id": salva.especialidade_id,
            "data_agendada": salva.data_agendada.strftime("%Y-%m-%d"),
            "hora": salva.hora,
            "data_cadastrada": salva.data_cadastrada.strftime("%Y-%m-%dT%H:%M:%S") if salva.data_cadastrada else None,
            "cancelada": salva.cancelada,
            "mensagem": "Consulta agendada com sucesso!",
        }
