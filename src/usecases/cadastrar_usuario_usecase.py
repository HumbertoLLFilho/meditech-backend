from werkzeug.security import generate_password_hash
from src.adapters.controllers.usuario_request import CadastrarUsuarioRequest
from src.application.usuario_repository_port import UsuarioRepositoryPort
from src.domain.usuario import Genero, Usuario


class CadastrarUsuarioUseCase:

    def __init__(self, repository: UsuarioRepositoryPort):
        self.repository = repository

    def executar(self, request: CadastrarUsuarioRequest) -> Usuario:
        try:
            genero_enum = Genero(request.genero)
        except ValueError:
            valores = [g.value for g in Genero]
            raise ValueError(f"Gênero inválido. Valores aceitos: {valores}")

        if self.repository.buscar_por_email(request.email):
            raise ValueError("E-mail já cadastrado.")

        if self.repository.buscar_por_cpf(request.cpf):
            raise ValueError("CPF já cadastrado.")

        # Hash da senha
        senha_hash = generate_password_hash(request.senha)

        usuario = Usuario(
            nome=request.nome,
            sobrenome=request.sobrenome,
            data_nascimento=request.data_nascimento,
            genero=genero_enum,
            email=request.email,
            senha=senha_hash,
            cpf=request.cpf
        )

        return self.repository.salvar(usuario)
