import os
from datetime import datetime, timedelta, timezone

import jwt
from werkzeug.security import check_password_hash

from src.application.usuario_repository_port import UsuarioRepositoryPort


class LoginUsuarioUseCase:

    def __init__(self, repository: UsuarioRepositoryPort):
        self.repository = repository

    def executar(self, email: str, senha: str) -> dict:
        usuario = self.repository.buscar_por_email(email)

        if not usuario or not check_password_hash(usuario.senha, senha):
            raise ValueError("E-mail ou senha inválidos.")

        payload = {
            "sub": usuario.id,
            "email": usuario.email,
            "tipo": usuario.tipo.value,
            "nome": f"{usuario.nome} {usuario.sobrenome}",
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        }

        secret = os.getenv("JWT_SECRET_KEY")
        if not secret:
            raise RuntimeError("JWT_SECRET_KEY environment variable is not set.")
        token = jwt.encode(payload, secret, algorithm="HS256")

        return {
            "access_token": token,
            "tipo": usuario.tipo.value,
            "nome": f"{usuario.nome} {usuario.sobrenome}",
        }
