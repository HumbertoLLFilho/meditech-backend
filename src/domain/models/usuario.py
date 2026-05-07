from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.models.consulta import Consulta
    from src.domain.models.documento import Documento
    from src.domain.models.especialidade import Especialidade
    from src.domain.models.horario_disponivel import HorarioDisponivel


class Genero(str, Enum):
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTRO = "outro"
    PREFIRO_NAO_INFORMAR = "prefiro_nao_informar"


class TipoUsuario(str, Enum):
    ADMIN = "admin"
    MEDICO = "medico"
    PACIENTE = "paciente"


class StatusAprovacao(str, Enum):
    NOVO = "novo"
    EM_ANDAMENTO = "em_andamento"
    EM_ANALISE = "em_analise"
    APROVADO = "aprovado"
    RECUSADO = "recusado"


@dataclass
class Usuario:
    nome: str
    sobrenome: str
    data_nascimento: date
    genero: Genero
    email: str
    senha: str
    telefone: str
    tipo: TipoUsuario
    ativo: bool
    cpf: str
    id: int | None = None
    data_cadastro: datetime | None = None
    status_aprovacao: "StatusAprovacao | None" = None
    consultas_como_paciente: "list[Consulta] | None" = field(default=None, compare=False)
    consultas_como_medico: "list[Consulta] | None" = field(default=None, compare=False)
    especialidades: "list[Especialidade] | None" = field(default=None, compare=False)
    horarios_disponiveis: "list[HorarioDisponivel] | None" = field(default=None, compare=False)
    documentos: "list[Documento] | None" = field(default=None, compare=False)
    cep: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    tipo_sanguineo: str | None = None
    alergias: str | None = None
    plano_saude: str | None = None
    excluido_em: datetime | None = None
