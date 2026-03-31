from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flasgger import swag_from

from src.application.docs.usuarios_docs import USUARIO_BUSCAR_DOC, USUARIO_CADASTRAR_ADMIN_DOC, USUARIO_CADASTRAR_DOC, USUARIO_CADASTRAR_MEDICO_DOC, USUARIO_LISTAR_DOC
from src.application.dependencies.container import get_buscar_usuario, get_cadastrar_usuario_use_case, get_listar_usuarios
from src.usecases.buscar_usuario.buscar_usuario_input import BuscarUsuarioInput
from src.usecases.cadastrar_usuario.cadastrar_usuario_input import CadastrarUsuarioInput
from src.usecases.listar_usuarios.listar_usuarios_input import ListarUsuariosInput
from src.domain.models.usuario import TipoUsuario


usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


@usuario_bp.route("", methods=["GET"])
@jwt_required()
@swag_from(USUARIO_LISTAR_DOC)
def listar_usuarios():
    claims = get_jwt()
    is_admin = claims.get("tipo") == TipoUsuario.ADMIN.value

    try:
        if is_admin:
            listar_input = ListarUsuariosInput.from_args(request.args)
        else:
            # Usuarios comuns só veem médicos ativos; filtro "ativo" e "tipo" são ignorados
            args_filtrados = {k: v for k, v in request.args.items() if k not in ("ativo", "tipo")}
            listar_input = ListarUsuariosInput.from_args(args_filtrados)
            listar_input.ativo = True
            listar_input.tipo = TipoUsuario.MEDICO.value

        use_case = get_listar_usuarios()
        resultado = use_case.listar(listar_input)

        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500


@usuario_bp.route("", methods=["POST"])
@swag_from(USUARIO_CADASTRAR_DOC)
def cadastrar_usuario():
    data = request.get_json(silent=True) or {}

    try:
        usuario_input = CadastrarUsuarioInput.from_dict(data)
        use_case = get_cadastrar_usuario_use_case()
        resultado = use_case.executar(usuario_input, ativo=True)

        return jsonify(resultado), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500


@usuario_bp.route("/admin", methods=["POST"])
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
        resultado = use_case.executar(usuario_input, tipo=TipoUsuario.ADMIN, ativo=True)

        return jsonify(resultado), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500


@usuario_bp.route("/medico", methods=["POST"])
@swag_from(USUARIO_CADASTRAR_MEDICO_DOC)
def cadastrar_medico():
    data = request.get_json(silent=True) or {}

    try:
        usuario_input = CadastrarUsuarioInput.from_dict(data)
        use_case = get_cadastrar_usuario_use_case()
        resultado = use_case.executar(usuario_input, tipo=TipoUsuario.MEDICO, ativo=False)

        return jsonify(resultado), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500


@usuario_bp.route("/<int:usuario_id>", methods=["GET"])
@jwt_required()
@swag_from(USUARIO_BUSCAR_DOC)
def buscar_usuario(usuario_id: int):
    claims = get_jwt()
    tipo_logado = claims.get("tipo")
    id_logado = int(get_jwt_identity())

    try:
        use_case = get_buscar_usuario()
        resultado = use_case.executar(BuscarUsuarioInput(usuario_id=usuario_id))

        if resultado is None:
            return jsonify({"erro": "Usuario nao encontrado."}), 422

        is_admin = tipo_logado == TipoUsuario.ADMIN.value
        is_proprio = id_logado == usuario_id
        is_medico_ativo = (
            resultado.get("tipo") == TipoUsuario.MEDICO.value
            and resultado.get("ativo") is True
        )

        if not (is_admin or is_proprio or is_medico_ativo):
            return jsonify({"erro": "Acesso negado."}), 403

        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500
