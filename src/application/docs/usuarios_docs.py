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
        200: {
            "description": "Lista de usuarios",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "nome": {"type": "string"},
                                "sobrenome": {"type": "string"},
                                "email": {"type": "string"},
                                "genero": {"type": "string"},
                                "tipo": {"type": "string"},
                                "ativo": {"type": "boolean"},
                                "status_aprovacao": {
                                    "type": "string",
                                    "enum": ["novo", "em_andamento", "em_analise", "aprovado", "recusado"],
                                    "nullable": True,
                                    "description": "Status de aprovacao (apenas para medicos; null para outros tipos)",
                                },
                                "data_cadastro": {"type": "string", "format": "date-time"},
                            },
                        },
                    }
                }
            },
        },
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
                        "tipo",
                        "cep",
                        "logradouro",
                        "numero",
                        "bairro",
                        "cidade",
                        "estado",
                        "tipo_sanguineo"
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
                        "telefone": {"type": "string", "example": "11999999999"},
                        "cep": {"type": "string", "example": "01310100", "description": "CEP com 8 dígitos numéricos"},
                        "logradouro": {"type": "string", "example": "Avenida Paulista"},
                        "numero": {"type": "string", "example": "1000"},
                        "complemento": {"type": "string", "example": "Apto 52", "description": "Opcional"},
                        "bairro": {"type": "string", "example": "Bela Vista"},
                        "cidade": {"type": "string", "example": "São Paulo"},
                        "estado": {"type": "string", "example": "SP", "description": "UF com 2 letras maiúsculas"},
                        "tipo_sanguineo": {
                            "type": "string",
                            "enum": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                            "example": "O+",
                        },
                        "alergias": {"type": "string", "example": "Penicilina, dipirona", "description": "Opcional"},
                        "plano_saude": {"type": "string", "example": "Unimed", "description": "Opcional"},
                    },
                }
            }
        },
    },
    "responses": {
        201: {
            "description": "Usuario cadastrado com sucesso",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "mensagem": {"type": "string"},
                            "id": {"type": "integer"},
                            "tipo": {"type": "string"},
                            "ativo": {"type": "boolean"},
                            "status_aprovacao": {
                                "type": "string",
                                "nullable": True,
                                "description": "Sempre null para pacientes",
                            },
                        },
                    }
                }
            },
        },
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
        201: {
            "description": "Admin cadastrado com sucesso",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "mensagem": {"type": "string"},
                            "id": {"type": "integer"},
                            "tipo": {"type": "string"},
                            "ativo": {"type": "boolean"},
                            "status_aprovacao": {"type": "string", "nullable": True},
                        },
                    }
                }
            },
        },
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
                        "telefone",
                        "cep",
                        "logradouro",
                        "numero",
                        "bairro",
                        "cidade",
                        "estado"
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
                        "cep": {"type": "string", "example": "01310100", "description": "CEP com 8 dígitos numéricos"},
                        "logradouro": {"type": "string", "example": "Rua das Flores"},
                        "numero": {"type": "string", "example": "200"},
                        "complemento": {"type": "string", "example": "Sala 5", "description": "Opcional"},
                        "bairro": {"type": "string", "example": "Centro"},
                        "cidade": {"type": "string", "example": "Campinas"},
                        "estado": {"type": "string", "example": "SP", "description": "UF com 2 letras maiúsculas"},
                        "especialidade_ids": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "example": [1, 2],
                            "description": "IDs das especialidades a associar ao medico (opcional)",
                        },
                        "sobre_mim": {
                            "type": "string",
                            "example": "Especialista em cardiologia com 10 anos de experiencia.",
                            "description": "Texto livre sobre o medico (opcional)",
                        },
                        "documentos": {
                            "type": "array",
                            "description": "Lista de documentos do medico (CRM e/ou curriculo, opcional)",
                            "items": {
                                "type": "object",
                                "required": ["tipo", "nome_arquivo", "mime_type", "conteudo_base64"],
                                "properties": {
                                    "tipo": {
                                        "type": "string",
                                        "enum": ["crm", "curriculo"],
                                        "example": "crm",
                                    },
                                    "nome_arquivo": {
                                        "type": "string",
                                        "example": "crm.pdf",
                                    },
                                    "mime_type": {
                                        "type": "string",
                                        "example": "application/pdf",
                                    },
                                    "conteudo_base64": {
                                        "type": "string",
                                        "description": "Conteudo do arquivo codificado em base64",
                                    },
                                },
                            },
                        },
                    },
                }
            }
        },
     },
    "responses": {
        201: {
            "description": "Medico cadastrado com sucesso",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "mensagem": {"type": "string"},
                            "id": {"type": "integer"},
                            "tipo": {"type": "string"},
                            "ativo": {"type": "boolean"},
                            "status_aprovacao": {
                                "type": "string",
                                "enum": ["novo", "em_andamento", "em_analise", "aprovado", "recusado"],
                                "description": "Status de aprovacao do medico (inicia como 'novo')",
                            },
                        },
                    }
                }
            },
        },
        422: {"description": "Erro de validacao, base64 invalido ou especialidade nao encontrada"},
        500: {"description": "Erro interno do servidor"},
    },
}

USUARIO_ALTERAR_STATUS_DOC = {
    "tags": ["Usuarios"],
    "security": [{"BearerAuth": []}],
    "summary": "Alterar status de aprovacao de um usuario (admin only)",
    "description": (
        "Permite que um admin altere o status de aprovacao de um medico. "
        "Quando o status for 'aprovado', o campo ativo e automaticamente definido como true, "
        "liberando acesso completo ao sistema. Para os demais status, ativo fica false e o "
        "medico so consegue acessar o proprio perfil."
    ),
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
                    "required": ["status_aprovacao"],
                    "properties": {
                        "status_aprovacao": {
                            "type": "string",
                            "enum": ["novo", "em_andamento", "em_analise", "aprovado", "recusado"],
                            "example": "em_analise",
                            "description": "Novo status de aprovacao do medico",
                        },
                    },
                }
            }
        },
    },
    "responses": {
        200: {
            "description": "Status alterado com sucesso",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "mensagem": {"type": "string"},
                            "usuario_id": {"type": "integer"},
                            "status_aprovacao": {
                                "type": "string",
                                "enum": ["novo", "em_andamento", "em_analise", "aprovado", "recusado"],
                            },
                            "ativo": {"type": "boolean"},
                        },
                    }
                }
            },
        },
        401: {"description": "Token ausente, invalido ou expirado"},
        403: {"description": "Acesso negado — apenas admins podem alterar status"},
        422: {"description": "Erro de validacao, status invalido ou usuario nao encontrado"},
        500: {"description": "Erro interno do servidor"},
    },
}

