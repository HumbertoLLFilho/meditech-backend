from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from flasgger import swag_from

from src.application.docs.especialidades_docs import (
    ESPECIALIDADE_ASSOCIAR_MEDICO_DOC,
    ESPECIALIDADE_CADASTRAR_DOC,
    ESPECIALIDADE_LISTAR_DOC,
    ESPECIALIDADE_LISTAR_MEDICO_DOC,
)
from src.application.dependencies.container import (
    get_associar_especialidade_medico,
    get_cadastrar_especialidade,
    get_listar_especialidades,
    get_listar_especialidades_medico,
)
from src.domain.models.usuario import TipoUsuario
from src.usecases.cadastrar_especialidade.cadastrar_especialidade_input import CadastrarEspecialidadeInput
from src.usecases.associar_especialidade_medico.associar_especialidade_medico_input import AssociarEspecialidadeMedicoInput


especialidade_bp = Blueprint("especialidade", __name__, url_prefix="/especialidades")


@especialidade_bp.route("", methods=["GET"])
@jwt_required()
@swag_from(ESPECIALIDADE_LISTAR_DOC)
def listar_especialidades():
    use_case = get_listar_especialidades()
    resultado = use_case.listar()
    return jsonify(resultado), 200


@especialidade_bp.route("", methods=["POST"])
@jwt_required()
@swag_from(ESPECIALIDADE_CADASTRAR_DOC)
def cadastrar_especialidade():
    claims = get_jwt()
    if claims.get("tipo") != TipoUsuario.ADMIN.value:
        return jsonify({"erro": "Acesso negado. Apenas admins podem cadastrar especialidades."}), 403

    data = request.get_json(silent=True) or {}

    try:
        especialidade_input = CadastrarEspecialidadeInput.from_dict(data)
        use_case = get_cadastrar_especialidade()
        resultado = use_case.executar(especialidade_input)
        return jsonify(resultado), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500


@especialidade_bp.route("/medico/<int:medico_id>", methods=["GET"])
@jwt_required()
@swag_from(ESPECIALIDADE_LISTAR_MEDICO_DOC)
def listar_especialidades_medico(medico_id: int):
    use_case = get_listar_especialidades_medico()
    resultado = use_case.listar(medico_id)
    return jsonify(resultado), 200


@especialidade_bp.route("/medico/<int:medico_id>", methods=["POST"])
@jwt_required()
@swag_from(ESPECIALIDADE_ASSOCIAR_MEDICO_DOC)
def associar_especialidade_medico(medico_id: int):
    claims = get_jwt()
    if claims.get("tipo") != TipoUsuario.ADMIN.value:
        return jsonify({"erro": "Acesso negado. Apenas admins podem associar especialidades."}), 403

    data = request.get_json(silent=True) or {}

    try:
        associar_input = AssociarEspecialidadeMedicoInput.from_dict(data, medico_id)
        use_case = get_associar_especialidade_medico()
        resultado = use_case.executar(associar_input)
        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500
