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
