ESPECIALIDADE_CADASTRAR_DOC = {
    "tags": ["Especialidades"],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["nome"],
                    "properties": {
                        "nome": {"type": "string", "example": "Cardiologia"},
                    },
                }
            }
        },
    },
    "responses": {
        201: {"description": "Especialidade cadastrada com sucesso"},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno do servidor"},
    },
}

ESPECIALIDADE_LISTAR_DOC = {
    "tags": ["Especialidades"],
    "security": [{"Bearer": []}],
    "responses": {
        200: {"description": "Lista de especialidades"},
        401: {"description": "Token ausente ou expirado"},
    },
}

ESPECIALIDADE_LISTAR_MEDICO_DOC = {
    "tags": ["Especialidades"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "medico_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID do medico",
        }
    ],
    "responses": {
        200: {"description": "Lista de especialidades do medico"},
        401: {"description": "Token ausente ou expirado"},
    },
}

ESPECIALIDADE_ASSOCIAR_MEDICO_DOC = {
    "tags": ["Especialidades"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "medico_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID do medico",
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["especialidade_id"],
                    "properties": {
                        "especialidade_id": {"type": "integer", "example": 1},
                    },
                }
            }
        },
    },
    "responses": {
        200: {"description": "Especialidade associada ao medico com sucesso"},
        401: {"description": "Token ausente ou expirado"},
        403: {"description": "Acesso negado. Apenas admins."},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno do servidor"},
    },
}

ESPECIALIDADE_DESASSOCIAR_MEDICO_DOC = {
    "tags": ["Especialidades"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "medico_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID do medico",
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["especialidade_id"],
                    "properties": {
                        "especialidade_id": {"type": "integer", "example": 1},
                    },
                }
            }
        },
    },
    "responses": {
        200: {"description": "Especialidade desassociada e horarios removidos com sucesso"},
        403: {"description": "Acesso negado. Apenas admins."},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno"},
    },
}
