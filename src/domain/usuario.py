from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Genero(str, Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTRO = "outro"
    PREFIRO_NAO_INFORMAR = "prefiro_nao_informar"


@dataclass
class Usuario:
    nome: str
    sobrenome: str
    data_nascimento: date
    genero: Genero
    email: str
    cpf: str | None = None
    rg: str | None = None
    id: int | None = None
