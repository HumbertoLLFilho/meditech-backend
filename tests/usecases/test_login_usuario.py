import pytest
from unittest.mock import MagicMock

from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.contracts.password_service_contract import PasswordServiceContract
from src.domain.contracts.token_service_contract import TokenServiceContract
from src.usecases.login_usuario.login_usuario_usecase import LoginUsuarioUseCase, InvalidCredentialsError
from src.usecases.login_usuario.login_usuario_input import LoginUsuarioInput


@pytest.fixture
def mock_repository():
    return MagicMock(spec=UsuarioRepositoryContract)


@pytest.fixture
def mock_password_service():
    return MagicMock(spec=PasswordServiceContract)


@pytest.fixture
def mock_token_service():
    return MagicMock(spec=TokenServiceContract)


@pytest.fixture
def usecase(mock_repository, mock_password_service, mock_token_service):
    return LoginUsuarioUseCase(
        repository=mock_repository,
        password_service=mock_password_service,
        token_service=mock_token_service,
    )


@pytest.fixture
def login_input():
    return LoginUsuarioInput(email="maria.silva@email.com", senha="SenhaForte123!")


class TestLoginUsuario:

    def test_login_com_sucesso(
        self, usecase, mock_repository, mock_password_service, mock_token_service,
        login_input, usuario_paciente
    ):
        mock_repository.buscar_por_email.return_value = usuario_paciente
        mock_password_service.verify.return_value = True
        mock_token_service.generate_access_token.return_value = "jwt_token_abc"

        resultado = usecase.executar(login_input)

        assert resultado["access_token"] == "jwt_token_abc"
        mock_repository.buscar_por_email.assert_called_once_with("maria.silva@email.com")
        mock_password_service.verify.assert_called_once_with("SenhaForte123!", usuario_paciente.senha)
        mock_token_service.generate_access_token.assert_called_once_with(usuario_paciente)

    def test_rejeita_email_nao_encontrado(self, usecase, mock_repository, mock_password_service, login_input):
        mock_repository.buscar_por_email.return_value = None

        with pytest.raises(InvalidCredentialsError, match="E-mail ou senha invalidos"):
            usecase.executar(login_input)

    def test_rejeita_senha_incorreta(
        self, usecase, mock_repository, mock_password_service, login_input, usuario_paciente
    ):
        mock_repository.buscar_por_email.return_value = usuario_paciente
        mock_password_service.verify.return_value = False

        with pytest.raises(InvalidCredentialsError, match="E-mail ou senha invalidos"):
            usecase.executar(login_input)

    def test_rejeita_usuario_inativo(
        self, usecase, mock_repository, mock_password_service, login_input, usuario_paciente
    ):
        usuario_paciente.ativo = False
        mock_repository.buscar_por_email.return_value = usuario_paciente
        mock_password_service.verify.return_value = True

        with pytest.raises(InvalidCredentialsError, match="Conta inativa"):
            usecase.executar(login_input)
