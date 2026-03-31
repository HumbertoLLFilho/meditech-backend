from dataclasses import dataclass


@dataclass
class AssociarEspecialidadeMedicoInput:
    medico_id: int
    especialidade_id: int

    @staticmethod
    def from_dict(data: dict, medico_id: int) -> "AssociarEspecialidadeMedicoInput":
        if not data.get("especialidade_id"):
            raise ValueError("Campo obrigatorio ausente: especialidade_id")

        try:
            especialidade_id = int(data["especialidade_id"])
        except (ValueError, TypeError):
            raise ValueError("Campo 'especialidade_id' deve ser um numero inteiro.")

        return AssociarEspecialidadeMedicoInput(medico_id=medico_id, especialidade_id=especialidade_id)
