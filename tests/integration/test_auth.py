"""
Testes de integração — Autenticação (/auth/login)
"""

import requests
from tests.integration.helpers import BASE_URL, ADMIN_EMAIL, ADMIN_SENHA


class TestLogin:
    def test_login_admin_retorna_token(self):
        resp = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": ADMIN_EMAIL, "senha": ADMIN_SENHA},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "access_token" in body

    def test_login_senha_errada_retorna_401(self):
        resp = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": ADMIN_EMAIL, "senha": "senha_errada"},
        )
        assert resp.status_code == 401

    def test_login_email_inexistente_retorna_401(self):
        resp = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "naoexiste@example.com", "senha": "qualquer"},
        )
        assert resp.status_code == 401

    def test_login_sem_campos_retorna_422(self):
        resp = requests.post(f"{BASE_URL}/auth/login", json={})
        assert resp.status_code == 422

    def test_rota_protegida_sem_token_retorna_401(self):
        resp = requests.get(f"{BASE_URL}/usuarios")
        assert resp.status_code == 401

    def test_rota_protegida_com_token_invalido_retorna_422(self):
        resp = requests.get(
            f"{BASE_URL}/usuarios",
            headers={"Authorization": "Bearer token.invalido.aqui"},
        )
        assert resp.status_code == 422
