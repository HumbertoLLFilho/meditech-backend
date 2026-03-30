from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.horario_disponivel import HorarioDisponivel
from src.domain.models.usuario import TipoUsuario
from src.usecases.adicionar_horario_disponivel.adicionar_horario_disponivel_input import AdicionarHorarioDisponivelInput


class AdicionarHorarioDisponivelUseCase:

    def __init__(
        self,
        repository: HorarioDisponivelRepositoryContract,
        usuario_repository: UsuarioRepositoryContract,
        especialidade_repository: EspecialidadeRepositoryContract,
    ):
        self.repository = repository
        self.usuario_repository = usuario_repository
        self.especialidade_repository = especialidade_repository

    def executar(self, input_data: AdicionarHorarioDisponivelInput) -> dict:
        medico = self.usuario_repository.buscar_por_id(input_data.medico_id)
        if not medico:
            raise ValueError("Medico nao encontrado.")
        if medico.tipo != TipoUsuario.MEDICO:
            raise ValueError("Usuario informado nao e um medico.")

        especialidades_medico = self.especialidade_repository.listar_por_medico(input_data.medico_id)
        if not any(e.id == input_data.especialidade_id for e in especialidades_medico):
            raise ValueError("Esta especialidade nao esta associada ao medico.")

        if self.repository.buscar_por_periodo(
            input_data.medico_id, input_data.especialidade_id, input_data.dia_semana, input_data.periodo
        ):
            raise ValueError("Periodo ja cadastrado para este medico nesta especialidade neste dia.")

        horario = HorarioDisponivel(
            medico_id=input_data.medico_id,
            especialidade_id=input_data.especialidade_id,
            dia_semana=input_data.dia_semana,
            periodo=input_data.periodo,
        )
        salvo = self.repository.salvar(horario)

        return {
            "id": salvo.id,
            "medico_id": salvo.medico_id,
            "especialidade_id": salvo.especialidade_id,
            "dia_semana": salvo.dia_semana,
            "periodo": salvo.periodo,
            "mensagem": "Horario disponivel cadastrado com sucesso!",
        }
