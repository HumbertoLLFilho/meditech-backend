import re
from dataclasses import dataclass


@dataclass
class AdicionarHorarioDisponivelInput:
    medico_id: int
    dia_semana: int
    hora: str

    @staticmethod
    def from_dict(data: dict, medico_id: int) -> "AdicionarHorarioDisponivelInput":
        if data.get("dia_semana") is None:
            raise ValueError("Campo obrigatorio ausente: dia_semana")
        if not data.get("hora"):
            raise ValueError("Campo obrigatorio ausente: hora")

        try:
            dia_semana = int(data["dia_semana"])
        except (ValueError, TypeError):
            raise ValueError("Campo 'dia_semana' deve ser um numero inteiro de 0 a 6.")

        if dia_semana not in range(7):
            raise ValueError("Campo 'dia_semana' deve ser entre 0 (segunda) e 6 (domingo).")

        hora = data["hora"].strip()
        if not re.match(r"^\d{2}:\d{2}$", hora):
            raise ValueError("Campo 'hora' deve estar no formato HH:MM.")

        return AdicionarHorarioDisponivelInput(
            medico_id=medico_id,
            dia_semana=dia_semana,
            hora=hora,
        )
