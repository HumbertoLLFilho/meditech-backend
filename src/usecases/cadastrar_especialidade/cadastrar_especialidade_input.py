from dataclasses import dataclass


@dataclass
class CadastrarEspecialidadeInput:
    nome: str

    @staticmethod
    def from_dict(data: dict) -> "CadastrarEspecialidadeInput":
        if not data.get("nome"):
            raise ValueError("Campo obrigatorio ausente: nome")
        return CadastrarEspecialidadeInput(nome=data["nome"].strip())
