from dataclasses import dataclass


@dataclass
class ExcluirEspecialidadeInput:
    especialidade_id: int

    @staticmethod
    def from_path(especialidade_id: int) -> "ExcluirEspecialidadeInput":
        if not especialidade_id:
            raise ValueError("Campo obrigatorio ausente: especialidade_id")
        return ExcluirEspecialidadeInput(especialidade_id=especialidade_id)
