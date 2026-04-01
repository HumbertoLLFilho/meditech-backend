import pytest
from unittest.mock import MagicMock

from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import TipoUsuario
from src.usecases.associar_especialidade_medico.associar_especialidade_medico_usecase import AssociarEspecialidadeMedicoUseCase
from src.usecases.associar_especialidade_medico.associar_especialidade_medico_input import AssociarEspecialidadeMedicoInput


@pytest.fixture
def especialidade_repo():
    return MagicMock(spec=EspecialidadeRepositoryContract)


@pytest.fixture
def usuario_repo():
    return MagicMock(spec=UsuarioRepositoryContract)


@pytest.fixture
def usecase(especialidade_repo, usuario_repo):
    return AssociarEspecialidadeMedicoUseCase(
        especialidade_repository=especialidade_repo,
        usuario_repository=usuario_repo,
    )


class TestAssociarEspecialidadeMedicoUseCase:

    def test_associa_especialidade_com_sucesso(
        self, usecase, usuario_repo, especialidade_repo, usuario_medico, especialidade
    ):
        usuario_repo.buscar_por_id.return_value = usuario_medico
        especialidade_repo.buscar_por_id.return_value = especialidade

        input_data = AssociarEspecialidadeMedicoInput(
            medico_id=usuario_medico.id,
            especialidade_id=especialidade.id,
        )
        resultado = usecase.executar(input_data)

        assert resultado["mensagem"] == f"Especialidade '{especialidade.nome}' associada ao medico com sucesso."
        usuario_repo.buscar_por_id.assert_called_once_with(usuario_medico.id)
        especialidade_repo.buscar_por_id.assert_called_once_with(especialidade.id)
        especialidade_repo.associar_medico.assert_called_once_with(
            usuario_medico.id, especialidade.id
        )

    def test_rejeita_medico_nao_encontrado(
        self, usecase, usuario_repo, especialidade
    ):
        usuario_repo.buscar_por_id.return_value = None

        input_data = AssociarEspecialidadeMedicoInput(medico_id=999, especialidade_id=especialidade.id)

        with pytest.raises(ValueError, match="Medico nao encontrado"):
            usecase.executar(input_data)

    def test_rejeita_usuario_que_nao_e_medico(
        self, usecase, usuario_repo, especialidade, usuario_paciente
    ):
        usuario_repo.buscar_por_id.return_value = usuario_paciente

        input_data = AssociarEspecialidadeMedicoInput(
            medico_id=usuario_paciente.id, especialidade_id=especialidade.id
        )

        with pytest.raises(ValueError, match="nao e um medico"):
            usecase.executar(input_data)

    def test_rejeita_usuario_admin_como_medico(
        self, usecase, usuario_repo, especialidade, usuario_paciente
    ):
        from src.domain.models.usuario import Usuario, Genero
        from datetime import date

        usuario_admin = Usuario(
            id=10,
            nome="Admin",
            sobrenome="Sistema",
            data_nascimento=date(1975, 1, 1),
            genero=Genero.MASCULINO,
            email="admin@meditech.com",
            senha="hash_admin",
            cpf="00011122233",
            telefone="11900000001",
            tipo=TipoUsuario.ADMIN,
            ativo=True,
        )
        usuario_repo.buscar_por_id.return_value = usuario_admin

        input_data = AssociarEspecialidadeMedicoInput(
            medico_id=usuario_admin.id, especialidade_id=especialidade.id
        )

        with pytest.raises(ValueError, match="nao e um medico"):
            usecase.executar(input_data)

    def test_rejeita_especialidade_nao_encontrada(
        self, usecase, usuario_repo, especialidade_repo, usuario_medico
    ):
        usuario_repo.buscar_por_id.return_value = usuario_medico
        especialidade_repo.buscar_por_id.return_value = None

        input_data = AssociarEspecialidadeMedicoInput(
            medico_id=usuario_medico.id, especialidade_id=999
        )

        with pytest.raises(ValueError, match="Especialidade nao encontrada"):
            usecase.executar(input_data)

    def test_nao_busca_especialidade_se_medico_invalido(
        self, usecase, usuario_repo, especialidade_repo
    ):
        usuario_repo.buscar_por_id.return_value = None

        input_data = AssociarEspecialidadeMedicoInput(medico_id=999, especialidade_id=1)

        with pytest.raises(ValueError):
            usecase.executar(input_data)

        especialidade_repo.buscar_por_id.assert_not_called()
        especialidade_repo.associar_medico.assert_not_called()

    def test_nao_associa_se_especialidade_invalida(
        self, usecase, usuario_repo, especialidade_repo, usuario_medico
    ):
        usuario_repo.buscar_por_id.return_value = usuario_medico
        especialidade_repo.buscar_por_id.return_value = None

        input_data = AssociarEspecialidadeMedicoInput(
            medico_id=usuario_medico.id, especialidade_id=999
        )

        with pytest.raises(ValueError):
            usecase.executar(input_data)

        especialidade_repo.associar_medico.assert_not_called()


class TestAssociarEspecialidadeMedicoInput:

    def test_from_dict_valido(self):
        input_data = AssociarEspecialidadeMedicoInput.from_dict(
            {"especialidade_id": 1}, medico_id=2
        )

        assert input_data.especialidade_id == 1
        assert input_data.medico_id == 2

    def test_from_dict_especialidade_id_como_string_numerica(self):
        input_data = AssociarEspecialidadeMedicoInput.from_dict(
            {"especialidade_id": "5"}, medico_id=3
        )

        assert input_data.especialidade_id == 5
        assert input_data.medico_id == 3

    def test_rejeita_especialidade_id_ausente(self):
        with pytest.raises(ValueError, match="especialidade_id"):
            AssociarEspecialidadeMedicoInput.from_dict({}, medico_id=1)

    def test_rejeita_especialidade_id_none(self):
        with pytest.raises(ValueError, match="especialidade_id"):
            AssociarEspecialidadeMedicoInput.from_dict(
                {"especialidade_id": None}, medico_id=1
            )

    def test_rejeita_especialidade_id_nao_numerico(self):
        with pytest.raises(ValueError, match="especialidade_id"):
            AssociarEspecialidadeMedicoInput.from_dict(
                {"especialidade_id": "abc"}, medico_id=1
            )

    def test_rejeita_especialidade_id_zero(self):
        with pytest.raises(ValueError, match="especialidade_id"):
            AssociarEspecialidadeMedicoInput.from_dict(
                {"especialidade_id": 0}, medico_id=1
            )
