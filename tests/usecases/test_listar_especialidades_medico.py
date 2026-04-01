import pytest
from unittest.mock import MagicMock

from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.models.especialidade import Especialidade
from src.usecases.listar_especialidades_medico.listar_especialidades_medico_usecase import ListarEspecialidadesMedicoUseCase


@pytest.fixture
def especialidade_repo():
    return MagicMock(spec=EspecialidadeRepositoryContract)


@pytest.fixture
def usecase(especialidade_repo):
    return ListarEspecialidadesMedicoUseCase(repository=especialidade_repo)


class TestListarEspecialidadesMedicoUseCase:

    def test_lista_especialidades_do_medico(
        self, usecase, especialidade_repo, usuario_medico
    ):
        especialidades = [
            Especialidade(id=1, nome="Cardiologia"),
            Especialidade(id=2, nome="Neurologia"),
        ]
        especialidade_repo.listar_por_medico.return_value = especialidades

        resultado = usecase.listar(usuario_medico.id)

        assert len(resultado) == 2
        assert resultado[0] == {"id": 1, "nome": "Cardiologia"}
        assert resultado[1] == {"id": 2, "nome": "Neurologia"}
        especialidade_repo.listar_por_medico.assert_called_once_with(usuario_medico.id)

    def test_retorna_lista_vazia_quando_medico_sem_especialidades(
        self, usecase, especialidade_repo, usuario_medico
    ):
        especialidade_repo.listar_por_medico.return_value = []

        resultado = usecase.listar(usuario_medico.id)

        assert resultado == []
        especialidade_repo.listar_por_medico.assert_called_once_with(usuario_medico.id)

    def test_retorna_especialidade_unica(
        self, usecase, especialidade_repo, usuario_medico, especialidade
    ):
        especialidade_repo.listar_por_medico.return_value = [especialidade]

        resultado = usecase.listar(usuario_medico.id)

        assert len(resultado) == 1
        assert resultado[0]["id"] == especialidade.id
        assert resultado[0]["nome"] == especialidade.nome

    def test_formato_de_saida_contem_apenas_id_e_nome(
        self, usecase, especialidade_repo, usuario_medico
    ):
        especialidade_repo.listar_por_medico.return_value = [
            Especialidade(id=3, nome="Pediatria")
        ]

        resultado = usecase.listar(usuario_medico.id)

        assert set(resultado[0].keys()) == {"id", "nome"}

    def test_repassa_medico_id_correto_ao_repositorio(
        self, usecase, especialidade_repo
    ):
        especialidade_repo.listar_por_medico.return_value = []

        usecase.listar(42)

        especialidade_repo.listar_por_medico.assert_called_once_with(42)

    def test_lista_muitas_especialidades(
        self, usecase, especialidade_repo, usuario_medico
    ):
        nomes = ["Cardiologia", "Neurologia", "Ortopedia", "Dermatologia", "Ginecologia"]
        especialidades = [Especialidade(id=i + 1, nome=nome) for i, nome in enumerate(nomes)]
        especialidade_repo.listar_por_medico.return_value = especialidades

        resultado = usecase.listar(usuario_medico.id)

        assert len(resultado) == 5
        for i, nome in enumerate(nomes):
            assert resultado[i]["id"] == i + 1
            assert resultado[i]["nome"] == nome
