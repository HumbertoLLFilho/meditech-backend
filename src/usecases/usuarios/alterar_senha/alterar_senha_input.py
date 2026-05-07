from dataclasses import dataclass


@dataclass
class AlterarSenhaInput:
    usuario_id: int
    nova_senha: str
    senha_atual: str | None

    @staticmethod
    def from_dict(data: dict, usuario_id: int) -> "AlterarSenhaInput":
        nova_senha = data.get("nova_senha")
        if not nova_senha:
            raise ValueError("Campo obrigatorio ausente: nova_senha")
        if len(nova_senha) < 6:
            raise ValueError("nova_senha deve ter pelo menos 6 caracteres")
        return AlterarSenhaInput(
            usuario_id=usuario_id,
            nova_senha=nova_senha,
            senha_atual=data.get("senha_atual"),
        )
