from dataclasses import dataclass
from datetime import date


@dataclass
class Consulta:
    usuario_id: int
    especialidade: str
    medico: str
    data: date
    horario: str

