# Design: Implementação dos 5 Gaps de Funcionalidade

**Data:** 2026-04-17  
**Branch:** feat/configuracao-doutores  
**Estratégia:** Batch único — todos os gaps em uma implementação

---

## Contexto

Cinco gaps de funcionalidade identificados no mapeamento dos fluxos do MediTech que ainda não foram implementados. Todos seguem o padrão já estabelecido no projeto: Contract → Repository → UseCase → Controller → SwaggerDoc.

---

## Gap 1 — Upload de documento pós-cadastro

### Endpoint
`POST /documentos/upload` — multipart/form-data

### Autorização
- `@jwt_required()` — qualquer usuário autenticado
- O próprio usuário faz upload para si mesmo (usuario_id extraído do JWT)
- Admin pode fazer upload para qualquer usuário (usuario_id passado como campo do form)

### Regras de negócio
- Recebe `multipart/form-data` com campos: `tipo` (crm | curriculo | sobre_mim) e arquivo `arquivo`
- Cria novo documento sem remover anteriores do mesmo tipo (múltiplos permitidos por tipo)
- Retorna `201` com `{id, tipo, nome_arquivo, usuario_id}`

### Arquivos novos
- `src/usecases/usuarios/upload_documento/upload_documento_input.py`
- `src/usecases/usuarios/upload_documento/upload_documento_usecase.py`

### Arquivos modificados
- `src/application/controllers/documentos_controller.py` — nova rota `POST /documentos/upload`
- `src/application/dependencies/container.py` — getter `get_upload_documento()`
- `src/application/docs/documentos_docs.py` — `DOCUMENTO_UPLOAD_DOC`

### Erros
| Situação | HTTP |
|----------|------|
| Tipo inválido | 422 |
| Arquivo ausente | 422 |
| Usuário não encontrado (admin subindo para outro) | 422 |

---

## Gap 2 — Alterar senha

### Endpoint
`PATCH /usuarios/<id>/senha`

### Autorização
- `@jwt_required()`
- Próprio usuário: exige `senha_atual` validada com `PasswordService.verify`
- Admin: não exige `senha_atual`, ignora o campo se fornecido

### Regras de negócio
- Body JSON: `{senha_atual?, nova_senha}`
- `nova_senha` mínimo 6 caracteres (validado no DTO)
- Hash da nova senha via `PasswordService.hash`
- Retorna `200` com `{mensagem: "Senha alterada com sucesso."}`

### Arquivos novos
- `src/usecases/usuarios/alterar_senha/alterar_senha_input.py`
- `src/usecases/usuarios/alterar_senha/alterar_senha_usecase.py`

### Arquivos modificados
- `src/domain/contracts/usuario_repository_contract.py` — + método abstrato `atualizar_senha(usuario_id, nova_senha_hash)`
- `src/repositories/usuario_repository.py` — implementação de `atualizar_senha`
- `src/application/controllers/usuario_controller.py` — nova rota `PATCH /usuarios/<id>/senha`
- `src/application/dependencies/container.py` — getter `get_alterar_senha_use_case()`
- `src/application/docs/usuarios_docs.py` — `USUARIO_ALTERAR_SENHA_DOC`

### Erros
| Situação | HTTP |
|----------|------|
| Usuário não encontrado | 422 |
| Senha atual incorreta | 422 |
| Nova senha muito curta (< 6 chars) | 422 |
| Acesso negado (não é admin nem próprio) | 403 |

---

## Gap 3 — Desassociar especialidade do médico

### Endpoint
`DELETE /especialidades/medico/<medico_id>`

### Autorização
- `@jwt_required()` — admin only

### Regras de negócio
- Body JSON: `{especialidade_id}`
- Remove a associação na tabela `medico_especialidades`
- Remove todos os `HorarioDisponivel` do médico com aquela `especialidade_id`
- Consultas já agendadas com essa especialidade não são tocadas
- Retorna `200` com `{mensagem}`

### Arquivos novos
- `src/usecases/especialidades/desassociar_especialidade_medico/desassociar_especialidade_medico_input.py`
- `src/usecases/especialidades/desassociar_especialidade_medico/desassociar_especialidade_medico_usecase.py`

### Arquivos modificados
- `src/domain/contracts/especialidade_repository_contract.py` — + `desassociar_medico(medico_id, especialidade_id)`
- `src/domain/contracts/horario_disponivel_repository_contract.py` — + `deletar_por_medico_e_especialidade(medico_id, especialidade_id)`
- `src/repositories/especialidade_repository.py` — implementação de `desassociar_medico`
- `src/repositories/horario_disponivel_repository.py` — implementação de `deletar_por_medico_e_especialidade`
- `src/application/controllers/especialidade_controller.py` — nova rota `DELETE /especialidades/medico/<medico_id>`
- `src/application/dependencies/container.py` — getter `get_desassociar_especialidade_medico()`
- `src/application/docs/especialidades_docs.py` — `ESPECIALIDADE_DESASSOCIAR_MEDICO_DOC`

### Erros
| Situação | HTTP |
|----------|------|
| Médico não encontrado | 422 |
| Especialidade não encontrada | 422 |
| Associação não existe | 422 |
| Não é admin | 403 |

---

## Gap 4 — Editar especialidade

### Endpoint
`PUT /especialidades/<id>`

### Autorização
- `@jwt_required()` — admin only

### Regras de negócio
- Body JSON: `{nome}`
- Valida unicidade do novo nome ignorando o próprio registro
- Retorna `200` com `{id, nome}`

### Arquivos novos
- `src/usecases/especialidades/editar_especialidade/editar_especialidade_input.py`
- `src/usecases/especialidades/editar_especialidade/editar_especialidade_usecase.py`

### Arquivos modificados
- `src/domain/contracts/especialidade_repository_contract.py` — + `atualizar(especialidade)`
- `src/repositories/especialidade_repository.py` — implementação de `atualizar`
- `src/application/controllers/especialidade_controller.py` — nova rota `PUT /especialidades/<id>`
- `src/application/dependencies/container.py` — getter `get_editar_especialidade()`
- `src/application/docs/especialidades_docs.py` — `ESPECIALIDADE_EDITAR_DOC`

### Erros
| Situação | HTTP |
|----------|------|
| Especialidade não encontrada | 422 |
| Nome já existe | 422 |
| Não é admin | 403 |

---

## Gap 5 — Excluir especialidade

### Endpoint
`DELETE /especialidades/<id>`

### Autorização
- `@jwt_required()` — admin only

### Regras de negócio
- Desassocia de todos os médicos (limpa `medico_especialidades`)
- Remove todos os `HorarioDisponivel` vinculados à especialidade
- Mantém `especialidade_id` nas consultas existentes (histórico intacto)
- Exclui o registro da tabela `especialidades` (hard delete)
- Retorna `200` com `{mensagem}`

### Arquivos novos
- `src/usecases/especialidades/excluir_especialidade/excluir_especialidade_input.py`
- `src/usecases/especialidades/excluir_especialidade/excluir_especialidade_usecase.py`

### Arquivos modificados
- `src/domain/contracts/especialidade_repository_contract.py` — + `deletar(especialidade_id)`
- `src/repositories/especialidade_repository.py` — implementação de `deletar` com limpeza de associações e horários
- `src/application/controllers/especialidade_controller.py` — nova rota `DELETE /especialidades/<id>`
- `src/application/dependencies/container.py` — getter `get_excluir_especialidade()`
- `src/application/docs/especialidades_docs.py` — `ESPECIALIDADE_EXCLUIR_DOC`

### Erros
| Situação | HTTP |
|----------|------|
| Especialidade não encontrada | 422 |
| Não é admin | 403 |

---

## Gap 6 — Excluir conta (soft delete)

### Endpoint
`DELETE /usuarios/<id>`

### Autorização
- `@jwt_required()` — admin ou o próprio usuário

### Regras de negócio
- Soft delete: seta `excluido_em = datetime.utcnow()` no `UsuarioModel`
- Usuários com `excluido_em != null` não aparecem em listagens (`listar` filtra `excluido_em IS NULL`)
- Login de usuário excluído retorna 401
- Admin não pode excluir a si mesmo via este endpoint
- Retorna `200` com `{mensagem}`

### Campo novo no modelo
- `UsuarioModel.excluido_em: DateTime, nullable=True, default=None`
- `Usuario.excluido_em: datetime | None = None` (domínio)

### Arquivos novos
- `src/usecases/usuarios/excluir_conta/excluir_conta_input.py`
- `src/usecases/usuarios/excluir_conta/excluir_conta_usecase.py`

### Arquivos modificados
- `src/domain/models/usuario.py` — + campo `excluido_em`
- `src/infrastructure/models/usuario_model.py` — + coluna `excluido_em`
- `src/domain/contracts/usuario_repository_contract.py` — + `excluir(usuario_id)`
- `src/repositories/usuario_repository.py` — implementação de `excluir` + filtro em `listar` e `buscar_por_email`
- `src/application/controllers/usuario_controller.py` — nova rota `DELETE /usuarios/<id>`
- `src/application/dependencies/container.py` — getter `get_excluir_conta_use_case()`
- `src/application/docs/usuarios_docs.py` — `USUARIO_EXCLUIR_DOC`

### Erros
| Situação | HTTP |
|----------|------|
| Usuário não encontrado | 422 |
| Admin tentando excluir a si mesmo | 422 |
| Acesso negado (não é admin nem próprio) | 403 |

---

## Resumo de novos endpoints

| Método | Rota | Auth | Gap |
|--------|------|------|-----|
| POST | `/documentos/upload` | JWT | Upload documento |
| PATCH | `/usuarios/<id>/senha` | JWT | Alterar senha |
| DELETE | `/especialidades/medico/<medico_id>` | JWT (admin) | Desassociar especialidade |
| PUT | `/especialidades/<id>` | JWT (admin) | Editar especialidade |
| DELETE | `/especialidades/<id>` | JWT (admin) | Excluir especialidade |
| DELETE | `/usuarios/<id>` | JWT (admin/próprio) | Excluir conta |

## Checklist de conclusão (CLAUDE.md)
- [ ] Use cases sem importação de Flask
- [ ] Validações de input no DTO (`from_dict` / `from_args`)
- [ ] Controller mapeia todos os erros para HTTP correto
- [ ] Repositório faz rollback em caso de falha
- [ ] Toda rota nova tem Swagger doc atualizado
- [ ] Endpoints retornam JSON válido nos códigos HTTP esperados
