"""
Constantes e funções utilitárias compartilhadas entre os testes de integração.
Não é um conftest — pode ser importado diretamente.
"""

import os
from datetime import date, timedelta

import requests

BASE_URL = os.getenv("MEDITECH_BASE_URL", "http://localhost:5000")

ADMIN_EMAIL = "admin@meditech.com"
ADMIN_SENHA = "Meditech@2026"

MEDICO_EMAIL = "ana.lima@meditech.com"
MEDICO_SENHA = "Meditech@2026"


def login(email: str, senha: str) -> str:
    """Faz login e retorna o access_token."""
    resp = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "senha": senha})
    assert resp.status_code == 200, f"Login falhou para {email}: {resp.text}"
    return resp.json()["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def proxima_data_dia_semana(dia: int) -> str:
    """Retorna a próxima data (YYYY-MM-DD) que caia no dia_semana informado.

    dia: 0=segunda … 6=domingo (compatível com date.weekday())
    Nunca retorna hoje.
    """
    hoje = date.today()
    dias_ate = (dia - hoje.weekday() + 7) % 7
    if dias_ate == 0:
        dias_ate = 7
    return (hoje + timedelta(days=dias_ate)).isoformat()
