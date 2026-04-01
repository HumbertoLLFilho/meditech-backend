import pytest
from unittest.mock import MagicMock

from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.models.horario_disponivel import HorarioDisponivel
from src.domain.models.especialidade import Especialidade
from src.usecases.listar_horarios_disponivel_medico.listar_horarios_disponivel_medico_usecase import ListarHorariosDisponivelMedicoUseCase


@pytest.fixture
def horario_repo():
    return MagicMock(spec=HorarioDisponivelRepositoryContract)


@pytest.fixture
def usecase(horario_repo):
    return ListarHorariosDisponivelMedicoUseCase(horario_repo)


class TestListarHorariosDisponivelMedicoUseCase:

    def test_lista_horarios_do_medico(self, usecase, horario_repo, usuario_medico, especialidade):
        horarios = [
            HorarioDisponivel(
                medico_id=usuario_medico.id,
                especialidade_id=especialidade.id,
                dia_semana=0,
                periodo="manha",
                id=1,
                especialidade=especialidade,
            ),
            HorarioDisponivel(
                medico_id=usuario_medico.id,
                especialidade_id=especialidade.id,
                dia_semana=2,
                periodo="tarde",
                id=2,
                especialidade=especialidade,
            ),
        ]
        horario_repo.listar_por_medico.return_value = horarios

        resultado = usecase.listar(usuario_medico.id)

        assert len(resultado) == 2
        assert resultado[0]["id"] == 1
        assert resultado[0]["dia_semana"] == 0
        assert resultado[0]["periodo"] == "manha"
        assert resultado[0]["especialidade_id"] == especialidade.id
        assert resultado[0]["especialidade_nome"] == especialidade.nome
        assert resultado[1]["id"] == 2
        assert resultado[1]["dia_semana"] == 2
        assert resultado[1]["periodo"] == "tarde"
        horario_repo.listar_por_medico.assert_called_once_with(usuario_medico.id)

    def test_retorna_lista_vazia(self, usecase, horario_repo, usuario_medico):
        horario_repo.listar_por_medico.return_value = []

        resultado = usecase.listar(usuario_medico.id)

        assert resultado == []
        horario_repo.listar_por_medico.assert_called_once_with(usuario_medico.id)

    def test_especialidade_none_retorna_nome_none(self, usecase, horario_repo, usuario_medico):
        horario = HorarioDisponivel(
            medico_id=usuario_medico.id,
            especialidade_id=1,
            dia_semana=4,
            periodo="noite",
            id=3,
            especialidade=None,
        )
        horario_repo.listar_por_medico.return_value = [horario]

        resultado = usecase.listar(usuario_medico.id)

        assert len(resultado) == 1
        assert resultado[0]["especialidade_nome"] is None
