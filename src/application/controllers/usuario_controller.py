from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from src.infrastructure.container import get_cadastrar_usuario_use_case, get_login_usuario_use_case
from src.usecases.cadastrar_usuario.cadastrar_usuario_input import CadastrarUsuarioInput
from src.usecases.login_usuario.login_usuario_input import LoginUsuarioInput


usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


@usuario_bp.route("/cadastrar", methods=["POST"])
def cadastrar_usuario():
    data = request.get_json(silent=True) or {}

    try:
        usuario_input = CadastrarUsuarioInput.from_dict(data)
        use_case = get_cadastrar_usuario_use_case()
        usuario = use_case.executar(usuario_input)

        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "sobrenome": usuario.sobrenome,
            "email": usuario.email,
            "cpf": usuario.cpf,
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
        login_input = LoginUsuarioInput(email=email, senha=senha)
        use_case = get_login_usuario_use_case()
        resultado = use_case.executar(login_input)

        token = create_access_token(
            identity=str(resultado["id"]),
            additional_claims={
                "email": resultado["email"],
                "cpf": resultado["cpf"],
                "nome": resultado["nome"],
            },
        )

        resposta = {
            "id": resultado["id"],
            "nome": resultado["nome"],
            "access_token": token,
        }

        return jsonify(resposta), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 401
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500
