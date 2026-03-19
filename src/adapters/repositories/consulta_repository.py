from src.application.consulta_repository_port import ConsultaRepositoryPort
from src.domain.consulta import Consulta
from src.infrastructure.database import db
from src.infrastructure.consulta_model import ConsultaModel


class ConsultaRepository(ConsultaRepositoryPort):

    def salvar(self, consulta: Consulta) -> Consulta:
        # Criar o modelo de consulta
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

        consulta.id = model.id
        return consulta


    def listar_por_usuario(self, usuario_id: int) -> list[Consulta]:
        consultas = ConsultaModel.query.filter_by(usuario_id=usuario_id).all()
        return consultas
