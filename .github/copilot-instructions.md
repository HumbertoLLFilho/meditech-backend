# MediTech Backend - Copilot Instructions

## Objetivo
Este repositorio implementa uma API Flask para cadastro/login de usuarios e cadastro/listagem de consultas medicas.
Priorize respostas e alteracoes pequenas, objetivas e alinhadas a arquitetura em camadas.

## Mapa de Arquitetura
- src/application/app_factory.py: setup e application factory do Flask
- src/application/controllers: endpoints HTTP e parse de request
- src/repositories: implementacoes de persistencia (SQLAlchemy)
- src/domain/models: entidades de negocio
- src/domain/contracts: contratos de repositorio
- src/usecases: regras de negocio
- src/infrastructure: banco, modelos e container de dependencias

## Regras de Edicao
- Mantenha use cases sem dependencia de Flask.
- Validacoes de input devem ficar em input DTOs dos usecases ou nos proprios usecases.
- Controllers devem traduzir erros para codigos HTTP consistentes.
- Repositories devem encapsular acesso ao banco e commits/rollbacks.
- Sempre que uma rota nova for criada ou alterada, atualize a documentacao Swagger/OpenAPI da rota no controller.
- Sempre que uma nova controller for criada, verifique se existe documentacao Swagger/OpenAPI para todas as suas rotas antes de finalizar.
- Evite mudancas grandes sem necessidade.

## Checklist Antes de Finalizar
- Verificar se o fluxo local e Docker continuam funcionando.
- Confirmar que endpoints retornam JSON valido.
- Confirmar codigos HTTP esperados:
  - 201 em cadastro bem-sucedido
  - 200 em consultas/listagem
  - 401 para credenciais invalidas
  - 422 para erro de validacao
  - 500 para falha inesperada

## Comandos Uteis
- Instalar dependencias: pip install -r requirements.txt
- Rodar local: python run.py
- Rodar com Docker: docker compose up --build

## Pontos de Atencao
- A autenticacao usa Flask-JWT-Extended.
- O token e gerado no use case de login via `TokenServiceContract`; o controller apenas retorna o token gerado.
- As rotas de consulta usam @jwt_required() e get_jwt_identity().
- JWT_SECRET_KEY deve estar definido para ambientes produtivos.
