from dataclasses import dataclass


@dataclass
class AlterarStatusUsuarioInput:
    usuario_id: int
    ativo: bool

    @staticmethod
    def from_dict(data: dict) -> "AlterarStatusUsuarioInput":
        if not data.get("usuario_id"):
            raise ValueError("Campo obrigatorio ausente: usuario_id")
        if "ativo" not in data or not isinstance(data.get("ativo"), bool):
            raise ValueError("Campo obrigatorio ausente ou invalido: ativo (deve ser true ou false)")
        return AlterarStatusUsuarioInput(
            usuario_id=data["usuario_id"],
            ativo=data["ativo"],
        )
