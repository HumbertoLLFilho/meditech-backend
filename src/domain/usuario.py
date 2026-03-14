from dataclasses import dataclass
from datetime import date
from enum import Enum


class Genero(str, Enum):
    MASCULINO = "Masculino"
    FEMININO = "Feminino"
    OUTRO = "Outro"
    PREFIRO_NAO_INFORMAR = "Prefiro não Informar"

@dataclass
class Usuario:
    nome: str
    sobrenome: str
    data_nascimento: date
    genero: Genero
    email: str
    senha: str
    cpf: str
