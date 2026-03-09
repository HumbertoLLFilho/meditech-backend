from src.application.usuario_repository_port import UsuarioRepositoryPort
from src.domain.usuario import Genero, TipoUsuario, Usuario
from src.infrastructure.database import db
from src.infrastructure.usuario_model import UsuarioModel


class UsuarioRepository(UsuarioRepositoryPort):

    def salvar(self, usuario: Usuario) -> Usuario:
        model = UsuarioModel(
            nome=usuario.nome,
            sobrenome=usuario.sobrenome,
            cpf=usuario.cpf,
            rg=usuario.rg,
            data_nascimento=usuario.data_nascimento,
            genero=usuario.genero.value,
            email=usuario.email,
            senha=usuario.senha,
            tipo=usuario.tipo.value,
        )
        db.session.add(model)
        db.session.commit()
        usuario.id = model.id
        return usuario

    def buscar_por_email(self, email: str) -> Usuario | None:
        model = UsuarioModel.query.filter_by(email=email).first()
        return self._para_dominio(model) if model else None

    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        model = UsuarioModel.query.filter_by(cpf=cpf).first()
        return self._para_dominio(model) if model else None

    def _para_dominio(self, model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            nome=model.nome,
            sobrenome=model.sobrenome,
            cpf=model.cpf,
            rg=model.rg,
            data_nascimento=model.data_nascimento,
            genero=Genero(model.genero),
            email=model.email,
            senha=model.senha,
            tipo=TipoUsuario(model.tipo),
        )
