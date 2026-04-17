from io import BytesIO

from flasgger import swag_from
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from src.application.docs.documentos_docs import DOCUMENTO_DOWNLOAD_DOC, DOCUMENTO_UPLOAD_DOC
from src.application.dependencies.container import get_baixar_documento, get_upload_documento
from src.usecases.usuarios.baixar_documento.baixar_documento_input import BaixarDocumentoInput
from src.usecases.usuarios.upload_documento.upload_documento_input import UploadDocumentoInput


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


@documento_bp.route("/upload", methods=["POST"])
@jwt_required()
@swag_from(DOCUMENTO_UPLOAD_DOC)
def upload_documento():
    claims = get_jwt()
    tipo_logado = claims.get("tipo")
    id_logado = int(get_jwt_identity())

    tipo_raw = request.form.get("tipo")
    usuario_id_raw = request.form.get("usuario_id")
    usuario_id = int(usuario_id_raw) if usuario_id_raw else id_logado

    arquivo = request.files.get("arquivo")
    conteudo = arquivo.read() if arquivo else None
    nome_arquivo = arquivo.filename if arquivo else None
    mime_type = arquivo.mimetype if arquivo else None

    try:
        upload_input = UploadDocumentoInput.from_form(
            usuario_id=usuario_id,
            tipo_raw=tipo_raw,
            nome_arquivo=nome_arquivo,
            mime_type=mime_type,
            conteudo=conteudo,
        )
        use_case = get_upload_documento()
        resultado = use_case.executar(upload_input, id_logado, tipo_logado)
        return jsonify(resultado), 201

    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500
