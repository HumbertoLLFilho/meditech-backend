from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class CadastrarUsuarioInput:
    nome: str
    sobrenome: str
    data_nascimento: date
    genero: str
    email: str
    senha: str
    cpf: str

    @staticmethod
    def from_dict(data: dict) -> "CadastrarUsuarioInput":
        campos_obrigatorios = ["nome", "sobrenome", "data_nascimento", "genero", "email", "senha", "cpf"]
        for campo in campos_obrigatorios:
            if not data.get(campo):
                raise ValueError(f"Campo obrigatorio ausente: {campo}")

        try:
            data_nascimento = datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de data invalido. Use YYYY-MM-DD.")

        return CadastrarUsuarioInput(
            nome=data["nome"],
            sobrenome=data["sobrenome"],
            data_nascimento=data_nascimento,
            genero=data["genero"],
            email=data["email"],
            senha=data["senha"],
            cpf=data["cpf"],
        )
