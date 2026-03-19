from abc import ABC, abstractmethod
from src.domain.models.usuario import Usuario


class UsuarioRepositoryContract(ABC):

    @abstractmethod
    def salvar(self, usuario: Usuario) -> Usuario:
        ...

    @abstractmethod
    def buscar_por_email(self, email: str) -> Usuario | None:
        ...

    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        ...
