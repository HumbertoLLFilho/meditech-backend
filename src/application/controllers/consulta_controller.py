from flask import Blueprint, jsonify, request
from flasgger import swag_from
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from src.application.docs.consultas_docs import CONSULTA_CADASTRAR_DOC, CONSULTA_CANCELAR_DOC, CONSULTA_LISTAR_DOC
from src.application.dependencies.container import get_cadastrar_consulta_use_case, get_cancelar_consulta, get_listar_consultas
from src.usecases.consultas.cadastrar_consulta.cadastrar_consulta_input import CadastrarConsultaInput
from src.usecases.consultas.cancelar_consulta.cancelar_consulta_input import CancelarConsultaInput
from src.usecases.consultas.listar_consultas.listar_consultas_input import ListarConsultasInput


consulta_bp = Blueprint("consulta", __name__, url_prefix="/consultas")


@consulta_bp.route("", methods=["POST"])
@jwt_required()
@swag_from(CONSULTA_CADASTRAR_DOC)
def cadastrar_consulta():
    data = request.get_json(silent=True) or {}
    try:
        usuario_id = int(get_jwt_identity())

        consulta_input = CadastrarConsultaInput.from_dict(data, paciente_id=usuario_id)
        use_case = get_cadastrar_consulta_use_case()
        resultado = use_case.executar(consulta_input)

        return jsonify(resultado), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422

    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500


@consulta_bp.route("/<int:consulta_id>/cancelar", methods=["PATCH"])
@jwt_required()
@swag_from(CONSULTA_CANCELAR_DOC)
def cancelar_consulta(consulta_id: int):
    data = request.get_json(silent=True) or {}
    try:
        usuario_id = int(get_jwt_identity())
        tipo_usuario = get_jwt().get("tipo")

        consulta_input = CancelarConsultaInput.from_dict(data, consulta_id=consulta_id, usuario_id=usuario_id)
        use_case = get_cancelar_consulta()
        resultado = use_case.executar(consulta_input, tipo_usuario=tipo_usuario)

        return jsonify(resultado), 200

    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422

    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500


@consulta_bp.route("", methods=["GET"])
@jwt_required()
@swag_from(CONSULTA_LISTAR_DOC)
def listar_consultas():
    usuario_id = int(get_jwt_identity())
    tipo_usuario = get_jwt().get("tipo")

    listar_input = ListarConsultasInput(usuario_id=usuario_id, tipo_usuario=tipo_usuario)
    use_case = get_listar_consultas()
    resultado = use_case.listar(listar_input)

    return jsonify(resultado), 200
