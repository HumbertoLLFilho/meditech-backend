from dataclasses import dataclass


@dataclass
class ListarConsultasInput:
    usuario_id: int
    tipo_usuario: str
