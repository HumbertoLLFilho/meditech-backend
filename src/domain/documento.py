from dataclasses import dataclass
from enum import Enum


class TipoDocumento(str, Enum):
    CPF = "cpf"
    RG = "rg"
    CNH = "cnh"
    PASSAPORTE = "passaporte"


@dataclass
class Documento:
    tipo: TipoDocumento
    numero: str
    id: int | None = None
    usuario_id: int | None = None
