import pytest
from datetime import date

from src.usecases.cadastrar_usuario.cadastrar_usuario_input import CadastrarUsuarioInput


class TestFromDictValido:
    def test_from_dict_valido(self, dados_usuario_validos):
        dto = CadastrarUsuarioInput.from_dict(dados_usuario_validos)

        assert dto.nome == "Ana"
        assert dto.sobrenome == "Oliveira"
        assert dto.data_nascimento == date(1995, 8, 25)
        assert dto.genero == "feminino"
        assert dto.email == "ana.oliveira@email.com"
        assert dto.senha == "SenhaForte123!"
        assert dto.cpf == "11122233344"
        assert dto.telefone == "11988887777"
        assert dto.especialidade_ids is None


class TestCampoObrigatorioAusente:
    @pytest.mark.parametrize("campo", [
        "nome",
        "sobrenome",
        "data_nascimento",
        "genero",
        "email",
        "senha",
        "cpf",
        "telefone",
    ])
    def test_campo_obrigatorio_ausente(self, dados_usuario_validos, campo):
        dados = {**dados_usuario_validos}
        del dados[campo]

        with pytest.raises(ValueError, match="Campo obrigatorio ausente"):
            CadastrarUsuarioInput.from_dict(dados)


class TestDataNascimento:
    def test_data_nascimento_formato_invalido(self, dados_usuario_validos):
        dados = {**dados_usuario_validos, "data_nascimento": "22/08/1995"}

        with pytest.raises(ValueError, match="Formato de data invalido"):
            CadastrarUsuarioInput.from_dict(dados)


class TestEspecialidadeIds:
    def test_especialidade_ids_invalido(self, dados_usuario_validos):
        dados = {**dados_usuario_validos, "especialidade_ids": ["abc", "def"]}

        with pytest.raises(ValueError, match="especialidade_ids deve ser uma lista de inteiros"):
            CadastrarUsuarioInput.from_dict(dados)

    def test_especialidade_ids_valido(self, dados_usuario_validos):
        dados = {**dados_usuario_validos, "especialidade_ids": [1, 2]}

        dto = CadastrarUsuarioInput.from_dict(dados)

        assert dto.especialidade_ids == [1, 2]
