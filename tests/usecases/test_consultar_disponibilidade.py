import pytest
from datetime import date, datetime
from unittest.mock import MagicMock

from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.models.horario_disponivel import HorarioDisponivel
from src.domain.models.consulta import Consulta
from src.domain.models.usuario import Usuario, TipoUsuario, Genero
from src.domain.models.especialidade import Especialidade
from src.usecases.consultar_disponibilidade.consultar_disponibilidade_usecase import ConsultarDisponibilidadeUseCase
from src.usecases.consultar_disponibilidade.consultar_disponibilidade_input import ConsultarDisponibilidadeInput
from src.usecases.horario_utils import SLOTS_POR_PERIODO


@pytest.fixture
def horario_repo():
    return MagicMock(spec=HorarioDisponivelRepositoryContract)


@pytest.fixture
def consulta_repo():
    return MagicMock(spec=ConsultaRepositoryContract)


@pytest.fixture
def usecase(horario_repo, consulta_repo):
    return ConsultarDisponibilidadeUseCase(horario_repo, consulta_repo)


@pytest.fixture
def medico():
    return Usuario(
        nome="Carlos",
        sobrenome="Souza",
        data_nascimento=date(1985, 3, 20),
        genero=Genero.MASCULINO,
        email="carlos.souza@email.com",
        senha="hashed",
        telefone="11999990002",
        tipo=TipoUsuario.MEDICO,
        ativo=True,
        cpf="98765432100",
        id=2,
    )


@pytest.fixture
def especialidade_cardio():
    return Especialidade(id=1, nome="Cardiologia")


@pytest.fixture
def horario_manha(medico, especialidade_cardio):
    return HorarioDisponivel(
        medico_id=medico.id,
        especialidade_id=especialidade_cardio.id,
        dia_semana=3,  # quinta-feira
        periodo="manha",
        id=10,
        medico=medico,
        especialidade=especialidade_cardio,
    )


# ── Sucesso ──────────────────────────────────────────────────────────


class TestRetornaSlotsDisponiveis:
    def test_retorna_slots_disponiveis(self, usecase, horario_repo, consulta_repo, horario_manha):
        """Medico tem horario no periodo, nenhuma consulta → retorna todos os slots."""
        # 2026-04-02 é quinta-feira (weekday=3)
        data_consulta = date(2026, 4, 2)

        horario_repo.listar_medicos_por_especialidade_dia_periodo.return_value = [horario_manha]
        consulta_repo.listar_por_medico_e_data.return_value = []

        input_data = ConsultarDisponibilidadeInput(
            especialidade_id=1, data=data_consulta, periodo="manha"
        )
        resultado = usecase.executar(input_data)

        assert len(resultado) == 1
        assert resultado[0]["medico_id"] == horario_manha.medico_id
        assert resultado[0]["medico_nome"] == "Carlos"
        assert resultado[0]["medico_sobrenome"] == "Souza"
        assert resultado[0]["especialidade_id"] == 1
        assert resultado[0]["especialidade_nome"] == "Cardiologia"
        assert resultado[0]["horarios"] == SLOTS_POR_PERIODO["manha"]

    def test_exclui_slots_ocupados(self, usecase, horario_repo, consulta_repo, horario_manha):
        """Consultas agendadas removem slots conflitantes (janela de 1h)."""
        data_consulta = date(2026, 4, 2)

        horario_repo.listar_medicos_por_especialidade_dia_periodo.return_value = [horario_manha]

        consulta_existente = Consulta(
            paciente_id=1,
            medico_id=horario_manha.medico_id,
            especialidade_id=1,
            data_agendada=data_consulta,
            hora="09:00",
            id=100,
            data_cadastrada=datetime(2026, 3, 25, 14, 0, 0),
            cancelada=False,
        )
        consulta_repo.listar_por_medico_e_data.return_value = [consulta_existente]

        input_data = ConsultarDisponibilidadeInput(
            especialidade_id=1, data=data_consulta, periodo="manha"
        )
        resultado = usecase.executar(input_data)

        slots_retornados = resultado[0]["horarios"]
        # Slots dentro da janela de 1h a partir de 09:00 devem ser removidos:
        # 09:00 e 09:30 são sobrepostos com consulta das 09:00
        assert "09:00" not in slots_retornados
        assert "09:30" not in slots_retornados
        # Slots fora da janela permanecem
        assert "08:00" in slots_retornados
        assert "10:00" in slots_retornados

    def test_retorna_vazio_sem_horario_disponivel(self, usecase, horario_repo, consulta_repo):
        """Medico nao tem horario cadastrado para o periodo/dia → lista vazia."""
        data_consulta = date(2026, 4, 2)

        horario_repo.listar_medicos_por_especialidade_dia_periodo.return_value = []

        input_data = ConsultarDisponibilidadeInput(
            especialidade_id=1, data=data_consulta, periodo="manha"
        )
        resultado = usecase.executar(input_data)

        assert resultado == []
        consulta_repo.listar_por_medico_e_data.assert_not_called()


# ── Validacao do DTO ─────────────────────────────────────────────────


class TestConsultarDisponibilidadeInput:
    def test_from_args_valido(self):
        args = {"especialidade_id": "1", "data": "2026-04-02", "periodo": "manha"}
        dto = ConsultarDisponibilidadeInput.from_args(args)

        assert dto.especialidade_id == 1
        assert dto.data == date(2026, 4, 2)
        assert dto.periodo == "manha"

    def test_data_invalida(self):
        args = {"especialidade_id": "1", "data": "02-04-2026", "periodo": "manha"}
        with pytest.raises(ValueError, match="formato YYYY-MM-DD"):
            ConsultarDisponibilidadeInput.from_args(args)

    def test_periodo_invalido(self):
        args = {"especialidade_id": "1", "data": "2026-04-02", "periodo": "almoco"}
        with pytest.raises(ValueError, match="periodo"):
            ConsultarDisponibilidadeInput.from_args(args)

    def test_especialidade_id_ausente(self):
        args = {"data": "2026-04-02", "periodo": "manha"}
        with pytest.raises(ValueError, match="especialidade_id"):
            ConsultarDisponibilidadeInput.from_args(args)

    def test_data_ausente(self):
        args = {"especialidade_id": "1", "periodo": "manha"}
        with pytest.raises(ValueError, match="data"):
            ConsultarDisponibilidadeInput.from_args(args)

    def test_periodo_ausente(self):
        args = {"especialidade_id": "1", "data": "2026-04-02"}
        with pytest.raises(ValueError, match="periodo"):
            ConsultarDisponibilidadeInput.from_args(args)

    def test_especialidade_id_nao_numerico(self):
        args = {"especialidade_id": "abc", "data": "2026-04-02", "periodo": "manha"}
        with pytest.raises(ValueError, match="numero inteiro"):
            ConsultarDisponibilidadeInput.from_args(args)
