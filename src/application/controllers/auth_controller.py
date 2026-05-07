from flask import Blueprint, jsonify, request
from flasgger import swag_from

from src.application.docs.auth_docs import AUTH_LOGIN_DOC
from src.application.dependencies.container import get_login_usuario_use_case
from src.usecases.auth.login_usuario.login_usuario_input import LoginUsuarioInput
from src.usecases.auth.login_usuario.login_usuario_usecase import InvalidCredentialsError


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
@swag_from(AUTH_LOGIN_DOC)
def login():
    data = request.get_json(silent=True) or {}

    try:
        login_input = LoginUsuarioInput.from_dict(data)
        use_case = get_login_usuario_use_case()
        resultado = use_case.executar(login_input)

        return jsonify(resultado), 200

    except InvalidCredentialsError as e:
        return jsonify({"erro": str(e)}), 401
    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500
