import bcrypt

from src.domain.contracts.password_service_contract import PasswordServiceContract


class PasswordService(PasswordServiceContract):

    def hash(self, senha: str) -> str:
        return bcrypt.hashpw(senha.encode(), bcrypt.gensalt(12)).decode()

    def verify(self, senha: str, senha_hash: str) -> bool:
        return bcrypt.checkpw(senha.encode(), senha_hash.encode())