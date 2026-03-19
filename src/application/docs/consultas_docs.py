CONSULTA_CADASTRAR_DOC = {
    "tags": ["Consultas"],
    "security": [{"BearerAuth": []}],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["especialidade", "medico", "data", "horario"],
                    "properties": {
                        "especialidade": {"type": "string", "example": "Cardiologia"},
                        "medico": {"type": "string", "example": "Dr. Pedro"},
                        "data": {
                            "type": "string",
                            "format": "date",
                            "example": "2026-03-25",
                        },
                        "horario": {"type": "string", "example": "14:30"},
                    },
                }
            }
        },
    },
    "responses": {
        201: {"description": "Consulta cadastrada com sucesso"},
        401: {"description": "Token ausente, invalido ou expirado"},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno do servidor"},
    },
}

CONSULTA_LISTAR_DOC = {
    "tags": ["Consultas"],
    "security": [{"BearerAuth": []}],
    "responses": {
        200: {"description": "Lista de consultas"},
        401: {"description": "Token ausente, invalido ou expirado"},
    },
}
