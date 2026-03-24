from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.models.horario_disponivel import HorarioDisponivel
from src.infrastructure.config.database import db
from src.infrastructure.models.horario_disponivel_model import HorarioDisponivelModel


class HorarioDisponivelRepository(HorarioDisponivelRepositoryContract):

    @staticmethod
    def _to_domain(model: HorarioDisponivelModel) -> HorarioDisponivel:
        return HorarioDisponivel(
            id=model.id,
            medico_id=model.medico_id,
            dia_semana=model.dia_semana,
            periodo=model.periodo,
        )

    def salvar(self, horario: HorarioDisponivel) -> HorarioDisponivel:
        model = HorarioDisponivelModel(
            medico_id=horario.medico_id,
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
        models = HorarioDisponivelModel.query.filter_by(medico_id=medico_id).order_by(
            HorarioDisponivelModel.dia_semana, HorarioDisponivelModel.periodo
        ).all()
        return [self._to_domain(m) for m in models]

    def buscar_por_periodo(
        self, medico_id: int, dia_semana: int, periodo: str
    ) -> HorarioDisponivel | None:
        model = HorarioDisponivelModel.query.filter_by(
            medico_id=medico_id, dia_semana=dia_semana, periodo=periodo
        ).first()
        return self._to_domain(model) if model else None

    def listar_medicos_por_especialidade_dia_periodo(
        self, especialidade_id: int, dia_semana: int, periodo: str
    ) -> list[int]:
        from src.infrastructure.models.especialidade_model import medico_especialidades

        rows = (
            db.session.query(HorarioDisponivelModel.medico_id)
            .join(
                medico_especialidades,
                HorarioDisponivelModel.medico_id == medico_especialidades.c.medico_id,
            )
            .filter(
                medico_especialidades.c.especialidade_id == especialidade_id,
                HorarioDisponivelModel.dia_semana == dia_semana,
                HorarioDisponivelModel.periodo == periodo,
            )
            .distinct()
            .all()
        )
        return [row.medico_id for row in rows]

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
