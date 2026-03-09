from werkzeug.security import generate_password_hash

from src.adapters.controllers.usuario_request import CadastrarUsuarioRequest
from src.application.usuario_repository_port import UsuarioRepositoryPort
from src.domain.usuario import Genero, TipoUsuario, Usuario


class CadastrarUsuarioUseCase:

    def __init__(self, repository: UsuarioRepositoryPort):
        self.repository = repository

    def executar(self, request: CadastrarUsuarioRequest) -> Usuario:
        if not request.cpf and not request.rg:
            raise ValueError("CPF ou RG deve ser informado.")

        if self.repository.buscar_por_email(request.email):
            raise ValueError("E-mail já cadastrado.")

        if request.cpf and self.repository.buscar_por_cpf(request.cpf):
            raise ValueError("CPF já cadastrado.")

        try:
            genero_enum = Genero(request.genero)
        except ValueError:
            valores = [g.value for g in Genero]
            raise ValueError(f"Gênero inválido. Valores aceitos: {valores}")

        try:
            tipo_enum = TipoUsuario(request.tipo)
        except ValueError:
            valores = [t.value for t in TipoUsuario]
            raise ValueError(f"Tipo de usuário inválido. Valores aceitos: {valores}")

        senha_hash = generate_password_hash(request.senha)

        usuario = Usuario(
            nome=request.nome,
            sobrenome=request.sobrenome,
            cpf=request.cpf,
            rg=request.rg,
            data_nascimento=request.data_nascimento,
            genero=genero_enum,
            email=request.email,
            senha=senha_hash,
            tipo=tipo_enum,
        )

        return self.repository.salvar(usuario)
