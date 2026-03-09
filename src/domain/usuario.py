from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Genero(str, Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTRO = "outro"
    PREFIRO_NAO_INFORMAR = "prefiro_nao_informar"


class TipoUsuario(str, Enum):
    PACIENTE = "paciente"
    DOUTOR = "doutor"
    ADMIN = "admin"


@dataclass
class Usuario:
    nome: str
    sobrenome: str
    data_nascimento: date
    genero: Genero
    email: str
    senha: str
    tipo: TipoUsuario = TipoUsuario.PACIENTE
    documentos: list = field(default_factory=list)  # Lista de Documento
    id: int | None = None
