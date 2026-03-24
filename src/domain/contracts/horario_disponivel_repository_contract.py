from abc import ABC, abstractmethod

from src.domain.models.horario_disponivel import HorarioDisponivel


class HorarioDisponivelRepositoryContract(ABC):

    @abstractmethod
    def salvar(self, horario: HorarioDisponivel) -> HorarioDisponivel:
        ...

    @abstractmethod
    def listar_por_medico(self, medico_id: int) -> list[HorarioDisponivel]:
        ...

    @abstractmethod
    def listar_por_medico_e_dia(self, medico_id: int, dia_semana: int) -> list[HorarioDisponivel]:
        ...

    @abstractmethod
    def buscar(self, medico_id: int, dia_semana: int, hora: str) -> HorarioDisponivel | None:
        ...

    @abstractmethod
    def listar_por_especialidade_e_dia(self, especialidade_id: int, dia_semana: int) -> list[HorarioDisponivel]:
        ...

    @abstractmethod
    def buscar_por_id(self, horario_id: int) -> "HorarioDisponivel | None":
        ...

    @abstractmethod
    def excluir(self, horario_id: int) -> None:
        ...
