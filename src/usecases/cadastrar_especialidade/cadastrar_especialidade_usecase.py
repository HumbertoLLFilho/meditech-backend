from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.models.especialidade import Especialidade
from src.usecases.cadastrar_especialidade.cadastrar_especialidade_input import CadastrarEspecialidadeInput


class CadastrarEspecialidadeUseCase:

    def __init__(self, repository: EspecialidadeRepositoryContract):
        self.repository = repository

    def executar(self, input_data: CadastrarEspecialidadeInput) -> dict:
        especialidade = Especialidade(nome=input_data.nome)
        salva = self.repository.salvar(especialidade)

        return {"id": salva.id, "nome": salva.nome, "mensagem": "Especialidade cadastrada com sucesso!"}
