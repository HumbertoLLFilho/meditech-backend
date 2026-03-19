from src.domain.contracts.consulta_repository_contract import ConsultaRepositoryContract
from src.domain.models.consulta import Consulta
from src.infrastructure.config.database import db
from src.infrastructure.models.consulta_model import ConsultaModel


class ConsultaRepository(ConsultaRepositoryContract):

    @staticmethod
    def _to_domain(model: ConsultaModel) -> Consulta:
        return Consulta(
            id=model.id,
            usuario_id=model.usuario_id,
            especialidade=model.especialidade,
            medico=model.medico,
            data=model.data,
            horario=model.horario,
        )

    def salvar(self, consulta: Consulta) -> Consulta:
        model = ConsultaModel(
            usuario_id=consulta.usuario_id,
            especialidade=consulta.especialidade,
            medico=consulta.medico,
            data=consulta.data,
            horario=consulta.horario
        )

        db.session.add(model)
        db.session.flush()  # Para obter o ID antes de commitar

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return self._to_domain(model)

    def listar_por_usuario(self, usuario_id: int) -> list[Consulta]:
        consultas = ConsultaModel.query.filter_by(usuario_id=usuario_id).all()
        return [self._to_domain(consulta) for consulta in consultas]
