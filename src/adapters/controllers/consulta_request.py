from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class CadastrarConsultaRequest:
    especialidade: str
    medico: str
    data: date
    horario: str

    @staticmethod
    def from_dict(data: dict) -> "CadastrarConsultaRequest":
        campos_obrigatorios = ["especialidade", "medico", "data", "horario"]
        for campo in campos_obrigatorios:
            if not data.get(campo):
                raise ValueError(f"Campo obrigatório ausente: {campo}")

        try:
            data_consulta = datetime.strptime(data["data"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")

        return CadastrarConsultaRequest(
            especialidade=data["especialidade"],
            medico=data["medico"],
            data=data_consulta,
            horario=data["horario"]
        )
