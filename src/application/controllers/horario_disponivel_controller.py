from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flasgger import swag_from

from src.application.docs.horarios_disponiveis_docs import (
    DISPONIBILIDADE_CONSULTAR_DOC,
    HORARIO_ADICIONAR_DOC,
    HORARIO_EXCLUIR_DOC,
    HORARIO_LISTAR_MEDICO_DOC,
)
from src.application.dependencies.container import (
    get_adicionar_horario_disponivel,
    get_consultar_disponibilidade,
    get_listar_horarios_disponivel_medico,
    get_horario_disponivel_repository,
)
from src.domain.models.usuario import TipoUsuario
from src.usecases.horarios.adicionar_horario_disponivel.adicionar_horario_disponivel_input import AdicionarHorarioDisponivelInput
from src.usecases.horarios.consultar_disponibilidade.consultar_disponibilidade_input import ConsultarDisponibilidadeInput


horario_disponivel_bp = Blueprint("horario_disponivel", __name__, url_prefix="/horarios-disponiveis")


@horario_disponivel_bp.route("", methods=["POST"])
@jwt_required()
@swag_from(HORARIO_ADICIONAR_DOC)
def adicionar_horario():
    claims = get_jwt()
    tipo = claims.get("tipo")

    if tipo == TipoUsuario.MEDICO.value:
        medico_id = int(get_jwt_identity())
    elif tipo == TipoUsuario.ADMIN.value:
        data = request.get_json(silent=True) or {}
        if not data.get("medico_id"):
            return jsonify({"erro": "Campo obrigatorio ausente: medico_id"}), 422
        try:
            medico_id = int(data["medico_id"])
        except (ValueError, TypeError):
            return jsonify({"erro": "Campo 'medico_id' deve ser um numero inteiro."}), 422
    else:
        return jsonify({"erro": "Acesso negado. Apenas medicos e admins podem cadastrar horarios."}), 403

    data = request.get_json(silent=True) or {}

    try:
        horario_input = AdicionarHorarioDisponivelInput.from_dict(data, medico_id)
        use_case = get_adicionar_horario_disponivel()
        resultado = use_case.executar(horario_input)
        return jsonify(resultado), 201

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500


@horario_disponivel_bp.route("/medico/<int:medico_id>", methods=["GET"])
@jwt_required()
@swag_from(HORARIO_LISTAR_MEDICO_DOC)
def listar_horarios_medico(medico_id: int):
    use_case = get_listar_horarios_disponivel_medico()
    resultado = use_case.listar(medico_id)
    return jsonify(resultado), 200


@horario_disponivel_bp.route("/<int:horario_id>", methods=["DELETE"])
@jwt_required()
@swag_from(HORARIO_EXCLUIR_DOC)
def excluir_horario(horario_id: int):
    claims = get_jwt()
    tipo = claims.get("tipo")

    try:
        repo = get_horario_disponivel_repository()
        horario = repo.buscar_por_id(horario_id)

        if not horario:
            return jsonify({"erro": "Horario nao encontrado."}), 422

        if tipo == TipoUsuario.MEDICO.value:
            if horario.medico_id != int(get_jwt_identity()):
                return jsonify({"erro": "Acesso negado. Voce so pode remover seus proprios horarios."}), 403
        elif tipo != TipoUsuario.ADMIN.value:
            return jsonify({"erro": "Acesso negado."}), 403

        repo.excluir(horario_id)
        return jsonify({"mensagem": "Horario removido com sucesso."}), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500


@horario_disponivel_bp.route("/disponivel", methods=["GET"])
@jwt_required()
@swag_from(DISPONIBILIDADE_CONSULTAR_DOC)
def consultar_disponibilidade():
    try:
        disponibilidade_input = ConsultarDisponibilidadeInput.from_args(request.args)
        use_case = get_consultar_disponibilidade()
        resultado = use_case.executar(disponibilidade_input)
        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500
