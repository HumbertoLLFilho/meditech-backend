from flask import Blueprint, jsonify, request

from src.adapters.controllers.usuario_request import CadastrarUsuarioRequest
from src.infrastructure.container import get_cadastrar_usuario_use_case, get_login_usuario_use_case

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


@usuario_bp.route("/cadastrar", methods=["POST"])
def cadastrar_usuario():
    data = request.get_json(silent=True) or {}

    try:
        usuario_request = CadastrarUsuarioRequest.from_dict(data)

        use_case = get_cadastrar_usuario_use_case()

        usuario = use_case.executar(usuario_request)

        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "sobrenome": usuario.sobrenome,
            "email": usuario.email,
            "tipo": usuario.tipo.value,
            "mensagem": "Usuário cadastrado com sucesso!",
        }), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500


@usuario_bp.route("/login", methods=["POST"])
def login_usuario():
    data = request.get_json(silent=True) or {}

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "E-mail e senha são obrigatórios."}), 422

    try:
        use_case = get_login_usuario_use_case()
        resultado = use_case.executar(email, senha)

        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 401
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500
