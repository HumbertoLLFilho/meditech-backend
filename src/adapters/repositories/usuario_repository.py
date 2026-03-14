from src.application.usuario_repository_port import UsuarioRepositoryPort
from src.domain.usuario import Usuario
from src.infrastructure.database import db
from src.infrastructure.usuario_model import UsuarioModel


class UsuarioRepository(UsuarioRepositoryPort):

    def salvar(self, usuario: Usuario) -> Usuario:
        # Criar o modelo de usuário
        model = UsuarioModel(
            nome=usuario.nome,
            sobrenome=usuario.sobrenome,
            data_nascimento=usuario.data_nascimento,
            genero=usuario.genero.value,
            email=usuario.email,
            senha=usuario.senha,
            cpf=usuario.cpf,
        )
        db.session.add(model)
        db.session.flush()  # Para obter o ID antes de commitar

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        usuario.id = model.id
        return usuario

    def buscar_por_email(self, email: str) -> Usuario | None:
        model = UsuarioModel.query.filter_by(email=email).first()
        return model

    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        model_cpf = UsuarioModel.query.filter_by(cpf=cpf).first()
        if not model_cpf:
            return None
        return model_cpf
