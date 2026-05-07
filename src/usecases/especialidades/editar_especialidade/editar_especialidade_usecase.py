from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.usecases.especialidades.editar_especialidade.editar_especialidade_input import EditarEspecialidadeInput


class EditarEspecialidadeUseCase:

    def __init__(self, especialidade_repository: EspecialidadeRepositoryContract):
        self.especialidade_repository = especialidade_repository

    def executar(self, input_data: EditarEspecialidadeInput) -> dict:
        especialidade = self.especialidade_repository.buscar_por_id(input_data.especialidade_id)
        if not especialidade:
            raise ValueError("Especialidade nao encontrada.")

        especialidade.nome = input_data.nome
        atualizada = self.especialidade_repository.atualizar(especialidade)

        return {"id": atualizada.id, "nome": atualizada.nome}
