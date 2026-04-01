import pytest
from unittest.mock import MagicMock

from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.models.horario_disponivel import HorarioDisponivel
from src.usecases.adicionar_horario_disponivel.adicionar_horario_disponivel_usecase import AdicionarHorarioDisponivelUseCase
from src.usecases.adicionar_horario_disponivel.adicionar_horario_disponivel_input import AdicionarHorarioDisponivelInput


@pytest.fixture
def horario_repo():
    return MagicMock(spec=HorarioDisponivelRepositoryContract)


@pytest.fixture
def usuario_repo():
    return MagicMock(spec=UsuarioRepositoryContract)


@pytest.fixture
def especialidade_repo():
    return MagicMock(spec=EspecialidadeRepositoryContract)


@pytest.fixture
def usecase(horario_repo, usuario_repo, especialidade_repo):
    return AdicionarHorarioDisponivelUseCase(horario_repo, usuario_repo, especialidade_repo)


class TestAdicionarHorarioDisponivelUseCase:

    def test_adiciona_horario_com_sucesso(self, usecase, horario_repo, usuario_repo, especialidade_repo, usuario_medico, especialidade):
        usuario_repo.buscar_por_id.return_value = usuario_medico
        especialidade_repo.listar_por_medico.return_value = [especialidade]
        horario_repo.buscar_por_periodo.return_value = None

        horario_salvo = HorarioDisponivel(
            medico_id=usuario_medico.id,
            especialidade_id=especialidade.id,
            dia_semana=0,
            periodo="manha",
            id=1,
        )
        horario_repo.salvar.return_value = horario_salvo

        input_data = AdicionarHorarioDisponivelInput(
            medico_id=usuario_medico.id,
            especialidade_id=especialidade.id,
            dia_semana=0,
            periodo="manha",
        )
        resultado = usecase.executar(input_data)

        assert resultado["mensagem"] == "Horario disponivel cadastrado com sucesso!"
        assert resultado["id"] == 1
        assert resultado["medico_id"] == usuario_medico.id
        assert resultado["especialidade_id"] == especialidade.id
        assert resultado["dia_semana"] == 0
        assert resultado["periodo"] == "manha"
        horario_repo.salvar.assert_called_once()

    def test_rejeita_usuario_nao_medico(self, usecase, usuario_repo, usuario_paciente, especialidade):
        usuario_repo.buscar_por_id.return_value = usuario_paciente

        input_data = AdicionarHorarioDisponivelInput(
            medico_id=usuario_paciente.id,
            especialidade_id=especialidade.id,
            dia_semana=0,
            periodo="manha",
        )

        with pytest.raises(ValueError, match="nao e um medico"):
            usecase.executar(input_data)

    def test_rejeita_medico_nao_encontrado(self, usecase, usuario_repo, especialidade):
        usuario_repo.buscar_por_id.return_value = None

        input_data = AdicionarHorarioDisponivelInput(
            medico_id=999,
            especialidade_id=especialidade.id,
            dia_semana=0,
            periodo="manha",
        )

        with pytest.raises(ValueError, match="Medico nao encontrado"):
            usecase.executar(input_data)

    def test_rejeita_especialidade_nao_associada(self, usecase, usuario_repo, especialidade_repo, usuario_medico):
        usuario_repo.buscar_por_id.return_value = usuario_medico
        especialidade_repo.listar_por_medico.return_value = []

        input_data = AdicionarHorarioDisponivelInput(
            medico_id=usuario_medico.id,
            especialidade_id=99,
            dia_semana=0,
            periodo="manha",
        )

        with pytest.raises(ValueError, match="especialidade nao esta associada"):
            usecase.executar(input_data)

    def test_rejeita_horario_duplicado(self, usecase, horario_repo, usuario_repo, especialidade_repo, usuario_medico, especialidade):
        usuario_repo.buscar_por_id.return_value = usuario_medico
        especialidade_repo.listar_por_medico.return_value = [especialidade]

        horario_existente = HorarioDisponivel(
            medico_id=usuario_medico.id,
            especialidade_id=especialidade.id,
            dia_semana=0,
            periodo="manha",
            id=1,
        )
        horario_repo.buscar_por_periodo.return_value = horario_existente

        input_data = AdicionarHorarioDisponivelInput(
            medico_id=usuario_medico.id,
            especialidade_id=especialidade.id,
            dia_semana=0,
            periodo="manha",
        )

        with pytest.raises(ValueError, match="Periodo ja cadastrado"):
            usecase.executar(input_data)


class TestAdicionarHorarioDisponivelInput:

    def test_rejeita_dia_semana_invalido(self):
        with pytest.raises(ValueError, match="dia_semana"):
            AdicionarHorarioDisponivelInput.from_dict(
                {"dia_semana": 7, "periodo": "manha", "especialidade_id": 1},
                medico_id=1,
            )

    def test_rejeita_periodo_invalido(self):
        with pytest.raises(ValueError, match="periodo"):
            AdicionarHorarioDisponivelInput.from_dict(
                {"dia_semana": 0, "periodo": "almoco", "especialidade_id": 1},
                medico_id=1,
            )

    def test_rejeita_dia_semana_ausente(self):
        with pytest.raises(ValueError, match="dia_semana"):
            AdicionarHorarioDisponivelInput.from_dict(
                {"periodo": "manha", "especialidade_id": 1},
                medico_id=1,
            )

    def test_rejeita_periodo_ausente(self):
        with pytest.raises(ValueError, match="periodo"):
            AdicionarHorarioDisponivelInput.from_dict(
                {"dia_semana": 0, "especialidade_id": 1},
                medico_id=1,
            )

    def test_rejeita_especialidade_id_ausente(self):
        with pytest.raises(ValueError, match="especialidade_id"):
            AdicionarHorarioDisponivelInput.from_dict(
                {"dia_semana": 0, "periodo": "manha"},
                medico_id=1,
            )
