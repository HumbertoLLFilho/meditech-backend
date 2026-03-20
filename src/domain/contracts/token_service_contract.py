from abc import ABC, abstractmethod


class TokenServiceContract(ABC):

    @abstractmethod
    def generate_access_token(self, user_id: int, email: str, cpf: str, nome: str, tipo: str) -> str:
        ...