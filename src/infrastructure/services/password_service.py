from werkzeug.security import check_password_hash, generate_password_hash

from src.domain.contracts.password_service_contract import PasswordServiceContract


class PasswordService(PasswordServiceContract):

    def hash(self, senha: str) -> str:
        return generate_password_hash(senha)

    def verify(self, senha: str, senha_hash: str) -> bool:
        return check_password_hash(senha_hash, senha)