from abc import ABC, abstractmethod

from src.domain.models.usuario import Usuario


class TokenServiceContract(ABC):

    @abstractmethod
    def generate_access_token(self, usuario: Usuario) -> str:
        ...