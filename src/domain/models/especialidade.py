from dataclasses import dataclass


@dataclass
class Especialidade:
    nome: str
    id: int | None = None
