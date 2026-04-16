from dataclasses import dataclass


@dataclass
class BaixarDocumentoInput:
    usuario_id: int
    tipo_solicitante: str
    documento_id: int
