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
    def buscar_por_periodo(
        self, medico_id: int, especialidade_id: int, dia_semana: int, periodo: str
    ) -> "HorarioDisponivel | None":
        ...

    @abstractmethod
    def listar_medicos_por_especialidade_dia_periodo(
        self, especialidade_id: int, dia_semana: int, periodo: str
    ) -> "list[HorarioDisponivel]":
        ...

    @abstractmethod
    def listar_periodos_do_medico(self, medico_id: int, dia_semana: int) -> list[str]:
        ...

    @abstractmethod
    def buscar_por_id(self, horario_id: int) -> "HorarioDisponivel | None":
        ...

    @abstractmethod
    def excluir(self, horario_id: int) -> None:
        ...

    @abstractmethod
    def deletar_por_medico_e_especialidade(self, medico_id: int, especialidade_id: int) -> None:
        ...
