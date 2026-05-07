from dataclasses import dataclass

from src.domain.models.usuario import StatusAprovacao


@dataclass
class AlterarStatusUsuarioInput:
    usuario_id: int
    status_aprovacao: StatusAprovacao

    @staticmethod
    def from_dict(data: dict) -> "AlterarStatusUsuarioInput":
        if not data.get("usuario_id"):
            raise ValueError("Campo obrigatorio ausente: usuario_id")
        status_raw = data.get("status_aprovacao")
        if not status_raw:
            raise ValueError("Campo obrigatorio ausente: status_aprovacao")
        try:
            status = StatusAprovacao(status_raw)
        except ValueError:
            valores = ", ".join(s.value for s in StatusAprovacao)
            raise ValueError(f"status_aprovacao invalido. Valores aceitos: {valores}")
        return AlterarStatusUsuarioInput(
            usuario_id=data["usuario_id"],
            status_aprovacao=status,
        )
