from dataclasses import dataclass


@dataclass
class CancelarConsultaInput:
    consulta_id: int
    usuario_id: int
    descricao: str | None = None

    @staticmethod
    def from_dict(data: dict, consulta_id: int, usuario_id: int) -> "CancelarConsultaInput":
        if not isinstance(consulta_id, int) or consulta_id <= 0:
            raise ValueError("consulta_id invalido.")

        descricao = data.get("descricao")
        if descricao is not None:
            descricao = str(descricao).strip()
            if not descricao:
                descricao = None

        return CancelarConsultaInput(
            consulta_id=consulta_id,
            usuario_id=usuario_id,
            descricao=descricao,
        )
