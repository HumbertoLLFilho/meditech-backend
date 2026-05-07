# Gaps de Funcionalidade — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implementar 6 novos endpoints que cobrem os 5 gaps de funcionalidade identificados no MediTech Backend.

**Architecture:** Cada feature segue o padrão já estabelecido: Contract → Repository → UseCase (com Input DTO) → Container (injeção de dependência) → Controller → Swagger Doc. Nenhuma abstração nova é introduzida. Os use cases não importam Flask. A validação de entrada fica nos DTOs (`from_dict`/método estático), que levantam `ValueError` em caso de dados inválidos.

**Tech Stack:** Python 3.12, Flask 3.0, SQLAlchemy, PostgreSQL, Flask-JWT-Extended, Flasgger.

---

## Mapa de arquivos

| Arquivo | Ação |
|---------|------|
| `src/domain/models/usuario.py` | + campo `excluido_em: datetime | None` |
| `src/infrastructure/models/usuario_model.py` | + coluna `excluido_em` |
| `src/infrastructure/models/consulta_model.py` | `especialidade_id` muda para `nullable=True, ondelete='SET NULL'` |
| `src/domain/contracts/usuario_repository_contract.py` | + `atualizar_senha`, `excluir` |
| `src/domain/contracts/especialidade_repository_contract.py` | + `desassociar_medico`, `atualizar`, `deletar` |
| `src/domain/contracts/horario_disponivel_repository_contract.py` | + `deletar_por_medico_e_especialidade` |
| `src/repositories/usuario_repository.py` | implementações + filtro `excluido_em` |
| `src/repositories/especialidade_repository.py` | implementações de `desassociar_medico`, `atualizar`, `deletar` |
| `src/repositories/horario_disponivel_repository.py` | implementação de `deletar_por_medico_e_especialidade` |
| `src/usecases/usuarios/alterar_senha/alterar_senha_input.py` | novo |
| `src/usecases/usuarios/alterar_senha/alterar_senha_usecase.py` | novo |
| `src/usecases/usuarios/excluir_conta/excluir_conta_input.py` | novo |
| `src/usecases/usuarios/excluir_conta/excluir_conta_usecase.py` | novo |
| `src/usecases/usuarios/upload_documento/upload_documento_input.py` | novo |
| `src/usecases/usuarios/upload_documento/upload_documento_usecase.py` | novo |
| `src/usecases/especialidades/desassociar_especialidade_medico/desassociar_especialidade_medico_input.py` | novo |
| `src/usecases/especialidades/desassociar_especialidade_medico/desassociar_especialidade_medico_usecase.py` | novo |
| `src/usecases/especialidades/editar_especialidade/editar_especialidade_input.py` | novo |
| `src/usecases/especialidades/editar_especialidade/editar_especialidade_usecase.py` | novo |
| `src/usecases/especialidades/excluir_especialidade/excluir_especialidade_input.py` | novo |
| `src/usecases/especialidades/excluir_especialidade/excluir_especialidade_usecase.py` | novo |
| `src/application/dependencies/container.py` | + 6 getters |
| `src/application/controllers/usuario_controller.py` | + rotas `PATCH /senha`, `DELETE /<id>` |
| `src/application/controllers/especialidade_controller.py` | + rotas `DELETE /medico/<id>`, `PUT /<id>`, `DELETE /<id>` |
| `src/application/controllers/documentos_controller.py` | + rota `POST /upload` |
| `src/application/docs/usuarios_docs.py` | + `USUARIO_ALTERAR_SENHA_DOC`, `USUARIO_EXCLUIR_DOC` |
| `src/application/docs/especialidades_docs.py` | + `ESPECIALIDADE_DESASSOCIAR_MEDICO_DOC`, `ESPECIALIDADE_EDITAR_DOC`, `ESPECIALIDADE_EXCLUIR_DOC` |
| `src/application/docs/documentos_docs.py` | + `DOCUMENTO_UPLOAD_DOC` |
| `tests/integration/test_gaps_funcionalidade.py` | novo — testes de integração |

---

## Task 1: Preparação — campo `excluido_em` no modelo e FK nullable em consulta

**Files:**
- Modify: `src/domain/models/usuario.py`
- Modify: `src/infrastructure/models/usuario_model.py`
- Modify: `src/infrastructure/models/consulta_model.py`
- Modify: `src/repositories/usuario_repository.py`

- [ ] **Step 1: Adicionar `excluido_em` ao domínio `Usuario`**

Em `src/domain/models/usuario.py`, após o campo `plano_saude`, adicionar:

```python
excluido_em: "datetime | None" = None
```

O arquivo completo da seção de campos do dataclass ficará:
```python
@dataclass
class Usuario:
    nome: str
    sobrenome: str
    data_nascimento: date
    genero: Genero
    email: str
    senha: str
    telefone: str
    tipo: TipoUsuario
    ativo: bool
    cpf: str
    id: int | None = None
    data_cadastro: datetime | None = None
    status_aprovacao: "StatusAprovacao | None" = None
    consultas_como_paciente: "list[Consulta] | None" = field(default=None, compare=False)
    consultas_como_medico: "list[Consulta] | None" = field(default=None, compare=False)
    especialidades: "list[Especialidade] | None" = field(default=None, compare=False)
    horarios_disponiveis: "list[HorarioDisponivel] | None" = field(default=None, compare=False)
    documentos: "list[Documento] | None" = field(default=None, compare=False)
    cep: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    estado: str | None = None
    tipo_sanguineo: str | None = None
    alergias: str | None = None
    plano_saude: str | None = None
    excluido_em: datetime | None = None
```

- [ ] **Step 2: Adicionar coluna ao `UsuarioModel`**

Em `src/infrastructure/models/usuario_model.py`, após `plano_saude`, adicionar:

```python
excluido_em = db.Column(db.DateTime, nullable=True, default=None)
```

- [ ] **Step 3: Tornar `especialidade_id` nullable em `ConsultaModel`**

Em `src/infrastructure/models/consulta_model.py`, alterar a linha 14:

```python
# Antes:
especialidade_id = db.Column(db.Integer, db.ForeignKey("especialidades.id"), nullable=False)

# Depois:
especialidade_id = db.Column(db.Integer, db.ForeignKey("especialidades.id", ondelete="SET NULL"), nullable=True)
```

Isso garante que ao excluir uma especialidade, o PostgreSQL seta `especialidade_id = NULL` nas consultas sem apagá-las.

- [ ] **Step 4: Atualizar `_to_domain` e filtros no `UsuarioRepository`**

Em `src/repositories/usuario_repository.py`:

No método `_to_domain`, adicionar `excluido_em=model.excluido_em,` ao construtor `Usuario(...)`.

No método `buscar_por_email`, trocar:
```python
model = UsuarioModel.query.filter_by(email=email).first()
```
por:
```python
model = UsuarioModel.query.filter_by(email=email).filter(UsuarioModel.excluido_em.is_(None)).first()
```

No método `listar`, adicionar antes dos filtros opcionais:
```python
query = query.filter(UsuarioModel.excluido_em.is_(None))
```

- [ ] **Step 5: Recriar o banco de dados**

```bash
docker compose down -v
docker compose up --build
```

Aguardar a API subir (`http://localhost:5000/apidocs` acessível). O `db.create_all()` cria as colunas novas automaticamente.

- [ ] **Step 6: Commit**

```bash
git add src/domain/models/usuario.py src/infrastructure/models/usuario_model.py src/infrastructure/models/consulta_model.py src/repositories/usuario_repository.py
git commit -m "feat: add excluido_em soft-delete field to usuario; make consulta.especialidade_id nullable"
```

---

## Task 2: Alterar senha — `PATCH /usuarios/<id>/senha`

**Files:**
- Create: `src/usecases/usuarios/alterar_senha/alterar_senha_input.py`
- Create: `src/usecases/usuarios/alterar_senha/alterar_senha_usecase.py`
- Modify: `src/domain/contracts/usuario_repository_contract.py`
- Modify: `src/repositories/usuario_repository.py`
- Modify: `src/application/dependencies/container.py`
- Modify: `src/application/controllers/usuario_controller.py`
- Modify: `src/application/docs/usuarios_docs.py`

- [ ] **Step 1: Criar o DTO de input**

Criar `src/usecases/usuarios/alterar_senha/alterar_senha_input.py`:

```python
from dataclasses import dataclass


@dataclass
class AlterarSenhaInput:
    usuario_id: int
    nova_senha: str
    senha_atual: str | None

    @staticmethod
    def from_dict(data: dict, usuario_id: int) -> "AlterarSenhaInput":
        nova_senha = data.get("nova_senha")
        if not nova_senha:
            raise ValueError("Campo obrigatorio ausente: nova_senha")
        if len(nova_senha) < 6:
            raise ValueError("nova_senha deve ter pelo menos 6 caracteres")
        return AlterarSenhaInput(
            usuario_id=usuario_id,
            nova_senha=nova_senha,
            senha_atual=data.get("senha_atual"),
        )
```

- [ ] **Step 2: Criar o use case**

Criar `src/usecases/usuarios/alterar_senha/alterar_senha_usecase.py`:

```python
from src.domain.contracts.password_service_contract import PasswordServiceContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import TipoUsuario
from src.usecases.usuarios.alterar_senha.alterar_senha_input import AlterarSenhaInput


class AlterarSenhaUseCase:

    def __init__(
        self,
        usuario_repository: UsuarioRepositoryContract,
        password_service: PasswordServiceContract,
    ):
        self.usuario_repository = usuario_repository
        self.password_service = password_service

    def executar(self, input_data: AlterarSenhaInput, id_logado: int, tipo_logado: str) -> dict:
        usuario = self.usuario_repository.buscar_por_id(input_data.usuario_id)
        if not usuario:
            raise ValueError("Usuario nao encontrado.")

        is_admin = tipo_logado == TipoUsuario.ADMIN.value
        is_proprio = id_logado == input_data.usuario_id

        if not is_admin and not is_proprio:
            raise PermissionError("Acesso negado.")

        if not is_admin:
            if not input_data.senha_atual:
                raise ValueError("Campo obrigatorio ausente: senha_atual")
            if not self.password_service.verify(input_data.senha_atual, usuario.senha):
                raise ValueError("Senha atual incorreta.")

        nova_hash = self.password_service.hash(input_data.nova_senha)
        self.usuario_repository.atualizar_senha(input_data.usuario_id, nova_hash)

        return {"mensagem": "Senha alterada com sucesso."}
```

- [ ] **Step 3: Adicionar método ao contrato**

Em `src/domain/contracts/usuario_repository_contract.py`, adicionar ao final da classe:

```python
    @abstractmethod
    def atualizar_senha(self, usuario_id: int, nova_senha_hash: str) -> None:
        ...
```

- [ ] **Step 4: Implementar no repositório**

Em `src/repositories/usuario_repository.py`, adicionar o método ao final da classe:

```python
    def atualizar_senha(self, usuario_id: int, nova_senha_hash: str) -> None:
        model = UsuarioModel.query.get(usuario_id)
        if not model:
            raise ValueError("Usuario nao encontrado.")
        model.senha = nova_senha_hash
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
```

- [ ] **Step 5: Adicionar getter ao container**

Em `src/application/dependencies/container.py`, adicionar import:

```python
from src.usecases.usuarios.alterar_senha.alterar_senha_usecase import AlterarSenhaUseCase
```

E adicionar a função ao final:

```python
def get_alterar_senha_use_case() -> AlterarSenhaUseCase:
    return _scoped(
        "alterar_senha_use_case",
        lambda: AlterarSenhaUseCase(
            _get_usuario_repository(),
            _get_password_service(),
        ),
    )
```

- [ ] **Step 6: Adicionar rota ao controller**

Em `src/application/controllers/usuario_controller.py`, adicionar import no topo:

```python
from src.application.docs.usuarios_docs import ..., USUARIO_ALTERAR_SENHA_DOC
from src.application.dependencies.container import ..., get_alterar_senha_use_case
from src.usecases.usuarios.alterar_senha.alterar_senha_input import AlterarSenhaInput
```

Adicionar rota ao final do arquivo:

```python
@usuario_bp.route("/<int:usuario_id>/senha", methods=["PATCH"])
@jwt_required()
@swag_from(USUARIO_ALTERAR_SENHA_DOC)
def alterar_senha(usuario_id: int):
    claims = get_jwt()
    id_logado = int(get_jwt_identity())
    tipo_logado = claims.get("tipo")

    data = request.get_json(silent=True) or {}

    try:
        alterar_input = AlterarSenhaInput.from_dict(data, usuario_id)
        use_case = get_alterar_senha_use_case()
        resultado = use_case.executar(alterar_input, id_logado, tipo_logado)
        return jsonify(resultado), 200

    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500
```

- [ ] **Step 7: Adicionar Swagger doc**

Em `src/application/docs/usuarios_docs.py`, adicionar ao final:

```python
USUARIO_ALTERAR_SENHA_DOC = {
    "tags": ["Usuarios"],
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "usuario_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID do usuario",
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["nova_senha"],
                    "properties": {
                        "senha_atual": {"type": "string", "description": "Obrigatorio para o proprio usuario; ignorado para admin"},
                        "nova_senha": {"type": "string", "minLength": 6},
                    },
                }
            }
        },
    },
    "responses": {
        200: {"description": "Senha alterada com sucesso"},
        403: {"description": "Acesso negado"},
        422: {"description": "Erro de validacao (senha atual incorreta, nova senha curta, usuario nao encontrado)"},
        500: {"description": "Erro interno"},
    },
}
```

- [ ] **Step 8: Criar `__init__.py` na pasta do use case**

```bash
touch src/usecases/usuarios/alterar_senha/__init__.py
```

- [ ] **Step 9: Commit**

```bash
git add src/usecases/usuarios/alterar_senha/ src/domain/contracts/usuario_repository_contract.py src/repositories/usuario_repository.py src/application/dependencies/container.py src/application/controllers/usuario_controller.py src/application/docs/usuarios_docs.py
git commit -m "feat: add PATCH /usuarios/<id>/senha endpoint (alterar senha)"
```

---

## Task 3: Excluir conta — `DELETE /usuarios/<id>` (soft delete)

**Files:**
- Create: `src/usecases/usuarios/excluir_conta/excluir_conta_input.py`
- Create: `src/usecases/usuarios/excluir_conta/excluir_conta_usecase.py`
- Modify: `src/domain/contracts/usuario_repository_contract.py`
- Modify: `src/repositories/usuario_repository.py`
- Modify: `src/application/dependencies/container.py`
- Modify: `src/application/controllers/usuario_controller.py`
- Modify: `src/application/docs/usuarios_docs.py`

- [ ] **Step 1: Criar o DTO de input**

Criar `src/usecases/usuarios/excluir_conta/excluir_conta_input.py`:

```python
from dataclasses import dataclass


@dataclass
class ExcluirContaInput:
    usuario_id: int

    @staticmethod
    def from_dict(usuario_id: int) -> "ExcluirContaInput":
        if not usuario_id:
            raise ValueError("Campo obrigatorio ausente: usuario_id")
        return ExcluirContaInput(usuario_id=usuario_id)
```

- [ ] **Step 2: Criar o use case**

Criar `src/usecases/usuarios/excluir_conta/excluir_conta_usecase.py`:

```python
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.usuario import TipoUsuario
from src.usecases.usuarios.excluir_conta.excluir_conta_input import ExcluirContaInput


class ExcluirContaUseCase:

    def __init__(self, usuario_repository: UsuarioRepositoryContract):
        self.usuario_repository = usuario_repository

    def executar(self, input_data: ExcluirContaInput, id_logado: int, tipo_logado: str) -> dict:
        usuario = self.usuario_repository.buscar_por_id(input_data.usuario_id)
        if not usuario:
            raise ValueError("Usuario nao encontrado.")

        is_admin = tipo_logado == TipoUsuario.ADMIN.value
        is_proprio = id_logado == input_data.usuario_id

        if not is_admin and not is_proprio:
            raise PermissionError("Acesso negado.")

        if is_admin and is_proprio:
            raise ValueError("Admin nao pode excluir a propria conta.")

        self.usuario_repository.excluir(input_data.usuario_id)

        return {"mensagem": "Conta excluida com sucesso."}
```

- [ ] **Step 3: Adicionar método ao contrato**

Em `src/domain/contracts/usuario_repository_contract.py`, adicionar:

```python
    @abstractmethod
    def excluir(self, usuario_id: int) -> None:
        ...
```

- [ ] **Step 4: Implementar no repositório**

Em `src/repositories/usuario_repository.py`, adicionar import no topo:

```python
from datetime import datetime
```

Adicionar método ao final da classe:

```python
    def excluir(self, usuario_id: int) -> None:
        model = UsuarioModel.query.get(usuario_id)
        if not model:
            raise ValueError("Usuario nao encontrado.")
        model.excluido_em = datetime.utcnow()
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
```

- [ ] **Step 5: Adicionar getter ao container**

Em `src/application/dependencies/container.py`, adicionar import:

```python
from src.usecases.usuarios.excluir_conta.excluir_conta_usecase import ExcluirContaUseCase
```

Adicionar função:

```python
def get_excluir_conta_use_case() -> ExcluirContaUseCase:
    return _scoped(
        "excluir_conta_use_case",
        lambda: ExcluirContaUseCase(_get_usuario_repository()),
    )
```

- [ ] **Step 6: Adicionar rota ao controller**

Em `src/application/controllers/usuario_controller.py`, adicionar imports e rota:

```python
# Adicionar aos imports
from src.application.docs.usuarios_docs import ..., USUARIO_EXCLUIR_DOC
from src.application.dependencies.container import ..., get_excluir_conta_use_case
from src.usecases.usuarios.excluir_conta.excluir_conta_input import ExcluirContaInput


@usuario_bp.route("/<int:usuario_id>", methods=["DELETE"])
@jwt_required()
@swag_from(USUARIO_EXCLUIR_DOC)
def excluir_usuario(usuario_id: int):
    claims = get_jwt()
    id_logado = int(get_jwt_identity())
    tipo_logado = claims.get("tipo")

    try:
        excluir_input = ExcluirContaInput.from_dict(usuario_id)
        use_case = get_excluir_conta_use_case()
        resultado = use_case.executar(excluir_input, id_logado, tipo_logado)
        return jsonify(resultado), 200

    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500
```

- [ ] **Step 7: Adicionar Swagger doc**

Em `src/application/docs/usuarios_docs.py`:

```python
USUARIO_EXCLUIR_DOC = {
    "tags": ["Usuarios"],
    "security": [{"BearerAuth": []}],
    "parameters": [
        {
            "name": "usuario_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID do usuario a excluir",
        }
    ],
    "responses": {
        200: {"description": "Conta excluida com sucesso (soft delete)"},
        403: {"description": "Acesso negado"},
        422: {"description": "Usuario nao encontrado ou admin tentando excluir a propria conta"},
        500: {"description": "Erro interno"},
    },
}
```

- [ ] **Step 8: Criar `__init__.py`**

```bash
touch src/usecases/usuarios/excluir_conta/__init__.py
```

- [ ] **Step 9: Commit**

```bash
git add src/usecases/usuarios/excluir_conta/ src/domain/contracts/usuario_repository_contract.py src/repositories/usuario_repository.py src/application/dependencies/container.py src/application/controllers/usuario_controller.py src/application/docs/usuarios_docs.py
git commit -m "feat: add DELETE /usuarios/<id> endpoint (soft delete)"
```

---

## Task 4: Upload de documento pós-cadastro — `POST /documentos/upload`

**Files:**
- Create: `src/usecases/usuarios/upload_documento/upload_documento_input.py`
- Create: `src/usecases/usuarios/upload_documento/upload_documento_usecase.py`
- Modify: `src/application/dependencies/container.py`
- Modify: `src/application/controllers/documentos_controller.py`
- Modify: `src/application/docs/documentos_docs.py`

- [ ] **Step 1: Criar o DTO de input**

Criar `src/usecases/usuarios/upload_documento/upload_documento_input.py`:

```python
from dataclasses import dataclass

from src.domain.models.documento import TipoDocumento


@dataclass
class UploadDocumentoInput:
    usuario_id: int
    tipo: TipoDocumento
    nome_arquivo: str
    mime_type: str
    conteudo: bytes

    @staticmethod
    def from_form(
        usuario_id: int,
        tipo_raw: str | None,
        nome_arquivo: str | None,
        mime_type: str | None,
        conteudo: bytes | None,
    ) -> "UploadDocumentoInput":
        if not tipo_raw:
            raise ValueError("Campo obrigatorio ausente: tipo")
        try:
            tipo = TipoDocumento(tipo_raw)
        except ValueError:
            valores = ", ".join(t.value for t in TipoDocumento)
            raise ValueError(f"tipo invalido. Valores aceitos: {valores}")
        if not conteudo:
            raise ValueError("Campo obrigatorio ausente: arquivo")
        if not nome_arquivo:
            raise ValueError("Campo obrigatorio ausente: nome do arquivo")
        return UploadDocumentoInput(
            usuario_id=usuario_id,
            tipo=tipo,
            nome_arquivo=nome_arquivo,
            mime_type=mime_type or "application/octet-stream",
            conteudo=conteudo,
        )
```

- [ ] **Step 2: Criar o use case**

Criar `src/usecases/usuarios/upload_documento/upload_documento_usecase.py`:

```python
from src.domain.contracts.documento_repository_contract import DocumentoRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.domain.models.documento import Documento
from src.domain.models.usuario import TipoUsuario
from src.usecases.usuarios.upload_documento.upload_documento_input import UploadDocumentoInput


class UploadDocumentoUseCase:

    def __init__(
        self,
        documento_repository: DocumentoRepositoryContract,
        usuario_repository: UsuarioRepositoryContract,
    ):
        self.documento_repository = documento_repository
        self.usuario_repository = usuario_repository

    def executar(self, input_data: UploadDocumentoInput, id_logado: int, tipo_logado: str) -> dict:
        is_admin = tipo_logado == TipoUsuario.ADMIN.value
        is_proprio = id_logado == input_data.usuario_id

        if not is_admin and not is_proprio:
            raise PermissionError("Acesso negado.")

        usuario = self.usuario_repository.buscar_por_id(input_data.usuario_id)
        if not usuario:
            raise ValueError("Usuario nao encontrado.")

        documento = Documento(
            usuario_id=input_data.usuario_id,
            tipo=input_data.tipo,
            nome_arquivo=input_data.nome_arquivo,
            mime_type=input_data.mime_type,
            conteudo=input_data.conteudo,
        )
        salvo = self.documento_repository.salvar(documento)

        return {
            "id": salvo.id,
            "tipo": salvo.tipo.value,
            "nome_arquivo": salvo.nome_arquivo,
            "usuario_id": salvo.usuario_id,
        }
```

- [ ] **Step 3: Adicionar getter ao container**

Em `src/application/dependencies/container.py`, adicionar import:

```python
from src.usecases.usuarios.upload_documento.upload_documento_usecase import UploadDocumentoUseCase
```

Adicionar função:

```python
def get_upload_documento() -> UploadDocumentoUseCase:
    return _scoped(
        "upload_documento_use_case",
        lambda: UploadDocumentoUseCase(
            _get_documento_repository(),
            _get_usuario_repository(),
        ),
    )
```

- [ ] **Step 4: Adicionar rota ao controller**

Em `src/application/controllers/documentos_controller.py`, adicionar imports e rota:

```python
# Adicionar aos imports existentes
from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from src.application.docs.documentos_docs import DOCUMENTO_DOWNLOAD_DOC, DOCUMENTO_UPLOAD_DOC
from src.application.dependencies.container import get_baixar_documento, get_upload_documento
from src.usecases.usuarios.upload_documento.upload_documento_input import UploadDocumentoInput


@documento_bp.route("/upload", methods=["POST"])
@jwt_required()
@swag_from(DOCUMENTO_UPLOAD_DOC)
def upload_documento():
    claims = get_jwt()
    tipo_logado = claims.get("tipo")
    id_logado = int(get_jwt_identity())

    tipo_raw = request.form.get("tipo")
    usuario_id_raw = request.form.get("usuario_id")
    usuario_id = int(usuario_id_raw) if usuario_id_raw else id_logado

    arquivo = request.files.get("arquivo")
    conteudo = arquivo.read() if arquivo else None
    nome_arquivo = arquivo.filename if arquivo else None
    mime_type = arquivo.mimetype if arquivo else None

    try:
        upload_input = UploadDocumentoInput.from_form(
            usuario_id=usuario_id,
            tipo_raw=tipo_raw,
            nome_arquivo=nome_arquivo,
            mime_type=mime_type,
            conteudo=conteudo,
        )
        use_case = get_upload_documento()
        resultado = use_case.executar(upload_input, id_logado, tipo_logado)
        return jsonify(resultado), 201

    except PermissionError as e:
        return jsonify({"erro": str(e)}), 403
    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception as e:
        return jsonify({"erro": "Erro interno no servidor.", "detalhe": str(e)}), 500
```

- [ ] **Step 5: Adicionar Swagger doc**

Em `src/application/docs/documentos_docs.py`, adicionar:

```python
DOCUMENTO_UPLOAD_DOC = {
    "tags": ["Documentos"],
    "security": [{"BearerAuth": []}],
    "consumes": ["multipart/form-data"],
    "requestBody": {
        "required": True,
        "content": {
            "multipart/form-data": {
                "schema": {
                    "type": "object",
                    "required": ["tipo", "arquivo"],
                    "properties": {
                        "tipo": {
                            "type": "string",
                            "enum": ["crm", "curriculo", "sobre_mim"],
                            "description": "Tipo do documento",
                        },
                        "arquivo": {
                            "type": "string",
                            "format": "binary",
                            "description": "Arquivo a ser enviado",
                        },
                        "usuario_id": {
                            "type": "integer",
                            "description": "ID do usuario destinatario (apenas admin pode especificar; padrao: usuario logado)",
                        },
                    },
                }
            }
        },
    },
    "responses": {
        201: {"description": "Documento enviado com sucesso"},
        403: {"description": "Acesso negado"},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno"},
    },
}
```

- [ ] **Step 6: Criar `__init__.py`**

```bash
touch src/usecases/usuarios/upload_documento/__init__.py
```

- [ ] **Step 7: Commit**

```bash
git add src/usecases/usuarios/upload_documento/ src/application/dependencies/container.py src/application/controllers/documentos_controller.py src/application/docs/documentos_docs.py
git commit -m "feat: add POST /documentos/upload endpoint"
```

---

## Task 5: Desassociar especialidade do médico — `DELETE /especialidades/medico/<id>`

**Files:**
- Create: `src/usecases/especialidades/desassociar_especialidade_medico/desassociar_especialidade_medico_input.py`
- Create: `src/usecases/especialidades/desassociar_especialidade_medico/desassociar_especialidade_medico_usecase.py`
- Modify: `src/domain/contracts/especialidade_repository_contract.py`
- Modify: `src/domain/contracts/horario_disponivel_repository_contract.py`
- Modify: `src/repositories/especialidade_repository.py`
- Modify: `src/repositories/horario_disponivel_repository.py`
- Modify: `src/application/dependencies/container.py`
- Modify: `src/application/controllers/especialidade_controller.py`
- Modify: `src/application/docs/especialidades_docs.py`

- [ ] **Step 1: Criar DTO de input**

Criar `src/usecases/especialidades/desassociar_especialidade_medico/desassociar_especialidade_medico_input.py`:

```python
from dataclasses import dataclass


@dataclass
class DesassociarEspecialidadeMedicoInput:
    medico_id: int
    especialidade_id: int

    @staticmethod
    def from_dict(data: dict, medico_id: int) -> "DesassociarEspecialidadeMedicoInput":
        especialidade_id = data.get("especialidade_id")
        if not especialidade_id:
            raise ValueError("Campo obrigatorio ausente: especialidade_id")
        try:
            especialidade_id = int(especialidade_id)
        except (TypeError, ValueError):
            raise ValueError("especialidade_id deve ser um inteiro")
        return DesassociarEspecialidadeMedicoInput(
            medico_id=medico_id,
            especialidade_id=especialidade_id,
        )
```

- [ ] **Step 2: Criar o use case**

Criar `src/usecases/especialidades/desassociar_especialidade_medico/desassociar_especialidade_medico_usecase.py`:

```python
from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.domain.contracts.horario_disponivel_repository_contract import HorarioDisponivelRepositoryContract
from src.domain.contracts.usuario_repository_contract import UsuarioRepositoryContract
from src.usecases.especialidades.desassociar_especialidade_medico.desassociar_especialidade_medico_input import DesassociarEspecialidadeMedicoInput


class DesassociarEspecialidadeMedicoUseCase:

    def __init__(
        self,
        especialidade_repository: EspecialidadeRepositoryContract,
        usuario_repository: UsuarioRepositoryContract,
        horario_disponivel_repository: HorarioDisponivelRepositoryContract,
    ):
        self.especialidade_repository = especialidade_repository
        self.usuario_repository = usuario_repository
        self.horario_disponivel_repository = horario_disponivel_repository

    def executar(self, input_data: DesassociarEspecialidadeMedicoInput) -> dict:
        medico = self.usuario_repository.buscar_por_id(input_data.medico_id)
        if not medico:
            raise ValueError("Medico nao encontrado.")

        especialidade = self.especialidade_repository.buscar_por_id(input_data.especialidade_id)
        if not especialidade:
            raise ValueError("Especialidade nao encontrada.")

        self.especialidade_repository.desassociar_medico(input_data.medico_id, input_data.especialidade_id)
        self.horario_disponivel_repository.deletar_por_medico_e_especialidade(
            input_data.medico_id, input_data.especialidade_id
        )

        return {"mensagem": "Especialidade desassociada e horarios removidos com sucesso."}
```

- [ ] **Step 3: Adicionar `desassociar_medico` ao contrato de especialidade**

Em `src/domain/contracts/especialidade_repository_contract.py`, adicionar:

```python
    @abstractmethod
    def desassociar_medico(self, medico_id: int, especialidade_id: int) -> None:
        ...
```

- [ ] **Step 4: Adicionar `deletar_por_medico_e_especialidade` ao contrato de horário**

Em `src/domain/contracts/horario_disponivel_repository_contract.py`, adicionar:

```python
    @abstractmethod
    def deletar_por_medico_e_especialidade(self, medico_id: int, especialidade_id: int) -> None:
        ...
```

- [ ] **Step 5: Implementar `desassociar_medico` no repositório de especialidade**

Em `src/repositories/especialidade_repository.py`, adicionar método:

```python
    def desassociar_medico(self, medico_id: int, especialidade_id: int) -> None:
        medico = UsuarioModel.query.get(medico_id)
        especialidade = EspecialidadeModel.query.get(especialidade_id)

        if not medico or especialidade not in medico.especialidades:
            raise ValueError("Associacao nao encontrada.")

        medico.especialidades.remove(especialidade)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
```

- [ ] **Step 6: Implementar `deletar_por_medico_e_especialidade` no repositório de horário**

Em `src/repositories/horario_disponivel_repository.py`, adicionar import e método:

```python
    def deletar_por_medico_e_especialidade(self, medico_id: int, especialidade_id: int) -> None:
        rows = HorarioDisponivelModel.query.filter_by(
            medico_id=medico_id,
            especialidade_id=especialidade_id,
        ).all()

        for row in rows:
            db.session.delete(row)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
```

- [ ] **Step 7: Adicionar getter ao container**

Em `src/application/dependencies/container.py`, adicionar import:

```python
from src.usecases.especialidades.desassociar_especialidade_medico.desassociar_especialidade_medico_usecase import DesassociarEspecialidadeMedicoUseCase
```

Adicionar função:

```python
def get_desassociar_especialidade_medico() -> DesassociarEspecialidadeMedicoUseCase:
    return _scoped(
        "desassociar_especialidade_medico_use_case",
        lambda: DesassociarEspecialidadeMedicoUseCase(
            _get_especialidade_repository(),
            _get_usuario_repository(),
            _get_horario_disponivel_repository(),
        ),
    )
```

- [ ] **Step 8: Adicionar rota ao controller de especialidade**

Em `src/application/controllers/especialidade_controller.py`, adicionar imports:

```python
from src.application.docs.especialidades_docs import (..., ESPECIALIDADE_DESASSOCIAR_MEDICO_DOC)
from src.application.dependencies.container import (..., get_desassociar_especialidade_medico)
from src.usecases.especialidades.desassociar_especialidade_medico.desassociar_especialidade_medico_input import DesassociarEspecialidadeMedicoInput
```

Adicionar rota:

```python
@especialidade_bp.route("/medico/<int:medico_id>", methods=["DELETE"])
@jwt_required()
@swag_from(ESPECIALIDADE_DESASSOCIAR_MEDICO_DOC)
def desassociar_especialidade_medico(medico_id: int):
    claims = get_jwt()
    if claims.get("tipo") != TipoUsuario.ADMIN.value:
        return jsonify({"erro": "Acesso negado. Apenas admins podem desassociar especialidades."}), 403

    data = request.get_json(silent=True) or {}

    try:
        desassociar_input = DesassociarEspecialidadeMedicoInput.from_dict(data, medico_id)
        use_case = get_desassociar_especialidade_medico()
        resultado = use_case.executar(desassociar_input)
        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500
```

- [ ] **Step 9: Adicionar Swagger doc**

Em `src/application/docs/especialidades_docs.py`:

```python
ESPECIALIDADE_DESASSOCIAR_MEDICO_DOC = {
    "tags": ["Especialidades"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "medico_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID do medico",
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["especialidade_id"],
                    "properties": {
                        "especialidade_id": {"type": "integer", "example": 1},
                    },
                }
            }
        },
    },
    "responses": {
        200: {"description": "Especialidade desassociada e horarios removidos com sucesso"},
        403: {"description": "Acesso negado. Apenas admins."},
        422: {"description": "Erro de validacao"},
        500: {"description": "Erro interno"},
    },
}
```

- [ ] **Step 10: Criar `__init__.py`**

```bash
touch src/usecases/especialidades/desassociar_especialidade_medico/__init__.py
```

- [ ] **Step 11: Commit**

```bash
git add src/usecases/especialidades/desassociar_especialidade_medico/ src/domain/contracts/especialidade_repository_contract.py src/domain/contracts/horario_disponivel_repository_contract.py src/repositories/especialidade_repository.py src/repositories/horario_disponivel_repository.py src/application/dependencies/container.py src/application/controllers/especialidade_controller.py src/application/docs/especialidades_docs.py
git commit -m "feat: add DELETE /especialidades/medico/<id> endpoint (desassociar especialidade)"
```

---

## Task 6: Editar especialidade — `PUT /especialidades/<id>`

**Files:**
- Create: `src/usecases/especialidades/editar_especialidade/editar_especialidade_input.py`
- Create: `src/usecases/especialidades/editar_especialidade/editar_especialidade_usecase.py`
- Modify: `src/domain/contracts/especialidade_repository_contract.py`
- Modify: `src/repositories/especialidade_repository.py`
- Modify: `src/application/dependencies/container.py`
- Modify: `src/application/controllers/especialidade_controller.py`
- Modify: `src/application/docs/especialidades_docs.py`

- [ ] **Step 1: Criar DTO de input**

Criar `src/usecases/especialidades/editar_especialidade/editar_especialidade_input.py`:

```python
from dataclasses import dataclass


@dataclass
class EditarEspecialidadeInput:
    especialidade_id: int
    nome: str

    @staticmethod
    def from_dict(data: dict, especialidade_id: int) -> "EditarEspecialidadeInput":
        nome = data.get("nome", "").strip()
        if not nome:
            raise ValueError("Campo obrigatorio ausente: nome")
        return EditarEspecialidadeInput(especialidade_id=especialidade_id, nome=nome)
```

- [ ] **Step 2: Criar o use case**

Criar `src/usecases/especialidades/editar_especialidade/editar_especialidade_usecase.py`:

```python
from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.usecases.especialidades.editar_especialidade.editar_especialidade_input import EditarEspecialidadeInput


class EditarEspecialidadeUseCase:

    def __init__(self, especialidade_repository: EspecialidadeRepositoryContract):
        self.especialidade_repository = especialidade_repository

    def executar(self, input_data: EditarEspecialidadeInput) -> dict:
        especialidade = self.especialidade_repository.buscar_por_id(input_data.especialidade_id)
        if not especialidade:
            raise ValueError("Especialidade nao encontrada.")

        especialidade.nome = input_data.nome
        atualizada = self.especialidade_repository.atualizar(especialidade)

        return {"id": atualizada.id, "nome": atualizada.nome}
```

- [ ] **Step 3: Adicionar `atualizar` ao contrato**

Em `src/domain/contracts/especialidade_repository_contract.py`:

```python
    @abstractmethod
    def atualizar(self, especialidade: Especialidade) -> Especialidade:
        ...
```

- [ ] **Step 4: Implementar `atualizar` no repositório**

Em `src/repositories/especialidade_repository.py`:

```python
    def atualizar(self, especialidade: Especialidade) -> Especialidade:
        existente = EspecialidadeModel.query.filter(
            EspecialidadeModel.nome == especialidade.nome,
            EspecialidadeModel.id != especialidade.id,
        ).first()
        if existente:
            raise ValueError(f"Especialidade '{especialidade.nome}' ja cadastrada.")

        model = EspecialidadeModel.query.get(especialidade.id)
        if not model:
            raise ValueError("Especialidade nao encontrada.")

        model.nome = especialidade.nome
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return self._to_domain(model)
```

- [ ] **Step 5: Adicionar getter ao container**

Em `src/application/dependencies/container.py`:

```python
from src.usecases.especialidades.editar_especialidade.editar_especialidade_usecase import EditarEspecialidadeUseCase


def get_editar_especialidade() -> EditarEspecialidadeUseCase:
    return _scoped(
        "editar_especialidade_use_case",
        lambda: EditarEspecialidadeUseCase(_get_especialidade_repository()),
    )
```

- [ ] **Step 6: Adicionar rota ao controller**

Em `src/application/controllers/especialidade_controller.py`:

```python
from src.application.docs.especialidades_docs import (..., ESPECIALIDADE_EDITAR_DOC)
from src.application.dependencies.container import (..., get_editar_especialidade)
from src.usecases.especialidades.editar_especialidade.editar_especialidade_input import EditarEspecialidadeInput


@especialidade_bp.route("/<int:especialidade_id>", methods=["PUT"])
@jwt_required()
@swag_from(ESPECIALIDADE_EDITAR_DOC)
def editar_especialidade(especialidade_id: int):
    claims = get_jwt()
    if claims.get("tipo") != TipoUsuario.ADMIN.value:
        return jsonify({"erro": "Acesso negado. Apenas admins podem editar especialidades."}), 403

    data = request.get_json(silent=True) or {}

    try:
        editar_input = EditarEspecialidadeInput.from_dict(data, especialidade_id)
        use_case = get_editar_especialidade()
        resultado = use_case.executar(editar_input)
        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500
```

- [ ] **Step 7: Adicionar Swagger doc**

Em `src/application/docs/especialidades_docs.py`:

```python
ESPECIALIDADE_EDITAR_DOC = {
    "tags": ["Especialidades"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "especialidade_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID da especialidade",
        }
    ],
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "required": ["nome"],
                    "properties": {
                        "nome": {"type": "string", "example": "Cardiologia Avancada"},
                    },
                }
            }
        },
    },
    "responses": {
        200: {"description": "Especialidade atualizada com sucesso"},
        403: {"description": "Acesso negado. Apenas admins."},
        422: {"description": "Especialidade nao encontrada ou nome ja em uso"},
        500: {"description": "Erro interno"},
    },
}
```

- [ ] **Step 8: Criar `__init__.py`**

```bash
touch src/usecases/especialidades/editar_especialidade/__init__.py
```

- [ ] **Step 9: Commit**

```bash
git add src/usecases/especialidades/editar_especialidade/ src/domain/contracts/especialidade_repository_contract.py src/repositories/especialidade_repository.py src/application/dependencies/container.py src/application/controllers/especialidade_controller.py src/application/docs/especialidades_docs.py
git commit -m "feat: add PUT /especialidades/<id> endpoint (editar especialidade)"
```

---

## Task 7: Excluir especialidade — `DELETE /especialidades/<id>`

**Files:**
- Create: `src/usecases/especialidades/excluir_especialidade/excluir_especialidade_input.py`
- Create: `src/usecases/especialidades/excluir_especialidade/excluir_especialidade_usecase.py`
- Modify: `src/domain/contracts/especialidade_repository_contract.py`
- Modify: `src/repositories/especialidade_repository.py`
- Modify: `src/application/dependencies/container.py`
- Modify: `src/application/controllers/especialidade_controller.py`
- Modify: `src/application/docs/especialidades_docs.py`

- [ ] **Step 1: Criar DTO de input**

Criar `src/usecases/especialidades/excluir_especialidade/excluir_especialidade_input.py`:

```python
from dataclasses import dataclass


@dataclass
class ExcluirEspecialidadeInput:
    especialidade_id: int

    @staticmethod
    def from_path(especialidade_id: int) -> "ExcluirEspecialidadeInput":
        if not especialidade_id:
            raise ValueError("Campo obrigatorio ausente: especialidade_id")
        return ExcluirEspecialidadeInput(especialidade_id=especialidade_id)
```

- [ ] **Step 2: Criar o use case**

Criar `src/usecases/especialidades/excluir_especialidade/excluir_especialidade_usecase.py`:

```python
from src.domain.contracts.especialidade_repository_contract import EspecialidadeRepositoryContract
from src.usecases.especialidades.excluir_especialidade.excluir_especialidade_input import ExcluirEspecialidadeInput


class ExcluirEspecialidadeUseCase:

    def __init__(self, especialidade_repository: EspecialidadeRepositoryContract):
        self.especialidade_repository = especialidade_repository

    def executar(self, input_data: ExcluirEspecialidadeInput) -> dict:
        especialidade = self.especialidade_repository.buscar_por_id(input_data.especialidade_id)
        if not especialidade:
            raise ValueError("Especialidade nao encontrada.")

        self.especialidade_repository.deletar(input_data.especialidade_id)

        return {"mensagem": "Especialidade excluida com sucesso."}
```

- [ ] **Step 3: Adicionar `deletar` ao contrato**

Em `src/domain/contracts/especialidade_repository_contract.py`:

```python
    @abstractmethod
    def deletar(self, especialidade_id: int) -> None:
        ...
```

- [ ] **Step 4: Implementar `deletar` no repositório**

Em `src/repositories/especialidade_repository.py`, adicionar import:

```python
from src.infrastructure.models.horario_disponivel_model import HorarioDisponivelModel
```

Adicionar método:

```python
    def deletar(self, especialidade_id: int) -> None:
        model = EspecialidadeModel.query.get(especialidade_id)
        if not model:
            raise ValueError("Especialidade nao encontrada.")

        # Remove horarios vinculados a esta especialidade
        HorarioDisponivelModel.query.filter_by(especialidade_id=especialidade_id).delete()

        # Desassocia de todos os medicos (limpa medico_especialidades)
        model.medicos.clear()

        # Remove o registro
        db.session.delete(model)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
```

- [ ] **Step 5: Adicionar getter ao container**

Em `src/application/dependencies/container.py`:

```python
from src.usecases.especialidades.excluir_especialidade.excluir_especialidade_usecase import ExcluirEspecialidadeUseCase


def get_excluir_especialidade() -> ExcluirEspecialidadeUseCase:
    return _scoped(
        "excluir_especialidade_use_case",
        lambda: ExcluirEspecialidadeUseCase(_get_especialidade_repository()),
    )
```

- [ ] **Step 6: Adicionar rota ao controller**

Em `src/application/controllers/especialidade_controller.py`:

```python
from src.application.docs.especialidades_docs import (..., ESPECIALIDADE_EXCLUIR_DOC)
from src.application.dependencies.container import (..., get_excluir_especialidade)
from src.usecases.especialidades.excluir_especialidade.excluir_especialidade_input import ExcluirEspecialidadeInput


@especialidade_bp.route("/<int:especialidade_id>", methods=["DELETE"])
@jwt_required()
@swag_from(ESPECIALIDADE_EXCLUIR_DOC)
def excluir_especialidade(especialidade_id: int):
    claims = get_jwt()
    if claims.get("tipo") != TipoUsuario.ADMIN.value:
        return jsonify({"erro": "Acesso negado. Apenas admins podem excluir especialidades."}), 403

    try:
        excluir_input = ExcluirEspecialidadeInput.from_path(especialidade_id)
        use_case = get_excluir_especialidade()
        resultado = use_case.executar(excluir_input)
        return jsonify(resultado), 200

    except ValueError as e:
        return jsonify({"erro": str(e)}), 422
    except Exception:
        return jsonify({"erro": "Erro interno no servidor."}), 500
```

- [ ] **Step 7: Adicionar Swagger doc**

Em `src/application/docs/especialidades_docs.py`:

```python
ESPECIALIDADE_EXCLUIR_DOC = {
    "tags": ["Especialidades"],
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "especialidade_id",
            "in": "path",
            "required": True,
            "schema": {"type": "integer"},
            "description": "ID da especialidade a excluir",
        }
    ],
    "responses": {
        200: {"description": "Especialidade excluida com sucesso (horarios e associacoes removidos; consultas mantidas)"},
        403: {"description": "Acesso negado. Apenas admins."},
        422: {"description": "Especialidade nao encontrada"},
        500: {"description": "Erro interno"},
    },
}
```

- [ ] **Step 8: Criar `__init__.py`**

```bash
touch src/usecases/especialidades/excluir_especialidade/__init__.py
```

- [ ] **Step 9: Commit**

```bash
git add src/usecases/especialidades/excluir_especialidade/ src/domain/contracts/especialidade_repository_contract.py src/repositories/especialidade_repository.py src/application/dependencies/container.py src/application/controllers/especialidade_controller.py src/application/docs/especialidades_docs.py
git commit -m "feat: add DELETE /especialidades/<id> endpoint (excluir especialidade)"
```

---

## Task 8: Testes de integração

**Files:**
- Create: `tests/integration/test_gaps_funcionalidade.py`

> **Pré-requisito:** API rodando em `http://localhost:5000` (via `docker compose up --build`). Login de admin: `admin@meditech.com` / `Meditech@2026`. Login de médico: `ana.lima@meditech.com` / `Meditech@2026`.

- [ ] **Step 1: Criar o arquivo de testes**

Criar `tests/integration/test_gaps_funcionalidade.py`:

```python
"""
Testes de integração para os 6 novos endpoints (gaps de funcionalidade).
Requer Docker rodando: docker compose up --build
"""

import io
import uuid

import pytest
import requests

from tests.integration.helpers import BASE_URL, auth_headers, login, ADMIN_EMAIL, ADMIN_SENHA, MEDICO_EMAIL, MEDICO_SENHA


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def admin_h():
    return auth_headers(login(ADMIN_EMAIL, ADMIN_SENHA))


@pytest.fixture(scope="module")
def medico_h():
    return auth_headers(login(MEDICO_EMAIL, MEDICO_SENHA))


@pytest.fixture(scope="module")
def medico_id(admin_h):
    resp = requests.get(f"{BASE_URL}/usuarios", headers=admin_h, params={"tipo": "medico", "nome": "Ana"})
    for u in resp.json():
        if u.get("email") == MEDICO_EMAIL:
            return u["id"]
    pytest.fail("Medico Ana nao encontrado")


@pytest.fixture(scope="module")
def esp_teste(admin_h):
    """Cria uma especialidade de teste e retorna seu ID."""
    sufixo = uuid.uuid4().hex[:6]
    resp = requests.post(
        f"{BASE_URL}/especialidades",
        headers=admin_h,
        json={"nome": f"EspTeste_{sufixo}"},
    )
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture(scope="module")
def paciente_teste():
    sufixo = uuid.uuid4().hex[:8]
    payload = {
        "nome": "Paciente",
        "sobrenome": "GapTeste",
        "data_nascimento": "1995-01-01",
        "genero": "feminino",
        "email": f"gap.teste.{sufixo}@example.com",
        "senha": "Teste@1234",
        "cpf": f"111{sufixo[:8]}",
        "telefone": "11988887777",
    }
    resp = requests.post(f"{BASE_URL}/usuarios", json=payload)
    assert resp.status_code == 201
    token = login(payload["email"], payload["senha"])
    return {"id": resp.json()["id"], "token": token, "headers": auth_headers(token), "senha": payload["senha"]}


# ── Alterar senha ──────────────────────────────────────────────────────────────

class TestAlterarSenha:

    def test_proprio_usuario_altera_senha_com_senha_atual_correta(self, paciente_teste):
        resp = requests.patch(
            f"{BASE_URL}/usuarios/{paciente_teste['id']}/senha",
            headers=paciente_teste["headers"],
            json={"senha_atual": paciente_teste["senha"], "nova_senha": "NovaSenha@456"},
        )
        assert resp.status_code == 200
        assert "mensagem" in resp.json()

    def test_senha_atual_incorreta_retorna_422(self, paciente_teste):
        resp = requests.patch(
            f"{BASE_URL}/usuarios/{paciente_teste['id']}/senha",
            headers=paciente_teste["headers"],
            json={"senha_atual": "SenhaErrada!", "nova_senha": "OutraSenha@789"},
        )
        assert resp.status_code == 422

    def test_nova_senha_curta_retorna_422(self, paciente_teste):
        resp = requests.patch(
            f"{BASE_URL}/usuarios/{paciente_teste['id']}/senha",
            headers=paciente_teste["headers"],
            json={"senha_atual": paciente_teste["senha"], "nova_senha": "abc"},
        )
        assert resp.status_code == 422

    def test_admin_altera_senha_sem_senha_atual(self, admin_h, paciente_teste):
        resp = requests.patch(
            f"{BASE_URL}/usuarios/{paciente_teste['id']}/senha",
            headers=admin_h,
            json={"nova_senha": "AdminReset@2026"},
        )
        assert resp.status_code == 200

    def test_usuario_nao_pode_alterar_senha_de_outro(self, medico_h, paciente_teste):
        resp = requests.patch(
            f"{BASE_URL}/usuarios/{paciente_teste['id']}/senha",
            headers=medico_h,
            json={"nova_senha": "HackerSenha@123"},
        )
        assert resp.status_code == 403


# ── Excluir conta ──────────────────────────────────────────────────────────────

class TestExcluirConta:

    @pytest.fixture(scope="class")
    def usuario_para_excluir(self):
        sufixo = uuid.uuid4().hex[:8]
        payload = {
            "nome": "Excluir",
            "sobrenome": "Teste",
            "data_nascimento": "2000-06-15",
            "genero": "masculino",
            "email": f"excluir.{sufixo}@example.com",
            "senha": "Excluir@123",
            "cpf": f"222{sufixo[:8]}",
            "telefone": "11977776666",
        }
        resp = requests.post(f"{BASE_URL}/usuarios", json=payload)
        assert resp.status_code == 201
        token = login(payload["email"], payload["senha"])
        return {"id": resp.json()["id"], "headers": auth_headers(token)}

    def test_usuario_exclui_propria_conta(self, usuario_para_excluir):
        resp = requests.delete(
            f"{BASE_URL}/usuarios/{usuario_para_excluir['id']}",
            headers=usuario_para_excluir["headers"],
        )
        assert resp.status_code == 200

    def test_usuario_excluido_nao_aparece_na_listagem(self, admin_h, usuario_para_excluir):
        resp = requests.get(f"{BASE_URL}/usuarios", headers=admin_h)
        assert resp.status_code == 200
        ids = [u["id"] for u in resp.json()]
        assert usuario_para_excluir["id"] not in ids

    def test_admin_nao_pode_excluir_propria_conta(self, admin_h):
        resp = requests.get(f"{BASE_URL}/usuarios", headers=admin_h, params={"tipo": "admin"})
        admin_id = resp.json()[0]["id"]
        resp = requests.delete(f"{BASE_URL}/usuarios/{admin_id}", headers=admin_h)
        assert resp.status_code == 422


# ── Upload de documento ────────────────────────────────────────────────────────

class TestUploadDocumento:

    def test_medico_faz_upload_de_documento(self, medico_h, medico_id):
        conteudo = b"Conteudo do CRM de teste"
        resp = requests.post(
            f"{BASE_URL}/documentos/upload",
            headers=medico_h,
            data={"tipo": "crm", "usuario_id": medico_id},
            files={"arquivo": ("crm.pdf", io.BytesIO(conteudo), "application/pdf")},
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["tipo"] == "crm"
        assert body["usuario_id"] == medico_id

    def test_tipo_invalido_retorna_422(self, medico_h, medico_id):
        resp = requests.post(
            f"{BASE_URL}/documentos/upload",
            headers=medico_h,
            data={"tipo": "passaporte", "usuario_id": medico_id},
            files={"arquivo": ("doc.pdf", io.BytesIO(b"abc"), "application/pdf")},
        )
        assert resp.status_code == 422

    def test_sem_arquivo_retorna_422(self, medico_h, medico_id):
        resp = requests.post(
            f"{BASE_URL}/documentos/upload",
            headers=medico_h,
            data={"tipo": "curriculo", "usuario_id": medico_id},
        )
        assert resp.status_code == 422


# ── Desassociar especialidade do médico ───────────────────────────────────────

class TestDesassociarEspecialidadeMedico:

    @pytest.fixture(scope="class")
    def esp_para_desassociar(self, admin_h, medico_id):
        sufixo = uuid.uuid4().hex[:6]
        resp = requests.post(
            f"{BASE_URL}/especialidades",
            headers=admin_h,
            json={"nome": f"EspDesassoc_{sufixo}"},
        )
        assert resp.status_code == 201
        esp_id = resp.json()["id"]
        resp = requests.post(
            f"{BASE_URL}/especialidades/medico/{medico_id}",
            headers=admin_h,
            json={"especialidade_id": esp_id},
        )
        assert resp.status_code == 201
        return esp_id

    def test_admin_desassocia_especialidade(self, admin_h, medico_id, esp_para_desassociar):
        resp = requests.delete(
            f"{BASE_URL}/especialidades/medico/{medico_id}",
            headers=admin_h,
            json={"especialidade_id": esp_para_desassociar},
        )
        assert resp.status_code == 200

    def test_nao_admin_retorna_403(self, medico_h, medico_id):
        resp = requests.delete(
            f"{BASE_URL}/especialidades/medico/{medico_id}",
            headers=medico_h,
            json={"especialidade_id": 999},
        )
        assert resp.status_code == 403


# ── Editar especialidade ───────────────────────────────────────────────────────

class TestEditarEspecialidade:

    def test_admin_edita_nome_da_especialidade(self, admin_h, esp_teste):
        novo_nome = f"Editada_{uuid.uuid4().hex[:6]}"
        resp = requests.put(
            f"{BASE_URL}/especialidades/{esp_teste['id']}",
            headers=admin_h,
            json={"nome": novo_nome},
        )
        assert resp.status_code == 200
        assert resp.json()["nome"] == novo_nome

    def test_nome_duplicado_retorna_422(self, admin_h, esp_teste):
        # Pega outra especialidade existente para pegar um nome em uso
        resp = requests.get(f"{BASE_URL}/especialidades", headers=admin_h)
        outros = [e for e in resp.json() if e["id"] != esp_teste["id"]]
        if not outros:
            pytest.skip("Nao ha outra especialidade para testar duplicidade")
        nome_em_uso = outros[0]["nome"]
        resp = requests.put(
            f"{BASE_URL}/especialidades/{esp_teste['id']}",
            headers=admin_h,
            json={"nome": nome_em_uso},
        )
        assert resp.status_code == 422

    def test_nao_admin_retorna_403(self, medico_h, esp_teste):
        resp = requests.put(
            f"{BASE_URL}/especialidades/{esp_teste['id']}",
            headers=medico_h,
            json={"nome": "Tentativa"},
        )
        assert resp.status_code == 403


# ── Excluir especialidade ──────────────────────────────────────────────────────

class TestExcluirEspecialidade:

    @pytest.fixture(scope="class")
    def esp_para_excluir(self, admin_h):
        sufixo = uuid.uuid4().hex[:6]
        resp = requests.post(
            f"{BASE_URL}/especialidades",
            headers=admin_h,
            json={"nome": f"EspExcluir_{sufixo}"},
        )
        assert resp.status_code == 201
        return resp.json()["id"]

    def test_admin_exclui_especialidade(self, admin_h, esp_para_excluir):
        resp = requests.delete(
            f"{BASE_URL}/especialidades/{esp_para_excluir}",
            headers=admin_h,
        )
        assert resp.status_code == 200

    def test_especialidade_excluida_nao_aparece_na_listagem(self, admin_h, esp_para_excluir):
        resp = requests.get(f"{BASE_URL}/especialidades", headers=admin_h)
        ids = [e["id"] for e in resp.json()]
        assert esp_para_excluir not in ids

    def test_nao_admin_retorna_403(self, medico_h):
        resp = requests.delete(f"{BASE_URL}/especialidades/1", headers=medico_h)
        assert resp.status_code == 403
```

- [ ] **Step 2: Rodar os testes**

```bash
pytest tests/integration/test_gaps_funcionalidade.py -v
```

Todos os testes devem passar. Se algum falhar, inspecionar a resposta HTTP e corrigir.

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_gaps_funcionalidade.py
git commit -m "test: add integration tests for 6 new endpoints (gaps de funcionalidade)"
```

---

## Self-Review do Plano

**Cobertura da spec:**
- [x] `POST /documentos/upload` — Task 4
- [x] `PATCH /usuarios/<id>/senha` — Task 2
- [x] `DELETE /especialidades/medico/<id>` — Task 5
- [x] `PUT /especialidades/<id>` — Task 6
- [x] `DELETE /especialidades/<id>` — Task 7
- [x] `DELETE /usuarios/<id>` (soft delete) — Task 3
- [x] Campo `excluido_em` no domínio e modelo — Task 1
- [x] `especialidade_id` nullable em consulta — Task 1
- [x] Filtro de `excluido_em` em `listar` e `buscar_por_email` — Task 1

**Assinaturas consistentes:**
- `atualizar_senha(usuario_id: int, nova_senha_hash: str)` — definida em Task 2 Step 3, implementada em Task 2 Step 4, chamada em Task 2 Step 2.
- `excluir(usuario_id: int)` — definida em Task 3 Step 3, implementada em Task 3 Step 4, chamada em Task 3 Step 2.
- `desassociar_medico(medico_id, especialidade_id)` — definida em Task 5 Step 3, implementada em Task 5 Step 5, chamada em Task 5 Step 2.
- `deletar_por_medico_e_especialidade(medico_id, especialidade_id)` — definida em Task 5 Step 4, implementada em Task 5 Step 6, chamada em Task 5 Step 2.
- `atualizar(especialidade)` — definida em Task 6 Step 3, implementada em Task 6 Step 4, chamada em Task 6 Step 2.
- `deletar(especialidade_id)` — definida em Task 7 Step 3, implementada em Task 7 Step 4, chamada em Task 7 Step 2.

**Sem placeholders.** Todos os passos têm código completo.
