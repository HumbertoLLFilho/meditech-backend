import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


@dataclass
class EditarUsuarioInput:
    usuario_id: int
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    data_nascimento: Optional[date] = None
    genero: Optional[str] = None
    telefone: Optional[str] = None
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
    especialidade_ids: Optional[list[int]] = field(default=None)

    @staticmethod
    def from_dict(data: dict, usuario_id: int) -> "EditarUsuarioInput":
        CAMPOS_EDITAVEIS = [
            "nome", "sobrenome", "data_nascimento", "genero", "telefone",
            "cep", "logradouro", "numero", "complemento", "bairro",
            "cidade", "estado", "tipo_sanguineo", "alergias", "plano_saude",
            "especialidade_ids",
        ]

        if not any(data.get(campo) is not None for campo in CAMPOS_EDITAVEIS):
            raise ValueError("Nenhum campo editavel foi fornecido.")

        data_nascimento = None
        if data.get("data_nascimento"):
            try:
                data_nascimento = datetime.strptime(data["data_nascimento"], "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Formato de data invalido. Use YYYY-MM-DD.")

        cep = data.get("cep")
        if cep is not None and not re.match(r'^\d{8}$', str(cep)):
            raise ValueError("CEP deve conter exatamente 8 digitos numericos.")

        estado = data.get("estado")
        if estado is not None and not re.match(r'^[A-Z]{2}$', str(estado)):
            raise ValueError("Estado deve ser uma UF de 2 letras maiusculas (ex: SP, RJ).")

        tipo_sanguineo = data.get("tipo_sanguineo")
        TIPOS_VALIDOS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        if tipo_sanguineo is not None and tipo_sanguineo not in TIPOS_VALIDOS:
            raise ValueError(f"tipo_sanguineo invalido. Valores aceitos: {TIPOS_VALIDOS}")

        especialidade_ids = data.get("especialidade_ids")
        if especialidade_ids is not None:
            if not isinstance(especialidade_ids, list) or not all(isinstance(i, int) for i in especialidade_ids):
                raise ValueError("especialidade_ids deve ser uma lista de inteiros.")

        return EditarUsuarioInput(
            usuario_id=usuario_id,
            nome=data.get("nome") or None,
            sobrenome=data.get("sobrenome") or None,
            data_nascimento=data_nascimento,
            genero=data.get("genero") or None,
            telefone=data.get("telefone") or None,
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
            especialidade_ids=especialidade_ids,
        )
