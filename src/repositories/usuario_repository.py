from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import Genero, Usuario
from src.infrastructure.config.database import db
from src.infrastructure.models.usuario_model import UsuarioModel


class UsuarioRepository(UsuarioRepositoryContract):

    @staticmethod
    def _to_domain(model: UsuarioModel) -> Usuario:
        return Usuario(
            id=model.id,
            nome=model.nome,
            sobrenome=model.sobrenome,
            data_nascimento=model.data_nascimento,
            genero=Genero(model.genero),
            email=model.email,
            senha=model.senha,
            cpf=model.cpf,
            telefone=model.telefone,
            tipo=model.tipo,
            ativo=model.ativo,
            data_cadastro=model.data_cadastro,
        )

    def salvar(self, usuario: Usuario) -> Usuario:
        model = UsuarioModel(
            nome=usuario.nome,
            sobrenome=usuario.sobrenome,
            data_nascimento=usuario.data_nascimento,
            genero=usuario.genero,
            email=usuario.email,
            senha=usuario.senha,
            cpf=usuario.cpf,
            telefone=usuario.telefone,
            tipo=usuario.tipo
        )
        db.session.add(model)
        db.session.flush()  # Para obter o ID antes de commitar

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return self._to_domain(model)

    def buscar_por_email(self, email: str) -> Usuario | None:
        model = UsuarioModel.query.filter_by(email=email).first()
        if not model:
            return None
        return self._to_domain(model)

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        model = UsuarioModel.query.get(usuario_id)
        if not model:
            return None
        return self._to_domain(model)

    def buscar_por_cpf(self, cpf: str) -> Usuario | None:
        model_cpf = UsuarioModel.query.filter_by(cpf=cpf).first()
        if not model_cpf:
            return None
        return self._to_domain(model_cpf)

    def listar(
        self,
        ativo: bool | None = None,
        tipo: str | None = None,
        nome: str | None = None,
        cpf: str | None = None,
        ordem: str = "desc",
    ) -> list[Usuario]:
        query = UsuarioModel.query

        if ativo is not None:
            query = query.filter(UsuarioModel.ativo == ativo)
        if tipo is not None:
            query = query.filter(UsuarioModel.tipo == tipo)
        if cpf is not None:
            query = query.filter(UsuarioModel.cpf == cpf)
        if nome is not None:
            termo = f"%{nome}%"
            query = query.filter(
                db.or_(
                    UsuarioModel.nome.ilike(termo),
                    UsuarioModel.sobrenome.ilike(termo),
                )
            )

        ordenacao = UsuarioModel.data_cadastro.asc() if ordem == "asc" else UsuarioModel.data_cadastro.desc()
        query = query.order_by(ordenacao)

        return [self._to_domain(m) for m in query.all()]
