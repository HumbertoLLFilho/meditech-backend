from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.usecases.especialidades.excluir_especialidade.excluir_especialidade_input import ExcluirEspecialidadeInput


class ExcluirEspecialidadeUseCase:

    def __init__(self, especialidade_repository: EspecialidadeRepositoryContract):
        self.especialidade_repository = especialidade_repository

    def executar(self, input_data: ExcluirEspecialidadeInput) -> dict:
        especialidade = self.especialidade_repository.buscar_por_id(input_data.especialidade_id)
        if not especialidade:
            raise ValueError("Especialidade nao encontrada.")

        self.especialidade_repository.deletar(input_data.especialidade_id)

        return {"mensagem": "Especialidade excluida com sucesso."}
