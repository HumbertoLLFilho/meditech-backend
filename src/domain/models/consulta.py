from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Consulta:
    paciente_id: int
    medico_id: int
    data_agendada: date
    hora: str
    especialidade_id: int = 0
    id: int | None = None
    data_cadastrada: datetime | None = None
    cancelada: bool = False
