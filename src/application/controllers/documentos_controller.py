from io import BytesIO

from flasgger import swag_from
from flask import Blueprint, jsonify, send_file
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from src.application.docs.documentos_docs import DOCUMENTO_DOWNLOAD_DOC
from src.application.dependencies.container import get_baixar_documento
from src.usecases.usuarios.baixar_documento.baixar_documento_input import BaixarDocumentoInput


documento_bp = Blueprint("documentos", __name__, url_prefix="/documentos")


@documento_bp.route("/<int:documento_id>/download", methods=["GET"])
@jwt_required()
@swag_from(DOCUMENTO_DOWNLOAD_DOC)
def baixar_documento(documento_id: int):
    claims = get_jwt()
    tipo_logado = claims.get("tipo")
    id_logado = int(get_jwt_identity())

    try:
        baixar_input = BaixarDocumentoInput(
            usuario_id=id_logado,
            tipo_solicitante=tipo_logado,
            documento_id=documento_id,
        )
        use_case = get_baixar_documento()
        resultado = use_case.executar(baixar_input)

        return send_file(
            BytesIO(resultado["conteudo"]),
            mimetype=resultado["mime_type"],
            as_attachment=True,
            download_name=resultado["nome_arquivo"],
        )

    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500
