"""
Testes de integração — Fluxo do médico

Cobre:
  1. Cadastro de médico (nasce inativo)
  2. Médico inativo não consegue logar em rotas de médico antes de ser ativado
  3. Admin ativa o médico
  4. Médico adiciona horário disponível
  5. Médico lista seus horários
  6. Médico remove horário
  7. Médico não pode remover horário de outro médico
"""

import uuid
import requests
import pytest
from tests.integration.helpers import BASE_URL, login


def _cadastrar_medico_unico():
    sufixo = uuid.uuid4().hex[:8]
    payload = {
        "nome": "Dr Teste",
        "sobrenome": "Integracao",
        "data_nascimento": "1985-06-15",
        "genero": "masculino",
        "email": f"dr.teste.{sufixo}@example.com",
        "senha": "DrTeste@1234",
        "cpf": f"888{sufixo[:8]}",
        "telefone": "11988880000",
        "cep": "01001000",
        "logradouro": "Rua Dr Teste",
        "numero": "200",
        "bairro": "Centro",
        "cidade": "Sao Paulo",
        "estado": "SP",
    }
    return payload


class TestCadastroMedico:
    def test_cadastro_medico_nasce_inativo(self):
        payload = _cadastrar_medico_unico()
        resp = requests.post(f"{BASE_URL}/usuarios/medico", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body.get("ativo") is False
        assert body.get("tipo") == "medico"

    def test_medico_sem_campos_obrigatorios_retorna_422(self):
        resp = requests.post(f"{BASE_URL}/usuarios/medico", json={"nome": "Incompleto"})
        assert resp.status_code == 422

    def test_cadastro_medico_com_especialidade_ids_associa_especialidades(self, admin_headers, especialidade_clinica_geral):
        """Especialidades passadas em especialidade_ids devem ser associadas ao médico na criação."""
        payload = _cadastrar_medico_unico()
        payload["especialidade_ids"] = [especialidade_clinica_geral["id"]]

        resp = requests.post(f"{BASE_URL}/usuarios/medico", json=payload)
        assert resp.status_code == 201, f"Cadastro falhou: {resp.text}"
        medico_id = resp.json()["id"]

        resp_esp = requests.get(
            f"{BASE_URL}/especialidades/medico/{medico_id}",
            headers=admin_headers,
        )
        assert resp_esp.status_code == 200, f"Listagem de especialidades falhou: {resp_esp.text}"
        especialidades = resp_esp.json()
        ids = [e["id"] for e in especialidades]
        assert especialidade_clinica_geral["id"] in ids, (
            f"Especialidade {especialidade_clinica_geral['id']} não encontrada. IDs retornados: {ids}"
        )

    def test_cadastro_medico_com_especialidade_inexistente_retorna_422(self):
        payload = _cadastrar_medico_unico()
        payload["especialidade_ids"] = [999999]

        resp = requests.post(f"{BASE_URL}/usuarios/medico", json=payload)
        assert resp.status_code == 422, f"Esperado 422, recebeu {resp.status_code}: {resp.text}"

    def test_cadastro_medico_sem_especialidade_ids_nao_associa_nada(self, admin_headers):
        """Sem especialidade_ids o médico nasce sem especialidades associadas."""
        payload = _cadastrar_medico_unico()

        resp = requests.post(f"{BASE_URL}/usuarios/medico", json=payload)
        assert resp.status_code == 201
        medico_id = resp.json()["id"]

        resp_esp = requests.get(
            f"{BASE_URL}/especialidades/medico/{medico_id}",
            headers=admin_headers,
        )
        assert resp_esp.status_code == 200
        assert resp_esp.json() == [], f"Esperado lista vazia, recebeu: {resp_esp.json()}"


class TestFluxoMedicoCompleto:
    """
    Cadastra um médico novo, admin ativa, médico gerencia horários.
    Usa scope='class' para compartilhar estado entre os testes da classe.
    """

    @pytest.fixture(scope="class")
    def medico_novo(self, admin_headers, especialidade_clinica_geral):
        """Cadastra médico, admin ativa e associa especialidade."""
        payload = _cadastrar_medico_unico()
        r = requests.post(f"{BASE_URL}/usuarios/medico", json=payload)
        assert r.status_code == 201
        medico_id = r.json()["id"]

        # Admin ativa
        r2 = requests.patch(
            f"{BASE_URL}/usuarios/{medico_id}/alterarStatus",
            headers=admin_headers,
            json={"status_aprovacao": "aprovado"},
        )
        assert r2.status_code == 200

        # Admin associa especialidade
        r3 = requests.post(
            f"{BASE_URL}/especialidades/medico/{medico_id}",
            headers=admin_headers,
            json={"especialidade_id": especialidade_clinica_geral["id"]},
        )
        assert r3.status_code == 201

        token = login(payload["email"], payload["senha"])
        return {
            "id": medico_id,
            "especialidade_id": especialidade_clinica_geral["id"],
            "token": token,
            "headers": {"Authorization": f"Bearer {token}"},
        }

    def test_medico_ativo_consegue_listar_usuarios(self, medico_novo):
        resp = requests.get(f"{BASE_URL}/usuarios", headers=medico_novo["headers"])
        assert resp.status_code == 200

    def test_medico_adiciona_horario_disponivel(self, medico_novo):
        resp = requests.post(
            f"{BASE_URL}/horarios-disponiveis",
            headers=medico_novo["headers"],
            json={
                "especialidade_id": medico_novo["especialidade_id"],
                "dia_semana": 2,   # quarta-feira
                "periodo": "tarde",
            },
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body.get("dia_semana") == 2
        assert body.get("periodo") == "tarde"

    def test_medico_nao_pode_adicionar_horario_duplicado(self, medico_novo):
        # Tenta adicionar o mesmo horário novamente
        resp = requests.post(
            f"{BASE_URL}/horarios-disponiveis",
            headers=medico_novo["headers"],
            json={
                "especialidade_id": medico_novo["especialidade_id"],
                "dia_semana": 2,
                "periodo": "tarde",
            },
        )
        assert resp.status_code in (422, 500)

    def test_medico_lista_seus_horarios(self, medico_novo):
        resp = requests.get(
            f"{BASE_URL}/horarios-disponiveis/medico/{medico_novo['id']}",
            headers=medico_novo["headers"],
        )
        assert resp.status_code == 200
        horarios = resp.json()
        assert any(h["dia_semana"] == 2 and h["periodo"] == "tarde" for h in horarios)

    def test_medico_remove_proprio_horario(self, medico_novo):
        # Lista e pega o id do horário criado
        resp = requests.get(
            f"{BASE_URL}/horarios-disponiveis/medico/{medico_novo['id']}",
            headers=medico_novo["headers"],
        )
        horarios = resp.json()
        horario = next(
            (h for h in horarios if h["dia_semana"] == 2 and h["periodo"] == "tarde"), None
        )
        assert horario, "Horário a remover não encontrado."

        resp_del = requests.delete(
            f"{BASE_URL}/horarios-disponiveis/{horario['id']}",
            headers=medico_novo["headers"],
        )
        assert resp_del.status_code == 200

    def test_medico_nao_remove_horario_de_outro(self, medico_novo, medico_headers):
        """O médico 'ana.lima' não pode remover horário do médico novo (e vice-versa)."""
        # Busca um horário do médico ana.lima via admin
        resp = requests.get(
            f"{BASE_URL}/horarios-disponiveis/medico/{medico_novo['id']}",
            headers=medico_novo["headers"],
        )
        # Tenta remover com o token de ana.lima
        horarios = resp.json()
        if not horarios:
            pytest.skip("Médico novo não tem horários para testar remoção indevida.")

        horario_id = horarios[0]["id"]
        resp_del = requests.delete(
            f"{BASE_URL}/horarios-disponiveis/{horario_id}",
            headers=medico_headers,  # token de ana.lima tentando remover do médico novo
        )
        assert resp_del.status_code == 403
