from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.models.especialidade import Especialidade
    from src.domain.models.usuario import Usuario


@dataclass
class HorarioDisponivel:
    medico_id: int
    especialidade_id: int
    dia_semana: int  # 0=segunda ... 6=domingo (Python date.weekday())
    periodo: str     # "manha", "tarde" ou "noite"
    id: int | None = None
    medico: "Usuario | None" = field(default=None, compare=False)
    especialidade: "Especialidade | None" = field(default=None, compare=False)
