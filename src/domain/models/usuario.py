from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum

class Genero(str, Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTRO = "outro"
    PREFIRO_NAO_INFORMAR = "prefiro_nao_informar"

class TipoUsuario(str, Enum):
    ADMIN = "admin"
    MEDICO = "medico"
    PACIENTE = "paciente"

@dataclass
class Usuario:
    nome: str
    sobrenome: str
    data_nascimento: date
    genero: Genero
    email: str
    senha: str
    telefone: str
    tipo: TipoUsuario
    ativo: bool
    cpf: str
    id: int | None = None
    data_cadastro: datetime | None = None
