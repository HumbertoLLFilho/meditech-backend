from abc import ABC, abstractmethod
from src.domain.consulta import Consulta


class ConsultaRepositoryPort(ABC):

    @abstractmethod
    def salvar(self, consulta: Consulta) -> Consulta:
        ...

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> list[Consulta]:
        ...
