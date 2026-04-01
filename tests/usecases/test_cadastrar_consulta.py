import pytest
from datetime import date, datetime
from unittest.mock import MagicMock

from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.models.consulta import Consulta
from src.domain.models.especialidade import Especialidade
from src.usecases.cadastrar_consulta.cadastrar_consulta_usecase import CadastrarConsultaUseCase
from src.usecases.cadastrar_consulta.cadastrar_consulta_input import CadastrarConsultaInput


@pytest.fixture
def mock_consulta_repository():
    return MagicMock(spec=ConsultaRepositoryContract)


@pytest.fixture
def mock_especialidade_repository():
    return MagicMock(spec=EspecialidadeRepositoryContract)


@pytest.fixture
def mock_horario_repository():
    return MagicMock(spec=HorarioDisponivelRepositoryContract)


@pytest.fixture
def usecase(mock_consulta_repository, mock_especialidade_repository, mock_horario_repository):
    return CadastrarConsultaUseCase(
        repository=mock_consulta_repository,
        especialidade_repository=mock_especialidade_repository,
        horario_repository=mock_horario_repository,
    )


@pytest.fixture
def consulta_input():
    return CadastrarConsultaInput(
        paciente_id=1,
        medico_id=2,
        especialidade_id=1,
        data_agendada=date(2026, 4, 6),  # Monday (weekday=0)
        hora="09:00",
    )


class TestCadastrarConsulta:

    def test_agenda_consulta_com_sucesso(
        self, usecase, mock_consulta_repository, mock_especialidade_repository,
        mock_horario_repository, consulta_input, especialidade
    ):
        mock_especialidade_repository.listar_por_medico.return_value = [especialidade]
        mock_horario_repository.listar_periodos_do_medico.return_value = ["manha"]
        mock_consulta_repository.listar_por_medico_e_data.return_value = []
        mock_consulta_repository.salvar.return_value = Consulta(
            paciente_id=1,
            medico_id=2,
            especialidade_id=1,
            data_agendada=date(2026, 4, 6),
            hora="09:00",
            id=1,
            data_cadastrada=datetime(2026, 3, 25, 14, 30, 0),
            cancelada=False,
        )

        resultado = usecase.executar(consulta_input)

        assert resultado["mensagem"] == "Consulta agendada com sucesso!"
        assert resultado["id"] == 1
        assert resultado["hora"] == "09:00"
        assert resultado["paciente_id"] == 1
        assert resultado["medico_id"] == 2
        assert resultado["especialidade_id"] == 1
        assert resultado["data_agendada"] == "2026-04-06"
        assert resultado["cancelada"] is False
        mock_consulta_repository.salvar.assert_called_once()

    def test_rejeita_medico_sem_especialidade(
        self, usecase, mock_especialidade_repository, consulta_input
    ):
        mock_especialidade_repository.listar_por_medico.return_value = []

        with pytest.raises(ValueError, match="Especialidade nao pertence ao medico"):
            usecase.executar(consulta_input)

    def test_rejeita_sem_horario_disponivel_no_dia(
        self, usecase, mock_especialidade_repository, mock_horario_repository,
        consulta_input, especialidade
    ):
        mock_especialidade_repository.listar_por_medico.return_value = [especialidade]
        mock_horario_repository.listar_periodos_do_medico.return_value = []

        with pytest.raises(ValueError, match="O medico nao possui disponibilidade"):
            usecase.executar(consulta_input)

    def test_rejeita_sem_horario_no_periodo(
        self, usecase, mock_especialidade_repository, mock_horario_repository,
        consulta_input, especialidade
    ):
        mock_especialidade_repository.listar_por_medico.return_value = [especialidade]
        mock_horario_repository.listar_periodos_do_medico.return_value = ["tarde"]

        with pytest.raises(ValueError, match="O medico nao possui disponibilidade"):
            usecase.executar(consulta_input)

    def test_rejeita_hora_fora_do_periodo(
        self, usecase, mock_especialidade_repository, mock_horario_repository,
        especialidade
    ):
        mock_especialidade_repository.listar_por_medico.return_value = [especialidade]
        mock_horario_repository.listar_periodos_do_medico.return_value = ["manha"]

        input_hora_invalida = CadastrarConsultaInput(
            paciente_id=1,
            medico_id=2,
            especialidade_id=1,
            data_agendada=date(2026, 4, 6),
            hora="15:00",
        )

        with pytest.raises(ValueError, match="O medico nao possui disponibilidade"):
            usecase.executar(input_hora_invalida)

    def test_rejeita_conflito_de_horario(
        self, usecase, mock_consulta_repository, mock_especialidade_repository,
        mock_horario_repository, consulta_input, especialidade
    ):
        mock_especialidade_repository.listar_por_medico.return_value = [especialidade]
        mock_horario_repository.listar_periodos_do_medico.return_value = ["manha"]
        consulta_existente = Consulta(
            paciente_id=3,
            medico_id=2,
            especialidade_id=1,
            data_agendada=date(2026, 4, 6),
            hora="09:00",
            id=5,
            data_cadastrada=datetime(2026, 3, 20, 10, 0, 0),
            cancelada=False,
        )
        mock_consulta_repository.listar_por_medico_e_data.return_value = [consulta_existente]

        with pytest.raises(ValueError, match="Este horario ja esta reservado"):
            usecase.executar(consulta_input)

    def test_rejeita_conflito_sobreposicao_parcial(
        self, usecase, mock_consulta_repository, mock_especialidade_repository,
        mock_horario_repository, consulta_input, especialidade
    ):
        mock_especialidade_repository.listar_por_medico.return_value = [especialidade]
        mock_horario_repository.listar_periodos_do_medico.return_value = ["manha"]
        consulta_existente = Consulta(
            paciente_id=3,
            medico_id=2,
            especialidade_id=1,
            data_agendada=date(2026, 4, 6),
            hora="08:30",
            id=5,
            data_cadastrada=datetime(2026, 3, 20, 10, 0, 0),
            cancelada=False,
        )
        mock_consulta_repository.listar_por_medico_e_data.return_value = [consulta_existente]

        with pytest.raises(ValueError, match="Este horario ja esta reservado"):
            usecase.executar(consulta_input)


class TestCadastrarConsultaInput:

    def test_from_dict_valido(self):
        data = {
            "medico_id": 2,
            "especialidade_id": 1,
            "data_agendada": "2026-04-06",
            "hora": "09:00",
        }

        resultado = CadastrarConsultaInput.from_dict(data, paciente_id=1)

        assert resultado.paciente_id == 1
        assert resultado.medico_id == 2
        assert resultado.especialidade_id == 1
        assert resultado.data_agendada == date(2026, 4, 6)
        assert resultado.hora == "09:00"

    @pytest.mark.parametrize("campo", ["medico_id", "especialidade_id", "data_agendada", "hora"])
    def test_campos_obrigatorios_ausentes(self, campo):
        data = {
            "medico_id": 2,
            "especialidade_id": 1,
            "data_agendada": "2026-04-06",
            "hora": "09:00",
        }
        del data[campo]

        with pytest.raises(ValueError, match="Campo obrigatorio ausente"):
            CadastrarConsultaInput.from_dict(data, paciente_id=1)

    def test_data_formato_invalido(self):
        data = {
            "medico_id": 2,
            "especialidade_id": 1,
            "data_agendada": "06/04/2026",
            "hora": "09:00",
        }

        with pytest.raises(ValueError, match="Formato de data invalido"):
            CadastrarConsultaInput.from_dict(data, paciente_id=1)

    def test_medico_id_nao_numerico(self):
        data = {
            "medico_id": "abc",
            "especialidade_id": 1,
            "data_agendada": "2026-04-06",
            "hora": "09:00",
        }

        with pytest.raises(ValueError, match="devem ser numeros inteiros"):
            CadastrarConsultaInput.from_dict(data, paciente_id=1)
