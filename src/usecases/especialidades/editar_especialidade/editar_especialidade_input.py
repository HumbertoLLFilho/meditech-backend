from dataclasses import dataclass


@dataclass
class EditarEspecialidadeInput:
    especialidade_id: int
    nome: str

    @staticmethod
    def from_dict(data: dict, especialidade_id: int) -> "EditarEspecialidadeInput":
        nome = data.get("nome", "").strip()
        if not nome:
            raise ValueError("Campo obrigatorio ausente: nome")
        return EditarEspecialidadeInput(especialidade_id=especialidade_id, nome=nome)
