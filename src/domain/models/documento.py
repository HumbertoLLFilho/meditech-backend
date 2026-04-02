from dataclasses import dataclass
from enum import Enum


class TipoDocumento(str, Enum):
    CRM = "crm"
    CURRICULO = "curriculo"

@dataclass
class Documento:
    tipo: TipoDocumento
    nome_arquivo: str
    mime_type: str
    conteudo: bytes
    id: int | None = None
    usuario_id: int | None = None
