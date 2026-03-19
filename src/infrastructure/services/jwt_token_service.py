from flask_jwt_extended import create_access_token

from src.domain.contracts.token_service_contract import TokenServiceContract


class JwtTokenService(TokenServiceContract):

    def generate_access_token(self, user_id: int, email: str, cpf: str, nome: str) -> str:
        return create_access_token(
            identity=str(user_id),
            additional_claims={
                "email": email,
                "cpf": cpf,
                "nome": nome,
            },
        )