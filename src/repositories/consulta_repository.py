from datetime import date

from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.models.consulta import Consulta
from src.infrastructure.config.database import db
from src.infrastructure.models.consulta_model import ConsultaModel


class ConsultaRepository(ConsultaRepositoryContract):

    @staticmethod
    def _to_domain(model: ConsultaModel) -> Consulta:
        return Consulta(
            id=model.id,
            paciente_id=model.paciente_id,
            medico_id=model.medico_id,
            especialidade_id=model.especialidade_id,
            data_agendada=model.data_agendada,
            hora=model.hora,
            data_cadastrada=model.data_cadastrada,
            cancelada=model.cancelada,
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

    def existe_consulta_ativa(self, medico_id: int, data_agendada: date, hora: str) -> bool:
        return ConsultaModel.query.filter_by(
            medico_id=medico_id,
            data_agendada=data_agendada,
            hora=hora,
            cancelada=False,
        ).first() is not None
