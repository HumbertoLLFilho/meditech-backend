CONSULTA_CANCELAR_DOC = {
    "tags": ["Consultas"],
    "security": [{"BearerAuth": []}],
    "summary": "Cancelar uma consulta",
    "description": (
        "Cancela a consulta informada. "
        "O paciente dono da consulta ou um administrador podem cancelar. "
        "O campo `descricao` e opcional; quando fornecido, e salvo como "
        "documento de texto vinculado a consulta."
    ),
    "parameters": [
        {
            "in": "path",
            "name": "consulta_id",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID da consulta a ser cancelada",
        }
    ],
    "requestBody": {
        "required": False,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "descricao": {
                            "type": "string",
                            "example": "Conflito de agenda de ultima hora.",
                            "description": "Motivo do cancelamento (opcional)",
                        }
                    },
                }
            }
        },
    },
    "responses": {
        200: {
            "description": "Consulta cancelada com sucesso",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "paciente_id": {"type": "integer"},
                            "medico_id": {"type": "integer"},
                            "especialidade_id": {"type": "integer"},
                            "data_agendada": {"type": "string", "format": "date"},
                            "hora": {"type": "string"},
                            "cancelada": {"type": "boolean"},
                            "descricao_cancelamento": {
                                "type": "string",
                                "nullable": True,
                                "description": "Motivo do cancelamento, ou null se nao informado",
                            },
                            "mensagem": {"type": "string"},
                        },
                    }
                }
            },
        },
        401: {"description": "Token ausente, invalido ou expirado"},
        403: {"description": "Sem permissao para cancelar esta consulta"},
        422: {"description": "Erro de validacao (consulta nao encontrada, ja cancelada, etc.)"},
        500: {"description": "Erro interno do servidor"},
    },
}

CONSULTA_CADASTRAR_DOC = {
    "tags": ["Consultas"],
    "security": [{"BearerAuth": []}],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["medico_id", "especialidade_id", "data_agendada", "hora"],
                    "properties": {
                        "medico_id": {"type": "integer", "example": 2},
                        "especialidade_id": {"type": "integer", "example": 1},
                        "data_agendada": {
                            "type": "string",
                            "format": "date",
                            "example": "2026-04-10",
                        },
                        "hora": {"type": "string", "example": "14:30"},
                    },
                }
            }
        },
    },
    "responses": {
        201: {"description": "Consulta agendada com sucesso"},
        401: {"description": "Token ausente, invalido ou expirado"},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno do servidor"},
    },
}

CONSULTA_LISTAR_DOC = {
    "tags": ["Consultas"],
    "security": [{"BearerAuth": []}],
    "responses": {
        200: {
            "description": "Lista de consultas do paciente autenticado",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "data_agendada": {"type": "string", "format": "date", "example": "2026-04-10"},
                                "hora": {"type": "string", "example": "14:30"},
                                "cancelada": {"type": "boolean"},
                                "data_cadastrada": {"type": "string", "format": "date-time"},
                                "medico": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "nome": {"type": "string"},
                                        "sobrenome": {"type": "string"},
                                        "email": {"type": "string"},
                                        "telefone": {"type": "string"},
                                    },
                                },
                                "paciente": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "nome": {"type": "string"},
                                        "sobrenome": {"type": "string"},
                                    },
                                },
                                "especialidade": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "integer"},
                                        "nome": {"type": "string", "example": "Cardiologia"},
                                    },
                                },
                            },
                        },
                    }
                }
            },
        },
        401: {"description": "Token ausente, invalido ou expirado"},
    },
}
