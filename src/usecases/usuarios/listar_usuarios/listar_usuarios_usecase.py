from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.usecases.usuarios.listar_usuarios.listar_usuarios_input import ListarUsuariosInput


class ListarUsuariosUseCase:

    def __init__(self, repository: UsuarioRepositoryContract):
        self.repository = repository

    def listar(self, input_data: ListarUsuariosInput) -> list[dict]:
        usuarios = self.repository.listar(
            ativo=input_data.ativo,
            tipo=input_data.tipo,
            nome=input_data.nome,
            cpf=input_data.cpf,
            ordem=input_data.ordem,
        )

        return [
            {
                "id": u.id,
                "nome": u.nome,
                "sobrenome": u.sobrenome,
                "email": u.email,
                "genero": u.genero,
                "tipo": u.tipo,
                "ativo": u.ativo,
                "data_cadastro": u.data_cadastro.strftime("%Y-%m-%dT%H:%M:%S") if u.data_cadastro else None,
            }
            for u in usuarios
        ]
