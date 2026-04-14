from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract


class ListarEspecialidadesMedicoUseCase:

    def __init__(self, repository: EspecialidadeRepositoryContract):
        self.repository = repository

    def listar(self, medico_id: int) -> list[dict]:
        especialidades = self.repository.listar_por_medico(medico_id)
        return [{"id": e.id, "nome": e.nome} for e in especialidades]
