from dataclasses import dataclass

_PERIODOS_VALIDOS = {"manha", "tarde", "noite"}


@dataclass
class AdicionarHorarioDisponivelInput:
    medico_id: int
    dia_semana: int
    periodo: str

    @staticmethod
    def from_dict(data: dict, medico_id: int) -> "AdicionarHorarioDisponivelInput":
        if data.get("dia_semana") is None:
            raise ValueError("Campo obrigatorio ausente: dia_semana")
        if not data.get("periodo"):
            raise ValueError("Campo obrigatorio ausente: periodo")

        try:
            dia_semana = int(data["dia_semana"])
        except (ValueError, TypeError):
            raise ValueError("Campo 'dia_semana' deve ser um numero inteiro de 0 a 6.")

        if dia_semana not in range(7):
            raise ValueError("Campo 'dia_semana' deve ser entre 0 (segunda) e 6 (domingo).")

        periodo = data["periodo"].strip().lower()
        if periodo not in _PERIODOS_VALIDOS:
            raise ValueError("Campo 'periodo' deve ser 'manha', 'tarde' ou 'noite'.")

        return AdicionarHorarioDisponivelInput(
            medico_id=medico_id,
            dia_semana=dia_semana,
            periodo=periodo,
        )
