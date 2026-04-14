from flask_jwt_extended import create_access_token

from src.domain.contracts.token_service_contract import TokenServiceContract
from src.domain.models.usuario import Usuario


class JwtTokenService(TokenServiceContract):

    def generate_access_token(self, usuario: Usuario) -> str:
        return create_access_token(
            identity=str(usuario.id),
            additional_claims={
                "email": usuario.email,
                "nome": usuario.nome + " " + usuario.sobrenome,
                "tipo": usuario.tipo,
                "status_aprovacao": usuario.status_aprovacao.value if usuario.status_aprovacao else None,
            },
        )