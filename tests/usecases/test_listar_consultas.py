import pytest
from unittest.mock import MagicMock
from datetime import date, datetime

from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.models.consulta import Consulta
from src.domain.models.usuario import Usuario, TipoUsuario, Genero
from src.domain.models.especialidade import Especialidade
from src.usecases.listar_consultas.listar_consultas_usecase import ListarConsultaUseCase
from src.usecases.listar_consultas.listar_consultas_input import ListarConsultasInput


@pytest.fixture
def mock_consulta_repository():
    return MagicMock(spec=ConsultaRepositoryContract)


@pytest.fixture
def usecase(mock_consulta_repository):
    return ListarConsultaUseCase(repository=mock_consulta_repository)


@pytest.fixture
def consulta_com_detalhes(usuario_paciente, usuario_medico, especialidade):
    return Consulta(
        paciente_id=usuario_paciente.id,
        medico_id=usuario_medico.id,
        data_agendada=date(2026, 4, 10),
        hora="09:00",
        especialidade_id=especialidade.id,
        id=1,
        data_cadastrada=datetime(2026, 3, 25, 14, 30, 0),
        cancelada=False,
        medico=usuario_medico,
        paciente=usuario_paciente,
        especialidade=especialidade,
    )


class TestListarConsultasUseCase:

    def test_lista_consultas_do_paciente(
        self, usecase, mock_consulta_repository, usuario_paciente,
        usuario_medico, especialidade, consulta_com_detalhes
    ):
        mock_consulta_repository.listar_por_usuario_com_detalhes.return_value = [
            consulta_com_detalhes
        ]

        input_data = ListarConsultasInput(usuario_id=usuario_paciente.id)
        resultado = usecase.listar(input_data)

        mock_consulta_repository.listar_por_usuario_com_detalhes.assert_called_once_with(
            usuario_paciente.id
        )
        assert len(resultado) == 1
        assert resultado[0]["id"] == 1
        assert resultado[0]["data_agendada"] == "2026-04-10"
        assert resultado[0]["hora"] == "09:00"
        assert resultado[0]["cancelada"] is False
        assert resultado[0]["data_cadastrada"] == "2026-03-25T14:30:00"
        assert resultado[0]["medico"]["id"] == usuario_medico.id
        assert resultado[0]["medico"]["nome"] == "Carlos"
        assert resultado[0]["medico"]["sobrenome"] == "Souza"
        assert resultado[0]["medico"]["email"] == "carlos.souza@email.com"
        assert resultado[0]["medico"]["telefone"] == "11999990002"
        assert resultado[0]["paciente"]["id"] == usuario_paciente.id
        assert resultado[0]["paciente"]["nome"] == "Maria"
        assert resultado[0]["paciente"]["sobrenome"] == "Silva"
        assert resultado[0]["especialidade"]["id"] == especialidade.id
        assert resultado[0]["especialidade"]["nome"] == "Cardiologia"

    def test_lista_consultas_do_medico(
        self, usecase, mock_consulta_repository, usuario_medico,
        usuario_paciente, especialidade, consulta_com_detalhes
    ):
        mock_consulta_repository.listar_por_usuario_com_detalhes.return_value = [
            consulta_com_detalhes
        ]

        input_data = ListarConsultasInput(usuario_id=usuario_medico.id)
        resultado = usecase.listar(input_data)

        mock_consulta_repository.listar_por_usuario_com_detalhes.assert_called_once_with(
            usuario_medico.id
        )
        assert len(resultado) == 1
        assert resultado[0]["medico"]["id"] == usuario_medico.id
        assert resultado[0]["paciente"]["id"] == usuario_paciente.id

    def test_retorna_lista_vazia(self, usecase, mock_consulta_repository):
        mock_consulta_repository.listar_por_usuario_com_detalhes.return_value = []

        input_data = ListarConsultasInput(usuario_id=99)
        resultado = usecase.listar(input_data)

        mock_consulta_repository.listar_por_usuario_com_detalhes.assert_called_once_with(99)
        assert resultado == []

    def test_data_cadastrada_none(
        self, usecase, mock_consulta_repository, usuario_paciente,
        usuario_medico, especialidade
    ):
        consulta = Consulta(
            paciente_id=usuario_paciente.id,
            medico_id=usuario_medico.id,
            data_agendada=date(2026, 5, 1),
            hora="14:00",
            especialidade_id=especialidade.id,
            id=2,
            data_cadastrada=None,
            cancelada=False,
            medico=usuario_medico,
            paciente=usuario_paciente,
            especialidade=especialidade,
        )
        mock_consulta_repository.listar_por_usuario_com_detalhes.return_value = [consulta]

        input_data = ListarConsultasInput(usuario_id=usuario_paciente.id)
        resultado = usecase.listar(input_data)

        assert resultado[0]["data_cadastrada"] is None


class TestListarConsultasInput:

    def test_from_args_valido(self):
        input_data = ListarConsultasInput(usuario_id=1)
        assert input_data.usuario_id == 1

    def test_campos_obrigatorios_ausentes(self):
        with pytest.raises(TypeError):
            ListarConsultasInput()
