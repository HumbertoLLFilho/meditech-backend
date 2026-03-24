HORARIO_ADICIONAR_DOC = {
    "tags": ["Horarios Disponiveis"],
    "security": [{"BearerAuth": []}],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["dia_semana", "hora"],
                    "properties": {
                        "dia_semana": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 6,
                            "example": 0,
                            "description": "0=segunda, 1=terca, 2=quarta, 3=quinta, 4=sexta, 5=sabado, 6=domingo",
                        },
                        "hora": {"type": "string", "example": "08:00"},
                        "medico_id": {
                            "type": "integer",
                            "example": 2,
                            "description": "Obrigatorio apenas para admins",
                        },
                    },
                }
            }
        },
    },
    "responses": {
        201: {"description": "Horario cadastrado com sucesso"},
        401: {"description": "Token ausente, invalido ou expirado"},
        403: {"description": "Acesso negado"},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno do servidor"},
    },
}

HORARIO_LISTAR_MEDICO_DOC = {
    "tags": ["Horarios Disponiveis"],
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "medico_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        200: {"description": "Lista de horarios do medico"},
        401: {"description": "Token ausente, invalido ou expirado"},
    },
}

HORARIO_EXCLUIR_DOC = {
    "tags": ["Horarios Disponiveis"],
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "horario_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
        }
    ],
    "responses": {
        200: {"description": "Horario removido com sucesso"},
        401: {"description": "Token ausente, invalido ou expirado"},
        403: {"description": "Acesso negado"},
        422: {"description": "Horario nao encontrado"},
    },
}

DISPONIBILIDADE_CONSULTAR_DOC = {
    "tags": ["Horarios Disponiveis"],
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "especialidade_id",
            "in": "query",
            "required": True,
            "schema": {"type": "integer"},
        },
        {
            "name": "data",
            "in": "query",
            "required": True,
            "schema": {"type": "string", "format": "date", "example": "2026-04-14"},
        },
        {
            "name": "periodo",
            "in": "query",
            "required": True,
            "schema": {"type": "string", "enum": ["manha", "tarde", "noite"]},
        },
    ],
    "responses": {
        200: {"description": "Medicos e horarios disponiveis"},
        401: {"description": "Token ausente, invalido ou expirado"},
        422: {"description": "Parametros invalidos"},
    },
}
