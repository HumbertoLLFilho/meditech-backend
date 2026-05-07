from dataclasses import dataclass

from src.domain.models.documento import TipoDocumento


@dataclass
class UploadDocumentoInput:
    usuario_id: int
    tipo: TipoDocumento
    nome_arquivo: str
    mime_type: str
    conteudo: bytes

    @staticmethod
    def from_form(
        usuario_id: int,
        tipo_raw: str | None,
        nome_arquivo: str | None,
        mime_type: str | None,
        conteudo: bytes | None,
    ) -> "UploadDocumentoInput":
        if not tipo_raw:
            raise ValueError("Campo obrigatorio ausente: tipo")
        try:
            tipo = TipoDocumento(tipo_raw)
        except ValueError:
            valores = ", ".join(t.value for t in TipoDocumento)
            raise ValueError(f"tipo invalido. Valores aceitos: {valores}")
        if not conteudo:
            raise ValueError("Campo obrigatorio ausente: arquivo")
        if not nome_arquivo:
            raise ValueError("Campo obrigatorio ausente: nome do arquivo")
        return UploadDocumentoInput(
            usuario_id=usuario_id,
            tipo=tipo,
            nome_arquivo=nome_arquivo,
            mime_type=mime_type or "application/octet-stream",
            conteudo=conteudo,
        )
