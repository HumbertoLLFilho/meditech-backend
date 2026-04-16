import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from src.domain.models.documento import TipoDocumento


@dataclass
class DocumentoInput:
    tipo: str
    nome_arquivo: str
    mime_type: str
    conteudo_base64: str


@dataclass
class CadastrarUsuarioInput:
    nome: str
    sobrenome: str
    data_nascimento: date
    genero: str
    email: str
    senha: str
    cpf: str
    telefone: str
    sobre_mim: Optional[str] = None
    especialidade_ids: Optional[list[int]] = field(default=None)
    documentos: Optional[list[DocumentoInput]] = field(default=None)
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    tipo_sanguineo: Optional[str] = None
    alergias: Optional[str] = None
    plano_saude: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> "CadastrarUsuarioInput":
        campos_obrigatorios = ["nome", "sobrenome", "data_nascimento", "genero", "email", "senha", "cpf", "telefone"]
        for campo in campos_obrigatorios:
            if not data.get(campo):
                raise ValueError(f"Campo obrigatorio ausente: {campo}")

        try:
            data_nascimento = datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Formato de data invalido. Use YYYY-MM-DD.")

        especialidade_ids = data.get("especialidade_ids")
        if especialidade_ids is not None:
            if not isinstance(especialidade_ids, list) or not all(isinstance(i, int) for i in especialidade_ids):
                raise ValueError("especialidade_ids deve ser uma lista de inteiros.")

        documentos_data = data.get("documentos", [])
        documentos = []
        for doc in documentos_data:
            if not all(k in doc for k in ("tipo", "nome_arquivo", "mime_type", "conteudo_base64")):
                raise ValueError("Cada documento deve conter os campos: tipo, nome_arquivo, mime_type, conteudo_base64.")
            
            documentos.append(DocumentoInput(
                tipo=doc["tipo"],
                nome_arquivo=doc["nome_arquivo"],
                mime_type=doc["mime_type"],
                conteudo_base64=doc["conteudo_base64"],
            ))

        cep = data.get("cep")
        if cep is not None and not re.match(r'^\d{8}$', str(cep)):
            raise ValueError("CEP deve conter exatamente 8 dígitos numéricos.")

        estado = data.get("estado")
        if estado is not None and not re.match(r'^[A-Z]{2}$', str(estado)):
            raise ValueError("Estado deve ser uma UF de 2 letras maiúsculas (ex: SP, RJ).")

        tipo_sanguineo = data.get("tipo_sanguineo")
        TIPOS_VALIDOS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if tipo_sanguineo is not None and tipo_sanguineo not in TIPOS_VALIDOS:
            raise ValueError(f"tipo_sanguineo invalido. Valores aceitos: {TIPOS_VALIDOS}")

        return CadastrarUsuarioInput(
            nome=data["nome"],
            sobrenome=data["sobrenome"],
            data_nascimento=data_nascimento,
            genero=data["genero"],
            email=data["email"],
            senha=data["senha"],
            cpf=data["cpf"],
            telefone=data["telefone"],
            sobre_mim=data.get("sobre_mim") or None,
            especialidade_ids=especialidade_ids,
            documentos=documentos if documentos else None,
            cep=cep,
            logradouro=data.get("logradouro") or None,
            numero=data.get("numero") or None,
            complemento=data.get("complemento") or None,
            bairro=data.get("bairro") or None,
            cidade=data.get("cidade") or None,
            estado=estado,
            tipo_sanguineo=tipo_sanguineo,
            alergias=data.get("alergias") or None,
            plano_saude=data.get("plano_saude") or None,
        )
