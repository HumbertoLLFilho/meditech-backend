from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.usecases.buscar_usuario.buscar_usuario_input import BuscarUsuarioInput


class BuscarUsuarioUseCase:

    def __init__(self, repository: UsuarioRepositoryContract):
        self.repository = repository

    def executar(self, input_data: BuscarUsuarioInput) -> dict | None:
        usuario = self.repository.buscar_por_id_com_detalhes(input_data.usuario_id)
        if not usuario:
            return None

        return {
            "id": usuario.id,
            "nome": usuario.nome,
            "sobrenome": usuario.sobrenome,
            "cpf": usuario.cpf,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "genero": usuario.genero.value,
            "tipo": usuario.tipo,
            "ativo": usuario.ativo,
            "data_nascimento": usuario.data_nascimento.strftime("%Y-%m-%d"),
            "data_cadastro": (
                usuario.data_cadastro.strftime("%Y-%m-%dT%H:%M:%S")
                if usuario.data_cadastro else None
            ),
            "consultas_como_paciente": [
                {
                    "id": c.id,
                    "data_agendada": c.data_agendada.strftime("%Y-%m-%d"),
                    "hora": c.hora,
                    "cancelada": c.cancelada,
                    "data_cadastrada": (
                        c.data_cadastrada.strftime("%Y-%m-%dT%H:%M:%S")
                        if c.data_cadastrada else None
                    ),
                    "medico": {
                        "id": c.medico.id,
                        "nome": c.medico.nome,
                        "sobrenome": c.medico.sobrenome,
                        "email": c.medico.email,
                        "telefone": c.medico.telefone,
                    } if c.medico else None,
                    "especialidade": {
                        "id": c.especialidade.id,
                        "nome": c.especialidade.nome,
                    } if c.especialidade else None,
                }
                for c in (usuario.consultas_como_paciente or [])
            ],
            "consultas_como_medico": [
                {
                    "id": c.id,
                    "data_agendada": c.data_agendada.strftime("%Y-%m-%d"),
                    "hora": c.hora,
                    "cancelada": c.cancelada,
                    "data_cadastrada": (
                        c.data_cadastrada.strftime("%Y-%m-%dT%H:%M:%S")
                        if c.data_cadastrada else None
                    ),
                    "paciente": {
                        "id": c.paciente.id,
                        "nome": c.paciente.nome,
                        "sobrenome": c.paciente.sobrenome,
                    } if c.paciente else None,
                    "especialidade": {
                        "id": c.especialidade.id,
                        "nome": c.especialidade.nome,
                    } if c.especialidade else None,
                }
                for c in (usuario.consultas_como_medico or [])
            ],
            "especialidades": [
                {"id": e.id, "nome": e.nome}
                for e in (usuario.especialidades or [])
            ],
            "horarios_disponiveis": [
                {
                    "id": h.id,
                    "dia_semana": h.dia_semana,
                    "periodo": h.periodo,
                    "especialidade_id": h.especialidade_id,
                    "especialidade_nome": h.especialidade.nome if h.especialidade else None,
                }
                for h in (usuario.horarios_disponiveis or [])
            ],
            "documentos": [
                {
                    "id": d.id,
                    "tipo": d.tipo.value if hasattr(d.tipo, "value") else d.tipo,
                    "nome_arquivo": d.nome_arquivo,
                    "mime_type": d.mime_type,
                }
                for d in (usuario.documentos or [])
            ],
        }
