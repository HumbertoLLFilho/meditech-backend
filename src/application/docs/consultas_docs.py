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
        200: {"description": "Lista de consultas do paciente autenticado"},
        401: {"description": "Token ausente, invalido ou expirado"},
    },
}
