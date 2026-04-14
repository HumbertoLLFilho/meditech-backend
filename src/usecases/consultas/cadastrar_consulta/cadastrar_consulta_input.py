from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class CadastrarConsultaInput:
    paciente_id: int
    medico_id: int
    especialidade_id: int
    data_agendada: date
    hora: str

    @staticmethod
    def from_dict(data: dict, paciente_id: int) -> "CadastrarConsultaInput":
        campos_obrigatorios = ["medico_id", "especialidade_id", "data_agendada", "hora"]
        for campo in campos_obrigatorios:
            if not data.get(campo):
                raise ValueError(f"Campo obrigatorio ausente: {campo}")

        try:
            data_agendada = datetime.strptime(data["data_agendada"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de data invalido. Use YYYY-MM-DD.")

        try:
            medico_id = int(data["medico_id"])
            especialidade_id = int(data["especialidade_id"])
        except (ValueError, TypeError):
            raise ValueError("Campos 'medico_id' e 'especialidade_id' devem ser numeros inteiros.")

        return CadastrarConsultaInput(
            paciente_id=paciente_id,
            medico_id=medico_id,
            especialidade_id=especialidade_id,
            data_agendada=data_agendada,
            hora=data["hora"],
        )
