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
        "cep": "01001000",
        "logradouro": "Rua Gap",
        "numero": "10",
        "bairro": "Centro",
        "cidade": "Sao Paulo",
        "estado": "SP",
        "tipo_sanguineo": "AB+",
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
            "cep": "01001000",
            "logradouro": "Rua Excluir",
            "numero": "20",
            "bairro": "Centro",
            "cidade": "Sao Paulo",
            "estado": "SP",
            "tipo_sanguineo": "O-",
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
