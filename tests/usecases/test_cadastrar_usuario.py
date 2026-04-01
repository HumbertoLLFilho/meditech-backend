import pytest
from datetime import date
from unittest.mock import MagicMock

from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.contracts.password_service_contract import PasswordServiceContract
from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.models.usuario import Usuario, TipoUsuario, Genero
from src.usecases.cadastrar_usuario.cadastrar_usuario_usecase import CadastrarUsuarioUseCase
from src.usecases.cadastrar_usuario.cadastrar_usuario_input import CadastrarUsuarioInput


@pytest.fixture
def mock_repository():
    return MagicMock(spec=UsuarioRepositoryContract)


@pytest.fixture
def mock_password_service():
    return MagicMock(spec=PasswordServiceContract)


@pytest.fixture
def mock_especialidade_repository():
    return MagicMock(spec=EspecialidadeRepositoryContract)


@pytest.fixture
def usecase(mock_repository, mock_password_service, mock_especialidade_repository):
    return CadastrarUsuarioUseCase(
        repository=mock_repository,
        password_service=mock_password_service,
        especialidade_repository=mock_especialidade_repository,
    )


@pytest.fixture
def input_paciente(dados_usuario_validos):
    return CadastrarUsuarioInput.from_dict(dados_usuario_validos)


class TestCadastrarUsuario:

    def test_cadastra_paciente_com_sucesso(
        self, usecase, mock_repository, mock_password_service, input_paciente
    ):
        mock_repository.buscar_por_email.return_value = None
        mock_repository.buscar_por_cpf.return_value = None
        mock_password_service.hash.return_value = "hashed_senha"
        mock_repository.salvar.return_value = Usuario(
            nome="Ana",
            sobrenome="Oliveira",
            data_nascimento=date(1995, 8, 25),
            genero=Genero.FEMININO,
            email="ana.oliveira@email.com",
            senha="hashed_senha",
            cpf="11122233344",
            telefone="11988887777",
            tipo=TipoUsuario.PACIENTE,
            ativo=True,
            id=1,
        )

        resultado = usecase.executar(input_paciente, tipo=TipoUsuario.PACIENTE, ativo=True)

        assert resultado["mensagem"] == "paciente cadastrado com sucesso!"
        mock_password_service.hash.assert_called_once_with("SenhaForte123!")
        mock_repository.salvar.assert_called_once()

    def test_rejeita_email_duplicado(self, usecase, mock_repository, input_paciente, usuario_paciente):
        mock_repository.buscar_por_email.return_value = usuario_paciente

        with pytest.raises(ValueError, match="E-mail ja cadastrado"):
            usecase.executar(input_paciente)

    def test_rejeita_cpf_duplicado(self, usecase, mock_repository, input_paciente, usuario_paciente):
        mock_repository.buscar_por_email.return_value = None
        mock_repository.buscar_por_cpf.return_value = usuario_paciente

        with pytest.raises(ValueError, match="CPF ja cadastrado"):
            usecase.executar(input_paciente)

    def test_rejeita_genero_invalido(self, usecase, mock_repository):
        input_data = CadastrarUsuarioInput(
            nome="Ana",
            sobrenome="Oliveira",
            data_nascimento=date(1995, 8, 25),
            genero="invalido",
            email="ana@email.com",
            senha="SenhaForte123!",
            cpf="11122233344",
            telefone="11988887777",
        )
        mock_repository.buscar_por_email.return_value = None
        mock_repository.buscar_por_cpf.return_value = None

        with pytest.raises(ValueError, match="Genero invalido"):
            usecase.executar(input_data)
