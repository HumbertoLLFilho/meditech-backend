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

    @abstractmethod
    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        ...

    @abstractmethod
    def listar(
        self,
        ativo: bool | None = None,
        tipo: str | None = None,
        nome: str | None = None,
        cpf: str | None = None,
        ordem: str = "desc",
    ) -> list[Usuario]:
        ...

    @abstractmethod
    def buscar_por_id_com_detalhes(self, usuario_id: int) -> Usuario | None:
        ...

    @abstractmethod
    def atualizar(self, usuario: Usuario) -> None:
        ...
