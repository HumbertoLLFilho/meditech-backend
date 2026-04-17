from abc import ABC, abstractmethod

from src.domain.models.especialidade import Especialidade


class EspecialidadeRepositoryContract(ABC):

    @abstractmethod
    def salvar(self, especialidade: Especialidade) -> Especialidade:
        ...

    @abstractmethod
    def listar(self) -> list[Especialidade]:
        ...

    @abstractmethod
    def buscar_por_id(self, especialidade_id: int) -> Especialidade | None:
        ...

    @abstractmethod
    def listar_por_medico(self, medico_id: int) -> list[Especialidade]:
        ...

    @abstractmethod
    def associar_medico(self, medico_id: int, especialidade_id: int) -> None:
        ...

    @abstractmethod
    def definir_especialidades_medico(self, medico_id: int, especialidade_ids: list[int]) -> None:
        ...

    @abstractmethod
    def desassociar_medico(self, medico_id: int, especialidade_id: int) -> None:
        ...

    @abstractmethod
    def atualizar(self, especialidade: Especialidade) -> Especialidade:
        ...
