HORARIO_ADICIONAR_DOC = {
    "tags": ["Horarios Disponiveis"],
    "security": [{"BearerAuth": []}],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["dia_semana", "periodo", "especialidade_id"],
                    "properties": {
                        "dia_semana": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 6,
                            "example": 1,
                            "description": "0=segunda, 1=terca, 2=quarta, 3=quinta, 4=sexta, 5=sabado, 6=domingo",
                        },
                        "periodo": {
                            "type": "string",
                            "enum": ["manha", "tarde", "noite"],
                            "example": "manha",
                            "description": "Periodo em que o medico atende neste dia",
                        },
                        "especialidade_id": {
                            "type": "integer",
                            "example": 1,
                            "description": "Especialidade para a qual o medico estara disponivel neste horario",
                        },
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
        200: {
            "description": "Lista de horarios do medico",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "especialidade_id": {"type": "integer"},
                                "especialidade_nome": {"type": "string"},
                                "dia_semana": {"type": "integer"},
                                "periodo": {"type": "string"},
                            },
                        },
                    }
                }
            },
        },
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
        200: {
            "description": "Medicos e horarios disponiveis",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "medico_id": {"type": "integer"},
                                "medico_nome": {"type": "string"},
                                "medico_sobrenome": {"type": "string"},
                                "especialidade_id": {"type": "integer"},
                                "especialidade_nome": {"type": "string"},
                                "horarios": {
                                    "type": "array",
                                    "items": {"type": "string", "example": "09:00"},
                                },
                            },
                        },
                    }
                }
            },
        },
        401: {"description": "Token ausente, invalido ou expirado"},
        422: {"description": "Parametros invalidos"},
    },
}
