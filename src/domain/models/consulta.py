from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.models.especialidade import Especialidade
    from src.domain.models.usuario import Usuario


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
    medico: "Usuario | None" = field(default=None, compare=False)
    paciente: "Usuario | None" = field(default=None, compare=False)
    especialidade: "Especialidade | None" = field(default=None, compare=False)
