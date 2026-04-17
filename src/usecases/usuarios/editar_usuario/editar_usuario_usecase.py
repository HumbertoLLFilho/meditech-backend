from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import TipoUsuario
from src.usecases.usuarios.editar_usuario.editar_usuario_input import EditarUsuarioInput


class EditarUsuarioUseCase:

    def __init__(
        self,
        usuario_repository: UsuarioRepositoryContract,
        especialidade_repository: EspecialidadeRepositoryContract,
    ):
        self.usuario_repository = usuario_repository
        self.especialidade_repository = especialidade_repository

    def executar(self, input_data: EditarUsuarioInput, usuario_id_logado: int, tipo_logado: str) -> dict:
        usuario = self.usuario_repository.buscar_por_id(input_data.usuario_id)
        if not usuario:
            raise ValueError("Usuario nao encontrado.")

        is_admin = tipo_logado == TipoUsuario.ADMIN.value
        is_proprio = usuario_id_logado == input_data.usuario_id

        if not is_admin and not is_proprio:
            raise ValueError("Acesso negado. Voce so pode editar seu proprio perfil.")

        if input_data.nome is not None:
            usuario.nome = input_data.nome
        if input_data.sobrenome is not None:
            usuario.sobrenome = input_data.sobrenome
        if input_data.data_nascimento is not None:
            usuario.data_nascimento = input_data.data_nascimento
        if input_data.genero is not None:
            usuario.genero = input_data.genero
        if input_data.telefone is not None:
            usuario.telefone = input_data.telefone
        if input_data.cep is not None:
            usuario.cep = input_data.cep
        if input_data.logradouro is not None:
            usuario.logradouro = input_data.logradouro
        if input_data.numero is not None:
            usuario.numero = input_data.numero
        if input_data.complemento is not None:
            usuario.complemento = input_data.complemento
        if input_data.bairro is not None:
            usuario.bairro = input_data.bairro
        if input_data.cidade is not None:
            usuario.cidade = input_data.cidade
        if input_data.estado is not None:
            usuario.estado = input_data.estado
        if input_data.tipo_sanguineo is not None:
            usuario.tipo_sanguineo = input_data.tipo_sanguineo
        if input_data.alergias is not None:
            usuario.alergias = input_data.alergias
        if input_data.plano_saude is not None:
            usuario.plano_saude = input_data.plano_saude

        usuario_atualizado = self.usuario_repository.atualizar_perfil(usuario)

        if input_data.especialidade_ids is not None:
            if usuario.tipo != TipoUsuario.MEDICO and not is_admin:
                raise ValueError("Apenas medicos ou admins podem atualizar especialidades.")

            for esp_id in input_data.especialidade_ids:
                if not self.especialidade_repository.buscar_por_id(esp_id):
                    raise ValueError(f"Especialidade com id {esp_id} nao encontrada.")

            self.especialidade_repository.definir_especialidades_medico(
                input_data.usuario_id,
                input_data.especialidade_ids,
            )

        return {
            "id": usuario_atualizado.id,
            "nome": usuario_atualizado.nome,
            "sobrenome": usuario_atualizado.sobrenome,
            "email": usuario_atualizado.email,
            "cpf": usuario_atualizado.cpf,
            "telefone": usuario_atualizado.telefone,
            "genero": usuario_atualizado.genero.value if hasattr(usuario_atualizado.genero, "value") else usuario_atualizado.genero,
            "tipo": usuario_atualizado.tipo.value if hasattr(usuario_atualizado.tipo, "value") else usuario_atualizado.tipo,
            "ativo": usuario_atualizado.ativo,
            "data_nascimento": usuario_atualizado.data_nascimento.strftime("%Y-%m-%d"),
            "cep": usuario_atualizado.cep,
            "logradouro": usuario_atualizado.logradouro,
            "numero": usuario_atualizado.numero,
            "complemento": usuario_atualizado.complemento,
            "bairro": usuario_atualizado.bairro,
            "cidade": usuario_atualizado.cidade,
            "estado": usuario_atualizado.estado,
            "tipo_sanguineo": usuario_atualizado.tipo_sanguineo,
            "alergias": usuario_atualizado.alergias,
            "plano_saude": usuario_atualizado.plano_saude,
            "mensagem": "Usuario atualizado com sucesso.",
        }
