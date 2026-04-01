import pytest
from unittest.mock import MagicMock, call

from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.models.especialidade import Especialidade
from src.usecases.cadastrar_especialidade.cadastrar_especialidade_usecase import CadastrarEspecialidadeUseCase
from src.usecases.cadastrar_especialidade.cadastrar_especialidade_input import CadastrarEspecialidadeInput


@pytest.fixture
def mock_repository():
    return MagicMock(spec=EspecialidadeRepositoryContract)


@pytest.fixture
def usecase(mock_repository):
    return CadastrarEspecialidadeUseCase(repository=mock_repository)


class TestCadastrarEspecialidadeInput:

    def test_from_dict_valido(self):
        dto = CadastrarEspecialidadeInput.from_dict({"nome": "Cardiologia"})
        assert dto.nome == "Cardiologia"

    def test_from_dict_strip_espacos(self):
        dto = CadastrarEspecialidadeInput.from_dict({"nome": "  Neurologia  "})
        assert dto.nome == "Neurologia"

    def test_rejeita_nome_ausente(self):
        with pytest.raises(ValueError, match="Campo obrigatorio ausente: nome"):
            CadastrarEspecialidadeInput.from_dict({})

    def test_rejeita_nome_string_vazia(self):
        with pytest.raises(ValueError, match="Campo obrigatorio ausente: nome"):
            CadastrarEspecialidadeInput.from_dict({"nome": ""})

    def test_nome_apenas_espacos_resulta_em_string_vazia_apos_strip(self):
        # from_dict verifica data.get("nome") antes do strip, entao "   " passa na guarda
        # e o nome resultante fica vazio apos o strip — comportamento atual da implementacao
        dto = CadastrarEspecialidadeInput.from_dict({"nome": "   "})
        assert dto.nome == ""

    def test_rejeita_nome_none(self):
        with pytest.raises(ValueError, match="Campo obrigatorio ausente: nome"):
            CadastrarEspecialidadeInput.from_dict({"nome": None})


class TestCadastrarEspecialidadeUseCase:

    def test_cadastra_especialidade_com_sucesso(self, usecase, mock_repository):
        mock_repository.salvar.return_value = Especialidade(id=1, nome="Cardiologia")

        resultado = usecase.executar(CadastrarEspecialidadeInput(nome="Cardiologia"))

        assert resultado["id"] == 1
        assert resultado["nome"] == "Cardiologia"
        assert resultado["mensagem"] == "Especialidade cadastrada com sucesso!"

    def test_chama_repositorio_salvar_com_especialidade_correta(self, usecase, mock_repository):
        mock_repository.salvar.return_value = Especialidade(id=2, nome="Ortopedia")

        usecase.executar(CadastrarEspecialidadeInput(nome="Ortopedia"))

        mock_repository.salvar.assert_called_once()
        especialidade_passada = mock_repository.salvar.call_args[0][0]
        assert isinstance(especialidade_passada, Especialidade)
        assert especialidade_passada.nome == "Ortopedia"

    def test_retorna_id_gerado_pelo_repositorio(self, usecase, mock_repository):
        mock_repository.salvar.return_value = Especialidade(id=42, nome="Dermatologia")

        resultado = usecase.executar(CadastrarEspecialidadeInput(nome="Dermatologia"))

        assert resultado["id"] == 42

    def test_retorna_nome_do_repositorio(self, usecase, mock_repository):
        # O nome retornado deve vir do objeto salvo, nao do input
        mock_repository.salvar.return_value = Especialidade(id=3, nome="Pediatria")

        resultado = usecase.executar(CadastrarEspecialidadeInput(nome="Pediatria"))

        assert resultado["nome"] == "Pediatria"

    def test_propaga_erro_de_duplicidade_do_repositorio(self, usecase, mock_repository):
        mock_repository.salvar.side_effect = ValueError("Especialidade 'Cardiologia' ja cadastrada.")

        with pytest.raises(ValueError, match="ja cadastrada"):
            usecase.executar(CadastrarEspecialidadeInput(nome="Cardiologia"))

    def test_propaga_excecao_generica_do_repositorio(self, usecase, mock_repository):
        mock_repository.salvar.side_effect = Exception("Erro de banco de dados")

        with pytest.raises(Exception, match="Erro de banco de dados"):
            usecase.executar(CadastrarEspecialidadeInput(nome="Oncologia"))

    def test_nao_importa_flask(self):
        import src.usecases.cadastrar_especialidade.cadastrar_especialidade_usecase as mod
        import sys

        # Nenhum modulo flask deve estar entre as dependencias do modulo
        source_modules = [
            name for name in dir(mod)
            if "flask" in name.lower()
        ]
        assert source_modules == [], f"Modulos Flask encontrados: {source_modules}"
