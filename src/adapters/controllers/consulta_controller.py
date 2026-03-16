import os
import jwt
from flask import Blueprint, jsonify, request
from src.adapters.controllers.consulta_request import CadastrarConsultaRequest
from src.infrastructure.container import get_cadastrar_consulta_use_case, get_listar_consultas

consulta_bp = Blueprint("consulta", __name__)


@consulta_bp.route("/consultas", methods=["POST"])
def cadastrar_consulta():
    data = request.get_json(silent=True) or {}
    try:
        auth = request.headers.get("Authorization")
        token = auth.replace("Bearer ", "")
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "secret-jullya-teste-18"), algorithms=["HS256"])
        usuario_id = int(payload["sub"])

        consulta_request = CadastrarConsultaRequest.from_dict(data)
        use_case = get_cadastrar_consulta_use_case()
        consulta = use_case.executar(consulta_request, usuario_id)

        return jsonify({
            "especialidade": consulta.especialidade,
            "medico": consulta.medico,
            "data": consulta.data,
            "horario": consulta.horario,
            "mensagem": "Consulta realizada com sucesso!"
        }), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422

    except Exception as e:
        return jsonify({
            "erro": "Erro interno no servidor",
            "detalhe": str(e)
        }), 500


@consulta_bp.route("/consultas", methods=["GET"])
def listar_consultas():
    auth = request.headers.get("Authorization")
    token = auth.replace("Bearer ", "")
    payload = jwt.decode(token, os.getenv("SECRET_KEY", "secret-jullya-teste-18"), algorithms=["HS256"])
    usuario_id = payload["sub"]

    use_case = get_listar_consultas()
    consultas = use_case.listar(usuario_id)

    result = [
        {
            "especialidade": c.especialidade,
            "medico": c.medico,
            "data": c.data.strftime("%Y-%m-%d"),
            "horario": c.horario
        } for c in consultas
    ]

    return jsonify(result), 200
