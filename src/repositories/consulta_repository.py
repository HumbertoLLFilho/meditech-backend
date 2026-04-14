from datetime import date

from sqlalchemy.orm import aliased

from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.models.consulta import Consulta
from src.domain.models.especialidade import Especialidade
from src.domain.models.usuario import Genero, Usuario
from src.infrastructure.config.database import db
from src.infrastructure.models.consulta_model import ConsultaModel
from src.infrastructure.models.especialidade_model import EspecialidadeModel
from src.infrastructure.models.usuario_model import UsuarioModel


class ConsultaRepository(ConsultaRepositoryContract):

    @staticmethod
    def _to_domain(
        model: ConsultaModel,
        medico: Usuario | None = None,
        paciente: Usuario | None = None,
        especialidade: Especialidade | None = None,
    ) -> Consulta:
        return Consulta(
            id=model.id,
            paciente_id=model.paciente_id,
            medico_id=model.medico_id,
            especialidade_id=model.especialidade_id,
            data_agendada=model.data_agendada,
            hora=model.hora,
            data_cadastrada=model.data_cadastrada,
            cancelada=model.cancelada,
            descricao_cancelamento=model.descricao_cancelamento,
            medico=medico,
            paciente=paciente,
            especialidade=especialidade,
        )

    def salvar(self, consulta: Consulta) -> Consulta:
        model = ConsultaModel(
            paciente_id=consulta.paciente_id,
            medico_id=consulta.medico_id,
            especialidade_id=consulta.especialidade_id,
            data_agendada=consulta.data_agendada,
            hora=consulta.hora,
        )

        db.session.add(model)
        db.session.flush()

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return self._to_domain(model)

    def listar_por_usuario(self, usuario_id: int) -> list[Consulta]:
        consultas = ConsultaModel.query.filter_by(paciente_id=usuario_id).all()
        return [self._to_domain(c) for c in consultas]

    def listar_por_medico_e_data(self, medico_id: int, data_agendada: date) -> list[Consulta]:
        models = ConsultaModel.query.filter_by(
            medico_id=medico_id,
            data_agendada=data_agendada,
            cancelada=False,
        ).all()
        return [self._to_domain(m) for m in models]

    def buscar_por_id(self, consulta_id: int) -> Consulta | None:
        model = ConsultaModel.query.get(consulta_id)
        if not model:
            return None
        return self._to_domain(model)

    def cancelar(self, consulta_id: int, descricao: str | None = None) -> Consulta:
        model = ConsultaModel.query.get(consulta_id)
        if not model:
            raise ValueError("Consulta nao encontrada.")
        model.cancelada = True
        model.descricao_cancelamento = descricao
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return self._to_domain(model)

    def listar_por_usuario_com_detalhes(self, usuario_id: int) -> list[Consulta]:
        MedicoAlias = aliased(UsuarioModel)
        PacienteAlias = aliased(UsuarioModel)

        rows = (
            db.session.query(ConsultaModel, MedicoAlias, PacienteAlias, EspecialidadeModel)
            .join(MedicoAlias, ConsultaModel.medico_id == MedicoAlias.id)
            .join(PacienteAlias, ConsultaModel.paciente_id == PacienteAlias.id)
            .join(EspecialidadeModel, ConsultaModel.especialidade_id == EspecialidadeModel.id)
            .filter(ConsultaModel.paciente_id == usuario_id)
            .all()
        )

        return [
            self._to_domain(
                c,
                medico=Usuario(
                    id=m.id,
                    nome=m.nome,
                    sobrenome=m.sobrenome,
                    data_nascimento=m.data_nascimento,
                    genero=Genero(m.genero),
                    email=m.email,
                    senha=m.senha,
                    cpf=m.cpf,
                    telefone=m.telefone,
                    tipo=m.tipo,
                    ativo=m.ativo,
                    data_cadastro=m.data_cadastro,
                ),
                paciente=Usuario(
                    id=p.id,
                    nome=p.nome,
                    sobrenome=p.sobrenome,
                    data_nascimento=p.data_nascimento,
                    genero=Genero(p.genero),
                    email=p.email,
                    senha=p.senha,
                    cpf=p.cpf,
                    telefone=p.telefone,
                    tipo=p.tipo,
                    ativo=p.ativo,
                    data_cadastro=p.data_cadastro,
                ),
                especialidade=Especialidade(id=e.id, nome=e.nome),
            )
            for c, m, p, e in rows
        ]
