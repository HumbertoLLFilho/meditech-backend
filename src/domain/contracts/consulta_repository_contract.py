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
    def listar_por_medico_e_data(self, medico_id: int, data_agendada: date) -> list[Consulta]:
        ...

    @abstractmethod
    def listar_por_usuario_com_detalhes(self, usuario_id: int) -> list[Consulta]:
        ...

    @abstractmethod
    def buscar_por_id(self, consulta_id: int) -> Consulta | None:
        ...

    @abstractmethod
    def cancelar(self, consulta_id: int, descricao: str | None = None) -> Consulta:
        ...
