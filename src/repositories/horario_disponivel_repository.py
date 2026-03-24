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
            hora=model.hora,
        )

    def salvar(self, horario: HorarioDisponivel) -> HorarioDisponivel:
        model = HorarioDisponivelModel(
            medico_id=horario.medico_id,
            dia_semana=horario.dia_semana,
            hora=horario.hora,
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
            HorarioDisponivelModel.dia_semana, HorarioDisponivelModel.hora
        ).all()
        return [self._to_domain(m) for m in models]

    def listar_por_medico_e_dia(self, medico_id: int, dia_semana: int) -> list[HorarioDisponivel]:
        models = HorarioDisponivelModel.query.filter_by(
            medico_id=medico_id, dia_semana=dia_semana
        ).order_by(HorarioDisponivelModel.hora).all()
        return [self._to_domain(m) for m in models]

    def buscar(self, medico_id: int, dia_semana: int, hora: str) -> HorarioDisponivel | None:
        model = HorarioDisponivelModel.query.filter_by(
            medico_id=medico_id, dia_semana=dia_semana, hora=hora
        ).first()
        return self._to_domain(model) if model else None

    def listar_por_especialidade_e_dia(self, especialidade_id: int, dia_semana: int) -> list[HorarioDisponivel]:
        from src.infrastructure.models.especialidade_model import medico_especialidades

        models = (
            HorarioDisponivelModel.query
            .join(
                medico_especialidades,
                HorarioDisponivelModel.medico_id == medico_especialidades.c.medico_id,
            )
            .filter(
                medico_especialidades.c.especialidade_id == especialidade_id,
                HorarioDisponivelModel.dia_semana == dia_semana,
            )
            .order_by(HorarioDisponivelModel.medico_id, HorarioDisponivelModel.hora)
            .all()
        )
        return [self._to_domain(m) for m in models]

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
