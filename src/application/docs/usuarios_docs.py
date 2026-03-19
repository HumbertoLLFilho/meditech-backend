USUARIO_CADASTRAR_DOC = {
    "tags": ["Usuarios"],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": [
                        "nome",
                        "sobrenome",
                        "data_nascimento",
                        "genero",
                        "email",
                        "senha",
                        "cpf",
                        "telefone",
                        "tipo"
                    ],
                    "properties": {
                        "nome": {"type": "string", "example": "Joao"},
                        "sobrenome": {"type": "string", "example": "Silva"},
                        "data_nascimento": {
                            "type": "string",
                            "format": "date",
                            "example": "1999-10-23",
                        },
                        "genero": {
                            "type": "string",
                            "enum": ["masculino", "feminino", "outro", "prefiro_nao_informar"],
                            "example": "masculino",
                        },
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "joao@email.com",
                        },
                        "senha": {"type": "string", "example": "senha123"},
                        "cpf": {"type": "string", "example": "12345678901"},
                        "telefone": {"type": "string", "example": "11999999999"}
                    },
                }
            }
        },
    },
    "responses": {
        201: {"description": "Usuario cadastrado com sucesso"},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno do servidor"},
    },
}

USUARIO_LOGIN_DOC = {
    "tags": ["Usuarios"],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["email", "senha"],
                    "properties": {
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "joao@email.com",
                        },
                        "senha": {"type": "string", "example": "senha123"},
                    },
                }
            }
        },
    },
    "responses": {
        200: {"description": "Login realizado com sucesso"},
        401: {"description": "Credenciais invalidas"},
        422: {"description": "Campos obrigatorios ausentes"},
        500: {"description": "Erro interno do servidor"},
    },
}
