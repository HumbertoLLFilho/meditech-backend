from src.domain.contracts.password_service_contract import PasswordServiceContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import Genero, TipoUsuario, Usuario
from src.usecases.cadastrar_usuario.cadastrar_usuario_input import CadastrarUsuarioInput


class CadastrarUsuarioUseCase:

    def __init__(self, repository: UsuarioRepositoryContract, password_service: PasswordServiceContract):
        self.repository = repository
        self.password_service = password_service

    def executar(self, input_data: CadastrarUsuarioInput, tipo: TipoUsuario = TipoUsuario.PACIENTE, ativo: bool = False) -> dict:
        
        # Validar se o genero e tipo sao validos
        try:
            genero_enum = Genero(input_data.genero)
        except ValueError:
            valores = [g.value for g in Genero]
            raise ValueError(f"Genero invalido. Valores aceitos: {valores}")

        # busca pra ver se o email ou cpf ja estao cadastrados
        if self.repository.buscar_por_email(input_data.email):
            raise ValueError("E-mail ja cadastrado.")

        if self.repository.buscar_por_cpf(input_data.cpf):
            raise ValueError("CPF ja cadastrado.")

        senha_hash = self.password_service.hash(input_data.senha)

        usuario = Usuario(
            nome=input_data.nome,
            sobrenome=input_data.sobrenome,
            data_nascimento=input_data.data_nascimento,
            genero=genero_enum,
            email=input_data.email,
            senha=senha_hash,
            cpf=input_data.cpf,
            telefone=input_data.telefone,
            tipo=tipo,
            ativo=ativo
        )

        self.repository.salvar(usuario)

        return {
            "mensagem": f"{tipo} cadastrado com sucesso!"
        }
