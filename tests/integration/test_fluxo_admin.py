"""
Testes de integração — Fluxo do administrador

Cobre:
  1. Admin lista todos os usuários (incluindo inativos)
  2. Admin filtra por tipo/ativo
  3. Admin cadastra nova especialidade
  4. Admin ativa médico inativo
  5. Admin desativa médico ativo
  6. Acesso negado para não-admins em rotas restritas
"""

import uuid
import requests
import pytest
from tests.integration.helpers import BASE_URL


# Email de um médico inativo da carga inicial
MEDICO_INATIVO_EMAIL = "karine.silva@meditech.com"


class TestListarUsuarios:
    def test_admin_ve_todos_os_usuarios(self, admin_headers):
        resp = requests.get(f"{BASE_URL}/usuarios", headers=admin_headers)
        assert resp.status_code == 200
        usuarios = resp.json()
        # Deve conter médicos inativos também
        tipos = {u["tipo"] for u in usuarios}
        ativos = {u["ativo"] for u in usuarios}
        assert "medico" in tipos
        assert False in ativos  # tem inativos

    def test_admin_filtra_por_tipo_medico(self, admin_headers):
        resp = requests.get(
            f"{BASE_URL}/usuarios", headers=admin_headers, params={"tipo": "medico"}
        )
        assert resp.status_code == 200
        for u in resp.json():
            assert u["tipo"] == "medico"

    def test_admin_filtra_medicos_ativos(self, admin_headers):
        resp = requests.get(
            f"{BASE_URL}/usuarios",
            headers=admin_headers,
            params={"tipo": "medico", "ativo": "true"},
        )
        assert resp.status_code == 200
        for u in resp.json():
            assert u["tipo"] == "medico"
            assert u["ativo"] is True

    def test_paciente_nao_ve_inativos(self, paciente_cadastrado):
        resp = requests.get(f"{BASE_URL}/usuarios", headers=paciente_cadastrado["headers"])
        assert resp.status_code == 200
        for u in resp.json():
            assert u["ativo"] is True


class TestCadastrarEspecialidade:
    def test_admin_cria_especialidade(self, admin_headers):
        nome = f"Especialidade Teste {uuid.uuid4().hex[:6]}"
        resp = requests.post(
            f"{BASE_URL}/especialidades",
            headers=admin_headers,
            json={"nome": nome},
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["nome"] == nome
        assert "id" in body

    def test_paciente_nao_pode_criar_especialidade(self, paciente_cadastrado):
        resp = requests.post(
            f"{BASE_URL}/especialidades",
            headers=paciente_cadastrado["headers"],
            json={"nome": "Especialidade Não Autorizada"},
        )
        assert resp.status_code == 403

    def test_especialidade_duplicada_retorna_erro(self, admin_headers):
        nome = f"Esp Dup {uuid.uuid4().hex[:6]}"
        requests.post(f"{BASE_URL}/especialidades", headers=admin_headers, json={"nome": nome})
        resp2 = requests.post(
            f"{BASE_URL}/especialidades", headers=admin_headers, json={"nome": nome}
        )
        # O repositório trata unicidade — esperamos 422 ou 500
        assert resp2.status_code in (422, 500)


class TestAlterarStatusUsuario:
    @pytest.fixture(scope="class")
    def medico_inativo_id(self, admin_headers):
        """Descobre o ID do médico inativo da carga inicial."""
        resp = requests.get(
            f"{BASE_URL}/usuarios",
            headers=admin_headers,
            params={"tipo": "medico", "ativo": "false"},
        )
        assert resp.status_code == 200
        for u in resp.json():
            if u.get("email") == MEDICO_INATIVO_EMAIL:
                return u["id"]
        # Fallback: pega qualquer inativo
        inativos = [u for u in resp.json() if not u["ativo"]]
        assert inativos, "Nenhum médico inativo encontrado."
        return inativos[0]["id"]

    def test_admin_ativa_medico_inativo(self, admin_headers, medico_inativo_id):
        resp = requests.patch(
            f"{BASE_URL}/usuarios/{medico_inativo_id}/alterarStatus",
            headers=admin_headers,
            json={"ativo": True},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ativo") is True

    def test_admin_desativa_medico(self, admin_headers, medico_inativo_id):
        # Garante que foi ativado antes de desativar
        resp = requests.patch(
            f"{BASE_URL}/usuarios/{medico_inativo_id}/alterarStatus",
            headers=admin_headers,
            json={"ativo": False},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ativo") is False

    def test_paciente_nao_pode_alterar_status(self, paciente_cadastrado, medico_inativo_id):
        resp = requests.patch(
            f"{BASE_URL}/usuarios/{medico_inativo_id}/alterarStatus",
            headers=paciente_cadastrado["headers"],
            json={"ativo": True},
        )
        assert resp.status_code == 403
