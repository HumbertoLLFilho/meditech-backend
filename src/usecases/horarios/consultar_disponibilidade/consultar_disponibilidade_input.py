from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class ConsultarDisponibilidadeInput:
    especialidade_id: int
    data: date
    periodo: str

    @staticmethod
    def from_args(args: dict) -> "ConsultarDisponibilidadeInput":
        if not args.get("especialidade_id"):
            raise ValueError("Parametro obrigatorio ausente: especialidade_id")
        if not args.get("data"):
            raise ValueError("Parametro obrigatorio ausente: data")
        if not args.get("periodo"):
            raise ValueError("Parametro obrigatorio ausente: periodo")

        try:
            especialidade_id = int(args["especialidade_id"])
        except (ValueError, TypeError):
            raise ValueError("Parametro 'especialidade_id' deve ser um numero inteiro.")

        try:
            data = datetime.strptime(args["data"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Parametro 'data' deve estar no formato YYYY-MM-DD.")

        periodo = args["periodo"].lower()
        if periodo not in ("manha", "tarde", "noite"):
            raise ValueError("Parametro 'periodo' deve ser 'manha', 'tarde' ou 'noite'.")

        return ConsultarDisponibilidadeInput(
            especialidade_id=especialidade_id,
            data=data,
            periodo=periodo,
        )
