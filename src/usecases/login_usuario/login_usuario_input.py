from dataclasses import dataclass


@dataclass
class LoginUsuarioInput:
    email: str
    senha: str

    @staticmethod
    def from_dict(data: dict) -> "LoginUsuarioInput":
        email = data.get("email")
        senha = data.get("senha")

        if not email or not senha:
            raise ValueError("E-mail e senha sao obrigatorios.")

        return LoginUsuarioInput(email=email, senha=senha)
