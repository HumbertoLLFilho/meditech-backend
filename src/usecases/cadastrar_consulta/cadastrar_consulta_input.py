from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class CadastrarConsultaInput:
    usuario_id: int
    especialidade: str
    medico: str
    data: date
    horario: str

    @staticmethod
    def from_dict(data: dict, usuario_id: int) -> "CadastrarConsultaInput":
        campos_obrigatorios = ["especialidade", "medico", "data", "horario"]
        for campo in campos_obrigatorios:
            if not data.get(campo):
                raise ValueError(f"Campo obrigatorio ausente: {campo}")

        try:
            data_consulta = datetime.strptime(data["data"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de data invalido. Use YYYY-MM-DD.")

        return CadastrarConsultaInput(
            usuario_id=usuario_id,
            especialidade=data["especialidade"],
            medico=data["medico"],
            data=data_consulta,
            horario=data["horario"],
        )
