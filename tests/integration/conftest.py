"""
Fixtures compartilhadas para testes de integração.

Pré-requisito: Docker rodando com `docker compose up --build`
O banco deve ter a carga inicial aplicada (scripts/carga_inicial.sql).

Configure a URL base via variável de ambiente:
    MEDITECH_BASE_URL=http://localhost:5000  (padrão)
"""

import uuid

import pytest
import requests

from tests.integration.helpers import (
    BASE_URL,
    ADMIN_EMAIL,
    ADMIN_SENHA,
    MEDICO_EMAIL,
    MEDICO_SENHA,
    login,
    auth_headers,
    proxima_data_dia_semana,
)


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def admin_token():
    return login(ADMIN_EMAIL, ADMIN_SENHA)


@pytest.fixture(scope="session")
def medico_token():
    return login(MEDICO_EMAIL, MEDICO_SENHA)


@pytest.fixture(scope="session")
def admin_headers(admin_token):
    return auth_headers(admin_token)


@pytest.fixture(scope="session")
def medico_headers(medico_token):
    return auth_headers(medico_token)


@pytest.fixture(scope="session")
def especialidade_clinica_geral(admin_headers):
    """Retorna o dict da especialidade 'Clínica Geral'."""
    resp = requests.get(f"{BASE_URL}/especialidades", headers=admin_headers)
    assert resp.status_code == 200
    for esp in resp.json():
        if "Cl" in esp["nome"] and "Geral" in esp["nome"]:
            return esp
    pytest.fail("Especialidade 'Clínica Geral' não encontrada no banco.")


@pytest.fixture(scope="session")
def medico_ana_id(admin_headers):
    """Retorna o id da doutora Ana Lima (médica ativa do seed)."""
    resp = requests.get(
        f"{BASE_URL}/usuarios",
        headers=admin_headers,
        params={"tipo": "medico", "nome": "Ana"},
    )
    assert resp.status_code == 200
    for u in resp.json():
        if u.get("email") == MEDICO_EMAIL:
            return u["id"]
    pytest.fail(f"Médico {MEDICO_EMAIL} não encontrado via /usuarios.")


@pytest.fixture(scope="session")
def proxima_segunda():
    """Retorna a próxima segunda-feira (dia_semana=0) como string YYYY-MM-DD."""
    return proxima_data_dia_semana(0)


@pytest.fixture(scope="session")
def paciente_cadastrado():
    """Cadastra um paciente único para os testes e retorna seus dados + token."""
    sufixo = uuid.uuid4().hex[:8]
    payload = {
        "nome": "Teste",
        "sobrenome": "Integracao",
        "data_nascimento": "1990-05-20",
        "genero": "masculino",
        "email": f"teste.integracao.{sufixo}@example.com",
        "senha": "Teste@1234",
        "cpf": f"999{sufixo[:8]}",
        "telefone": "11999990000",
    }
    resp = requests.post(f"{BASE_URL}/usuarios", json=payload)
    assert resp.status_code == 201, f"Cadastro de paciente falhou: {resp.text}"

    token = login(payload["email"], payload["senha"])
    return {
        "id": resp.json()["id"],
        "email": payload["email"],
        "token": token,
        "headers": auth_headers(token),
    }
