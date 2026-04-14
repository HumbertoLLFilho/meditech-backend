from dataclasses import dataclass

from src.domain.models.usuario import StatusAprovacao

VALORES_VALIDOS = [s.value for s in StatusAprovacao]


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
        if status_raw not in VALORES_VALIDOS:
            raise ValueError(f"Status invalido. Valores permitidos: {VALORES_VALIDOS}")
        return AlterarStatusUsuarioInput(
            usuario_id=data["usuario_id"],
            status_aprovacao=StatusAprovacao(status_raw),
        )
