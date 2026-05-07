from dataclasses import dataclass


@dataclass
class ExcluirContaInput:
    usuario_id: int

    @staticmethod
    def from_dict(usuario_id: int) -> "ExcluirContaInput":
        if not usuario_id:
            raise ValueError("Campo obrigatorio ausente: usuario_id")
        return ExcluirContaInput(usuario_id=usuario_id)
