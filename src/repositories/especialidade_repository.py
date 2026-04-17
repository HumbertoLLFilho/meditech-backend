from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.models.especialidade import Especialidade
from src.infrastructure.config.database import db
from src.infrastructure.models.especialidade_model import EspecialidadeModel
from src.infrastructure.models.usuario_model import UsuarioModel


class EspecialidadeRepository(EspecialidadeRepositoryContract):

    @staticmethod
    def _to_domain(model: EspecialidadeModel) -> Especialidade:
        return Especialidade(id=model.id, nome=model.nome)

    def salvar(self, especialidade: Especialidade) -> Especialidade:
        if EspecialidadeModel.query.filter_by(nome=especialidade.nome).first():
            raise ValueError(f"Especialidade '{especialidade.nome}' ja cadastrada.")

        model = EspecialidadeModel(nome=especialidade.nome)
        db.session.add(model)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return self._to_domain(model)

    def listar(self) -> list[Especialidade]:
        return [self._to_domain(m) for m in EspecialidadeModel.query.all()]

    def buscar_por_id(self, especialidade_id: int) -> Especialidade | None:
        model = EspecialidadeModel.query.get(especialidade_id)
        return self._to_domain(model) if model else None

    def listar_por_medico(self, medico_id: int) -> list[Especialidade]:
        medico = UsuarioModel.query.get(medico_id)
        if not medico:
            return []
        return [self._to_domain(e) for e in medico.especialidades]

    def associar_medico(self, medico_id: int, especialidade_id: int) -> None:
        medico = UsuarioModel.query.get(medico_id)
        especialidade = EspecialidadeModel.query.get(especialidade_id)

        if especialidade in medico.especialidades:
            raise ValueError("Especialidade ja associada a este medico.")

        medico.especialidades.append(especialidade)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def definir_especialidades_medico(self, medico_id: int, especialidade_ids: list[int]) -> None:
        medico = UsuarioModel.query.get(medico_id)
        if not medico:
            raise ValueError("Medico nao encontrado.")

        medico.especialidades.clear()
        for esp_id in especialidade_ids:
            especialidade = EspecialidadeModel.query.get(esp_id)
            if especialidade:
                medico.especialidades.append(especialidade)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
