USUARIO_LISTAR_DOC = {
    "tags": ["Usuarios"],
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "ativo",
            "in": "query",
            "required": False,
            "schema": {"type": "boolean"},
            "description": "Filtrar por status ativo (true ou false). Apenas admins podem usar este filtro; usuarios comuns sempre veem apenas ativos.",
        },
        {
            "name": "tipo",
            "in": "query",
            "required": False,
            "schema": {
                "type": "string",
                "enum": ["admin", "medico", "paciente"],
            },
            "description": "Filtrar por tipo de usuario. Apenas admins podem usar este filtro; usuarios comuns sempre veem apenas medicos.",
        },
        {
            "name": "nome",
            "in": "query",
            "required": False,
            "schema": {"type": "string"},
            "description": "Filtrar por nome ou sobrenome (busca parcial)",
        },
        {
            "name": "cpf",
            "in": "query",
            "required": False,
            "schema": {"type": "string"},
            "description": "Filtrar por CPF (busca exata)",
        },
        {
            "name": "ordem",
            "in": "query",
            "required": False,
            "schema": {
                "type": "string",
                "enum": ["asc", "desc"],
                "default": "desc",
            },
            "description": "Ordenacao por data de cadastro (padrao: desc)",
        },
    ],
    "responses": {
        200: {"description": "Lista de usuarios"},
        401: {"description": "Token ausente, invalido ou expirado"},
        422: {"description": "Valor invalido nos filtros"},
    },
}

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

USUARIO_CADASTRAR_ADMIN_DOC = {
    "tags": ["Usuarios"],
    "security": [{"BearerAuth": []}],
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
                    ],
                    "properties": {
                        "nome": {"type": "string", "example": "Maria"},
                        "sobrenome": {"type": "string", "example": "Souza"},
                        "data_nascimento": {
                            "type": "string",
                            "format": "date",
                            "example": "1985-03-15",
                        },
                        "genero": {
                            "type": "string",
                            "enum": ["masculino", "feminino", "outro", "prefiro_nao_informar"],
                            "example": "feminino",
                        },
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "maria.admin@email.com",
                        },
                        "senha": {"type": "string", "example": "senhaSegura123"},
                        "cpf": {"type": "string", "example": "98765432100"},
                        "telefone": {"type": "string", "example": "11988887777"},
                    },
                }
            }
        },
    },
    "responses": {
        201: {"description": "Admin cadastrado com sucesso"},
        403: {"description": "Acesso negado — requer token de admin"},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno do servidor"},
        },
}

USUARIO_BUSCAR_DOC = {
    "tags": ["Usuarios"],
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID do usuario",
        }
    ],
    "responses": {
        200: {"description": "Dados completos do usuario com relacionamentos"},
        401: {"description": "Token ausente, invalido ou expirado"},
        403: {"description": "Acesso negado"},
        422: {"description": "Usuario nao encontrado"},
        500: {"description": "Erro interno do servidor"},
    },
}

USUARIO_CADASTRAR_MEDICO_DOC = {
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
                        "telefone"
                    ],
                    "properties": {
                        "nome": {"type": "string", "example": "Dr. Carlos"},
                        "sobrenome": {"type": "string", "example": "Mendes"},
                        "data_nascimento": {
                            "type": "string",
                            "format": "date",
                            "example": "1975-05-10",
                        },
                        "genero": {
                            "type": "string",
                            "enum": ["masculino", "feminino", "outro", "prefiro_nao_informar"],
                            "example": "masculino",
                        },
                        "email": {
                            "type": "string",
                            "format": "email",
                            "example": "carlos.medico@email.com",
                        },
                        "senha": {"type": "string", "example": "senhaSegura456"},
                        "cpf": {"type": "string", "example": "11223344556"},
                        "telefone": {"type": "string", "example": "11977776666"},
                        "especialidade_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "example": [1, 2],
                            "description": "IDs das especialidades a associar ao medico (opcional)",
                        },
                    },
                }
            }
        },
     },
    "responses": {
        201: {"description": "Medico cadastrado com sucesso"},
        422: {"description": "Erro de validacao ou especialidade nao encontrada"},
        500: {"description": "Erro interno do servidor"},
    },
}

USUARIO_ALTERAR_STATUS_DOC = {
    "tags": ["Usuarios"],
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "usuario_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID do usuario a ter o status alterado",
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["ativo"],
                    "properties": {
                        "ativo": {
                            "type": "boolean",
                            "example": True,
                            "description": "Novo status do usuario (true para ativo, false para inativo)",
                        },
                    },
                }
            }
        },
    },
    "responses": {
        201: {"description": "Status do usuario alterado com sucesso"},
        401: {"description": "Token ausente, invalido ou expirado"},
        403: {"description": "Acesso negado — apenas admins podem alterar status"},
        422: {"description": "Erro de validacao ou usuario nao encontrado"},
        500: {"description": "Erro interno do servidor"},
    },
}

