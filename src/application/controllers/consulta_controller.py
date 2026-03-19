from flask import Blueprint, jsonify, request
from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.application.docs.consultas_docs import CONSULTA_CADASTRAR_DOC, CONSULTA_LISTAR_DOC
from src.infrastructure.container import get_cadastrar_consulta_use_case, get_listar_consultas
from src.usecases.cadastrar_consulta.cadastrar_consulta_input import CadastrarConsultaInput
from src.usecases.listar_consultas.listar_consultas_input import ListarConsultasInput


consulta_bp = Blueprint("consulta", __name__)


@consulta_bp.route("/consultas", methods=["POST"])
@jwt_required()
@swag_from(CONSULTA_CADASTRAR_DOC)
def cadastrar_consulta():
    data = request.get_json(silent=True) or {}
    try:
        usuario_id = int(get_jwt_identity())

        consulta_input = CadastrarConsultaInput.from_dict(data, usuario_id)
        use_case = get_cadastrar_consulta_use_case()
        consulta = use_case.executar(consulta_input)

        return jsonify(
            {
                "especialidade": consulta.especialidade,
                "medico": consulta.medico,
                "data": consulta.data,
                "horario": consulta.horario,
                "mensagem": "Consulta realizada com sucesso!",
            }
        ), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422

    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500


@consulta_bp.route("/consultas", methods=["GET"])
@jwt_required()
@swag_from(CONSULTA_LISTAR_DOC)
def listar_consultas():
    usuario_id = int(get_jwt_identity())

    listar_input = ListarConsultasInput(usuario_id=usuario_id)
    use_case = get_listar_consultas()
    consultas = use_case.listar(listar_input)

    result = [
        {
            "especialidade": c.especialidade,
            "medico": c.medico,
            "data": c.data.strftime("%Y-%m-%d"),
            "horario": c.horario,
        }
        for c in consultas
    ]

    return jsonify(result), 200
