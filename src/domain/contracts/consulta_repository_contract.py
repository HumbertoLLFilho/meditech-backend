from abc import ABC, abstractmethod
from src.domain.models.consulta import Consulta


class ConsultaRepositoryContract(ABC):

    @abstractmethod
    def salvar(self, consulta: Consulta) -> Consulta:
        ...

    @abstractmethod
    def listar_por_usuario(self, usuario_id: int) -> list[Consulta]:
        ...
