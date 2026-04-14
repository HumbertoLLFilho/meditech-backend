from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract


class ListarEspecialidadesUseCase:

    def __init__(self, repository: EspecialidadeRepositoryContract):
        self.repository = repository

    def listar(self) -> list[dict]:
        especialidades = self.repository.listar()
        return [{"id": e.id, "nome": e.nome} for e in especialidades]
