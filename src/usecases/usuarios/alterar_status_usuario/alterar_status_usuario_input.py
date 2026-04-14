from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

@dataclass
class AlterarStatusUsuarioInput:
    usuario_id: int
    ativo: bool

    @staticmethod
    def from_dict(data: dict) -> "AlterarStatusUsuarioInput":
        if not data.get("usuario_id"):
            raise ValueError("Campo obrigatorio ausente: usuario_id")
        if not data.get("ativo"):
            raise ValueError("Campo obrigatorio ausente: ativo")

        return AlterarStatusUsuarioInput(
            usuario_id=data["usuario_id"],
            ativo=data["ativo"]
        )
    
    