from dataclasses import dataclass


@dataclass
class DesassociarEspecialidadeMedicoInput:
    medico_id: int
    especialidade_id: int

    @staticmethod
    def from_dict(data: dict, medico_id: int) -> "DesassociarEspecialidadeMedicoInput":
        especialidade_id = data.get("especialidade_id")
        if not especialidade_id:
            raise ValueError("Campo obrigatorio ausente: especialidade_id")
        try:
            especialidade_id = int(especialidade_id)
        except (TypeError, ValueError):
            raise ValueError("especialidade_id deve ser um inteiro")
        return DesassociarEspecialidadeMedicoInput(
            medico_id=medico_id,
            especialidade_id=especialidade_id,
        )
