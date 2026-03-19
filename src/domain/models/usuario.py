from dataclasses import dataclass
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
    senha: str
    cpf: str
    id: int | None = None
