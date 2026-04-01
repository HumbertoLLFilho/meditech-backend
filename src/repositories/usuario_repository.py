from sqlalchemy.orm import aliased

from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.consulta import Consulta
from src.domain.models.especialidade import Especialidade
from src.domain.models.horario_disponivel import HorarioDisponivel
from src.domain.models.usuario import Genero, TipoUsuario, Usuario
from src.infrastructure.config.database import db
from src.infrastructure.models.consulta_model import ConsultaModel
from src.infrastructure.models.especialidade_model import EspecialidadeModel
from src.infrastructure.models.horario_disponivel_model import HorarioDisponivelModel
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
            tipo=usuario.tipo,
            ativo = usuario.ativo
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

    def buscar_por_id_com_detalhes(self, usuario_id: int) -> Usuario | None:
        usuario_model = UsuarioModel.query.get(usuario_id)
        if not usuario_model:
            return None

        MedicoAlias = aliased(UsuarioModel)
        PacienteAlias = aliased(UsuarioModel)

        # consultas como paciente
        rows = (
            db.session.query(ConsultaModel, MedicoAlias, EspecialidadeModel)
            .join(MedicoAlias, ConsultaModel.medico_id == MedicoAlias.id)
            .join(EspecialidadeModel, ConsultaModel.especialidade_id == EspecialidadeModel.id)
            .filter(ConsultaModel.paciente_id == usuario_id)
            .all()
        )
        consultas_paciente = [
            Consulta(
                id=c.id,
                paciente_id=c.paciente_id,
                medico_id=c.medico_id,
                especialidade_id=c.especialidade_id,
                data_agendada=c.data_agendada,
                hora=c.hora,
                data_cadastrada=c.data_cadastrada,
                cancelada=c.cancelada,
                medico=self._to_domain(m),
                especialidade=Especialidade(id=e.id, nome=e.nome),
            )
            for c, m, e in rows
        ]

        # consultas como médico
        rows = (
            db.session.query(ConsultaModel, PacienteAlias, EspecialidadeModel)
            .join(PacienteAlias, ConsultaModel.paciente_id == PacienteAlias.id)
            .join(EspecialidadeModel, ConsultaModel.especialidade_id == EspecialidadeModel.id)
            .filter(ConsultaModel.medico_id == usuario_id)
            .all()
        )
        consultas_medico = [
            Consulta(
                id=c.id,
                paciente_id=c.paciente_id,
                medico_id=c.medico_id,
                especialidade_id=c.especialidade_id,
                data_agendada=c.data_agendada,
                hora=c.hora,
                data_cadastrada=c.data_cadastrada,
                cancelada=c.cancelada,
                paciente=self._to_domain(p),
                especialidade=Especialidade(id=e.id, nome=e.nome),
            )
            for c, p, e in rows
        ]

        # especialidades via relacionamento ORM
        especialidades = [
            Especialidade(id=e.id, nome=e.nome)
            for e in usuario_model.especialidades
        ]

        # horários disponíveis
        rows = (
            db.session.query(HorarioDisponivelModel, EspecialidadeModel)
            .join(EspecialidadeModel, HorarioDisponivelModel.especialidade_id == EspecialidadeModel.id)
            .filter(HorarioDisponivelModel.medico_id == usuario_id)
            .order_by(HorarioDisponivelModel.dia_semana, HorarioDisponivelModel.periodo)
            .all()
        )
        horarios = [
            HorarioDisponivel(
                id=h.id,
                medico_id=h.medico_id,
                especialidade_id=h.especialidade_id,
                dia_semana=h.dia_semana,
                periodo=h.periodo,
                especialidade=Especialidade(id=e.id, nome=e.nome),
            )
            for h, e in rows
        ]

        usuario = self._to_domain(usuario_model)
        usuario.consultas_como_paciente = consultas_paciente
        usuario.consultas_como_medico = consultas_medico
        usuario.especialidades = especialidades
        usuario.horarios_disponiveis = horarios
        return usuario
