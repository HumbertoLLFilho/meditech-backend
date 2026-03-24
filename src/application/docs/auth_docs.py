AUTH_LOGIN_DOC = {
    "tags": ["Auth"],
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
