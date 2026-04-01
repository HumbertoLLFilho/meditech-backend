import pytest
from unittest.mock import MagicMock

from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.models.especialidade import Especialidade
from src.usecases.listar_especialidades.listar_especialidades_usecase import ListarEspecialidadesUseCase


@pytest.fixture
def mock_repository():
    return MagicMock(spec=EspecialidadeRepositoryContract)


@pytest.fixture
def usecase(mock_repository):
    return ListarEspecialidadesUseCase(repository=mock_repository)


class TestListarEspecialidadesUseCase:

    def test_retorna_lista_com_todas_especialidades(self, usecase, mock_repository):
        mock_repository.listar.return_value = [
            Especialidade(id=1, nome="Cardiologia"),
            Especialidade(id=2, nome="Ortopedia"),
            Especialidade(id=3, nome="Neurologia"),
        ]

        resultado = usecase.listar()

        assert len(resultado) == 3

    def test_retorna_formato_dict_correto(self, usecase, mock_repository):
        mock_repository.listar.return_value = [
            Especialidade(id=1, nome="Cardiologia"),
        ]

        resultado = usecase.listar()

        assert resultado[0] == {"id": 1, "nome": "Cardiologia"}

    def test_retorna_lista_vazia_quando_sem_especialidades(self, usecase, mock_repository):
        mock_repository.listar.return_value = []

        resultado = usecase.listar()

        assert resultado == []

    def test_mapeia_todos_campos_corretamente(self, usecase, mock_repository):
        mock_repository.listar.return_value = [
            Especialidade(id=10, nome="Dermatologia"),
            Especialidade(id=20, nome="Pediatria"),
        ]

        resultado = usecase.listar()

        assert resultado[0]["id"] == 10
        assert resultado[0]["nome"] == "Dermatologia"
        assert resultado[1]["id"] == 20
        assert resultado[1]["nome"] == "Pediatria"

    def test_chama_repositorio_listar_uma_vez(self, usecase, mock_repository):
        mock_repository.listar.return_value = []

        usecase.listar()

        mock_repository.listar.assert_called_once()

    def test_resultado_contem_apenas_chaves_id_e_nome(self, usecase, mock_repository):
        mock_repository.listar.return_value = [
            Especialidade(id=1, nome="Cardiologia"),
        ]

        resultado = usecase.listar()

        assert set(resultado[0].keys()) == {"id", "nome"}

    def test_ordem_preservada_do_repositorio(self, usecase, mock_repository):
        especialidades = [
            Especialidade(id=3, nome="Neurologia"),
            Especialidade(id=1, nome="Cardiologia"),
            Especialidade(id=2, nome="Ortopedia"),
        ]
        mock_repository.listar.return_value = especialidades

        resultado = usecase.listar()

        assert resultado[0]["id"] == 3
        assert resultado[1]["id"] == 1
        assert resultado[2]["id"] == 2

    def test_propaga_excecao_do_repositorio(self, usecase, mock_repository):
        mock_repository.listar.side_effect = Exception("Erro de conexao com banco")

        with pytest.raises(Exception, match="Erro de conexao com banco"):
            usecase.listar()

    def test_nao_importa_flask(self):
        import src.usecases.listar_especialidades.listar_especialidades_usecase as mod

        source_modules = [
            name for name in dir(mod)
            if "flask" in name.lower()
        ]
        assert source_modules == [], f"Modulos Flask encontrados: {source_modules}"
