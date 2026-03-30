from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.models.especialidade import Especialidade
from src.domain.models.horario_disponivel import HorarioDisponivel
from src.domain.models.usuario import Genero, TipoUsuario, Usuario
from src.infrastructure.config.database import db
from src.infrastructure.models.especialidade_model import EspecialidadeModel
from src.infrastructure.models.horario_disponivel_model import HorarioDisponivelModel
from src.infrastructure.models.usuario_model import UsuarioModel


class HorarioDisponivelRepository(HorarioDisponivelRepositoryContract):

    @staticmethod
    def _to_domain(
        model: HorarioDisponivelModel,
        medico: Usuario | None = None,
        especialidade: Especialidade | None = None,
    ) -> HorarioDisponivel:
        return HorarioDisponivel(
            id=model.id,
            medico_id=model.medico_id,
            especialidade_id=model.especialidade_id,
            dia_semana=model.dia_semana,
            periodo=model.periodo,
            medico=medico,
            especialidade=especialidade,
        )

    def salvar(self, horario: HorarioDisponivel) -> HorarioDisponivel:
        model = HorarioDisponivelModel(
            medico_id=horario.medico_id,
            especialidade_id=horario.especialidade_id,
            dia_semana=horario.dia_semana,
            periodo=horario.periodo,
        )
        db.session.add(model)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return self._to_domain(model)

    def listar_por_medico(self, medico_id: int) -> list[HorarioDisponivel]:
        rows = (
            db.session.query(HorarioDisponivelModel, EspecialidadeModel)
            .join(EspecialidadeModel, HorarioDisponivelModel.especialidade_id == EspecialidadeModel.id)
            .filter(HorarioDisponivelModel.medico_id == medico_id)
            .order_by(HorarioDisponivelModel.dia_semana, HorarioDisponivelModel.periodo)
            .all()
        )
        return [
            self._to_domain(h, especialidade=Especialidade(id=e.id, nome=e.nome))
            for h, e in rows
        ]

    def buscar_por_periodo(
        self, medico_id: int, especialidade_id: int, dia_semana: int, periodo: str
    ) -> HorarioDisponivel | None:
        model = HorarioDisponivelModel.query.filter_by(
            medico_id=medico_id,
            especialidade_id=especialidade_id,
            dia_semana=dia_semana,
            periodo=periodo,
        ).first()
        return self._to_domain(model) if model else None

    def listar_medicos_por_especialidade_dia_periodo(
        self, especialidade_id: int, dia_semana: int, periodo: str
    ) -> list[HorarioDisponivel]:
        rows = (
            db.session.query(HorarioDisponivelModel, UsuarioModel, EspecialidadeModel)
            .join(UsuarioModel, HorarioDisponivelModel.medico_id == UsuarioModel.id)
            .join(EspecialidadeModel, HorarioDisponivelModel.especialidade_id == EspecialidadeModel.id)
            .filter(
                HorarioDisponivelModel.especialidade_id == especialidade_id,
                HorarioDisponivelModel.dia_semana == dia_semana,
                HorarioDisponivelModel.periodo == periodo,
            )
            .all()
        )
        return [
            self._to_domain(
                h,
                medico=Usuario(
                    id=u.id,
                    nome=u.nome,
                    sobrenome=u.sobrenome,
                    data_nascimento=u.data_nascimento,
                    genero=Genero(u.genero),
                    email=u.email,
                    senha=u.senha,
                    cpf=u.cpf,
                    telefone=u.telefone,
                    tipo=TipoUsuario(u.tipo),
                    ativo=u.ativo,
                    data_cadastro=u.data_cadastro,
                ),
                especialidade=Especialidade(id=e.id, nome=e.nome),
            )
            for h, u, e in rows
        ]

    def listar_periodos_do_medico(self, medico_id: int, dia_semana: int) -> list[str]:
        rows = HorarioDisponivelModel.query.filter_by(
            medico_id=medico_id, dia_semana=dia_semana
        ).all()
        return [r.periodo for r in rows]

    def buscar_por_id(self, horario_id: int) -> HorarioDisponivel | None:
        model = HorarioDisponivelModel.query.get(horario_id)
        return self._to_domain(model) if model else None

    def excluir(self, horario_id: int) -> None:
        model = HorarioDisponivelModel.query.get(horario_id)
        if not model:
            raise ValueError("Horario nao encontrado.")

        db.session.delete(model)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
