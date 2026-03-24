from dataclasses import dataclass


@dataclass
class HorarioDisponivel:
    medico_id: int
    dia_semana: int  # 0=segunda ... 6=domingo (Python date.weekday())
    hora: str        # "HH:MM"
    id: int | None = None
