from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class DocumentoRequest:
    tipo: str
    numero: str


@dataclass
class CadastrarUsuarioRequest:
    nome: str
    sobrenome: str
    data_nascimento: date
    genero: str
    email: str
    senha: str
    tipo: str
    documentos: list[DocumentoRequest]

    @staticmethod
    def from_dict(data: dict) -> "CadastrarUsuarioRequest":
        campos_obrigatorios = ["nome", "sobrenome", "data_nascimento", "genero", "email", "senha"]
        for campo in campos_obrigatorios:
            if not data.get(campo):
                raise ValueError(f"Campo obrigatório ausente: {campo}")

        try:
            data_nascimento = datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de data inválido. Use YYYY-MM-DD.")

        # Validar documentos
        documentos_data = data.get("documentos", [])
        if not documentos_data:
            raise ValueError("Pelo menos um documento (CPF, RG, etc) deve ser informado.")

        documentos = []
        for doc in documentos_data:
            if not doc.get("tipo") or not doc.get("numero"):
                raise ValueError("Cada documento deve ter 'tipo' e 'numero'.")
            documentos.append(DocumentoRequest(tipo=doc["tipo"], numero=doc["numero"]))

        return CadastrarUsuarioRequest(
            nome=data["nome"],
            sobrenome=data["sobrenome"],
            data_nascimento=data_nascimento,
            genero=data["genero"],
            email=data["email"],
            senha=data["senha"],
            tipo=data.get("tipo", "paciente"),
            documentos=documentos,
        )
