from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from flasgger import swag_from

from src.application.docs.usuarios_docs import USUARIO_CADASTRAR_ADMIN_DOC, USUARIO_CADASTRAR_DOC, USUARIO_LOGIN_DOC
from src.application.dependencies.container import get_cadastrar_usuario_use_case, get_login_usuario_use_case
from src.usecases.cadastrar_usuario.cadastrar_usuario_input import CadastrarUsuarioInput
from src.usecases.login_usuario.login_usuario_input import LoginUsuarioInput
from src.usecases.login_usuario.login_usuario_usecase import InvalidCredentialsError
from src.domain.models.usuario import TipoUsuario


usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


@usuario_bp.route("/cadastrar", methods=["POST"])
@swag_from(USUARIO_CADASTRAR_DOC)
def cadastrar_usuario():
    data = request.get_json(silent=True) or {}

    try:
        usuario_input = CadastrarUsuarioInput.from_dict(data)
        use_case = get_cadastrar_usuario_use_case()
        usuario = use_case.executar(usuario_input)

        return jsonify(
            {
                "id": usuario.id,
                "nome": usuario.nome,
                "sobrenome": usuario.sobrenome,
                "mensagem": "Usuário cadastrado com sucesso!",
            }
        ), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500


@usuario_bp.route("/admin/cadastrar", methods=["POST"])
@jwt_required()
@swag_from(USUARIO_CADASTRAR_ADMIN_DOC)
def cadastrar_admin():
    claims = get_jwt()
    if claims.get("tipo") != TipoUsuario.ADMIN.value:
        return jsonify({"erro": "Acesso negado. Apenas admins podem cadastrar outros admins."}), 403

    data = request.get_json(silent=True) or {}

    try:
        usuario_input = CadastrarUsuarioInput.from_dict(data)
        use_case = get_cadastrar_usuario_use_case()
        usuario = use_case.executar(usuario_input, tipo=TipoUsuario.ADMIN)

        return jsonify(
            {
                "id": usuario.id,
                "nome": usuario.nome,
                "sobrenome": usuario.sobrenome,
                "mensagem": "Admin cadastrado com sucesso!",
            }
        ), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500


@usuario_bp.route("/login", methods=["POST"])
@swag_from(USUARIO_LOGIN_DOC)
def login_usuario():
    data = request.get_json(silent=True) or {}

    try:
        login_input = LoginUsuarioInput.from_dict(data)
        use_case = get_login_usuario_use_case()
        resultado = use_case.executar(login_input)

        resposta = {
            "nome": resultado["nome"],
            "access_token": resultado["access_token"],
        }

        return jsonify(resposta), 200

    except InvalidCredentialsError as e:
        return jsonify({"erro": str(e)}), 401
    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500
