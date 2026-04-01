import pytest
from datetime import date, datetime
from src.domain.models.usuario import Usuario, TipoUsuario, Genero
from src.domain.models.consulta import Consulta
from src.domain.models.especialidade import Especialidade


@pytest.fixture
def usuario_paciente():
    return Usuario(
        nome="Maria",
        sobrenome="Silva",
        data_nascimento=date(1990, 5, 15),
        genero=Genero.FEMININO,
        email="maria.silva@email.com",
        senha="hashed_password_123",
        telefone="11999990001",
        tipo=TipoUsuario.PACIENTE,
        ativo=True,
        cpf="12345678901",
        id=1,
        data_cadastro=datetime(2026, 1, 10, 10, 0, 0),
    )


@pytest.fixture
def usuario_medico():
    return Usuario(
        nome="Carlos",
        sobrenome="Souza",
        data_nascimento=date(1985, 3, 20),
        genero=Genero.MASCULINO,
        email="carlos.souza@email.com",
        senha="hashed_password_456",
        telefone="11999990002",
        tipo=TipoUsuario.MEDICO,
        ativo=True,
        cpf="98765432100",
        id=2,
        data_cadastro=datetime(2026, 1, 5, 8, 0, 0),
    )


@pytest.fixture
def especialidade():
    return Especialidade(id=1, nome="Cardiologia")


@pytest.fixture
def consulta(usuario_paciente, usuario_medico, especialidade):
    return Consulta(
        paciente_id=usuario_paciente.id,
        medico_id=usuario_medico.id,
        data_agendada=date(2026, 4, 10),
        hora="09:00",
        especialidade_id=especialidade.id,
        id=1,
        data_cadastrada=datetime(2026, 3, 25, 14, 30, 0),
        cancelada=False,
    )


@pytest.fixture
def dados_usuario_validos():
    return {
        "nome": "Ana",
        "sobrenome": "Oliveira",
        "data_nascimento": "1995-08-25",
        "genero": "feminino",
        "email": "ana.oliveira@email.com",
        "senha": "SenhaForte123!",
        "cpf": "11122233344",
        "telefone": "11988887777",
    }
