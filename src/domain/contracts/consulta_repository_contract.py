from abc import ABC, abstractmethod
from datetime import date

from src.domain.models.consulta import Consulta


class ConsultaRepositoryContract(ABC):

    @abstractmethod
    def salvar(self, consulta: Consulta) -> Consulta:
        ...

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> list[Consulta]:
        ...

    @abstractmethod
    def existe_consulta_ativa(self, medico_id: int, data_agendada: date, hora: str) -> bool:
        ...
