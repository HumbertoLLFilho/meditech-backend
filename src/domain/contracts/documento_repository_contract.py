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
