from abc import ABC, abstractmethod
from src.domain.models.documento import Documento

class DocumentoRepositoryContract(ABC):

    @abstractmethod
    def salvar(self, documento: Documento) -> Documento:
        ...

    @abstractmethod
    def buscar_por_id(self, documento_id: int) -> Documento | None:
        ...

    @abstractmethod
    def listar_por_usuario_id(self, usuario_id: int) -> list[Documento]:
        ...

    @abstractmethod
    def buscar_por_usuario_e_tipo(self, usuario_id: int, tipo: str) -> Documento | None:
        ...

    @abstractmethod
    def deletar(self, documento_id: int) -> None:
        ...
