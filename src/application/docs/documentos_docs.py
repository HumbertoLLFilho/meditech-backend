DOCUMENTO_DOWNLOAD_DOC = {
    "tags": ["Documentos"],
    "security": [{"BearerAuth": []}],
    "summary": "Download de documento",
    "description": (
        "Retorna o conteudo binario do documento. "
        "Admin pode baixar qualquer documento; usuario comum so pode baixar os proprios."
    ),
    "parameters": [
        {
            "name": "documento_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID do documento a baixar",
        },
    ],
    "responses": {
        200: {
            "description": "Conteudo binario do arquivo",
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"}
                }
            },
        },
        401: {"description": "Token ausente, invalido ou expirado"},
        403: {"description": "Sem permissao para baixar este documento"},
        422: {"description": "Documento nao encontrado"},
        500: {"description": "Erro interno do servidor"},
    },
}
