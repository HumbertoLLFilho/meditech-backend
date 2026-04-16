"""
Testes de integração — Fluxo completo do paciente

Cobre:
  1. Cadastro de paciente
  2. Login
  3. Listagem de médicos ativos
  4. Listagem de especialidades
  5. Consulta de disponibilidade
  6. Agendamento de consulta
  7. Listagem de consultas (vê a própria)
  8. Conflito de horário (tenta agendar no mesmo slot)
  9. Cancelamento de consulta
"""

import requests
import pytest
from tests.integration.helpers import BASE_URL


class TestCadastroELoginPaciente:
    def test_cadastro_retorna_201_com_id(self, paciente_cadastrado):
        assert paciente_cadastrado["id"] is not None

    def test_login_apos_cadastro_retorna_token(self, paciente_cadastrado):
        assert paciente_cadastrado["token"] != ""

    def test_cadastro_email_duplicado_retorna_422(self, paciente_cadastrado):
        payload = {
            "nome": "Outro",
            "sobrenome": "Paciente",
            "data_nascimento": "1990-01-01",
            "genero": "feminino",
            "email": paciente_cadastrado["email"],  # mesmo email
            "senha": "Outro@1234",
            "cpf": "00000000099",
            "telefone": "11900000099",
        }
        resp = requests.post(f"{BASE_URL}/usuarios", json=payload)
        assert resp.status_code == 422


class TestListagemPorPaciente:
    def test_paciente_ve_somente_medicos_ativos(self, paciente_cadastrado):
        resp = requests.get(f"{BASE_URL}/usuarios", headers=paciente_cadastrado["headers"])
        assert resp.status_code == 200
        usuarios = resp.json()
        assert len(usuarios) > 0
        for u in usuarios:
            assert u["tipo"] == "medico"
            assert u["ativo"] is True

    def test_listar_especialidades(self, paciente_cadastrado):
        resp = requests.get(
            f"{BASE_URL}/especialidades", headers=paciente_cadastrado["headers"]
        )
        assert resp.status_code == 200
        especialidades = resp.json()
        assert len(especialidades) >= 10
        nomes = [e["nome"] for e in especialidades]
        assert "Cardiologia" in nomes


class TestDisponibilidade:
    def test_consultar_disponibilidade_retorna_slots(
        self,
        paciente_cadastrado,
        especialidade_clinica_geral,
        proxima_segunda,
    ):
        resp = requests.get(
            f"{BASE_URL}/horarios-disponiveis/disponivel",
            headers=paciente_cadastrado["headers"],
            params={
                "especialidade_id": especialidade_clinica_geral["id"],
                "data": proxima_segunda,
                "periodo": "manha",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list)
        assert len(body) > 0, "Esperava médicos disponíveis na próxima segunda manhã para Clínica Geral"
        primeiro = body[0]
        assert "medico_id" in primeiro
        assert "horarios" in primeiro
        assert len(primeiro["horarios"]) > 0

    def test_disponibilidade_sem_parametros_retorna_422(self, paciente_cadastrado):
        resp = requests.get(
            f"{BASE_URL}/horarios-disponiveis/disponivel",
            headers=paciente_cadastrado["headers"],
        )
        assert resp.status_code == 422


class TestAgendamentoDeConsulta:
    """
    Esse bloco depende de um slot disponível na próxima segunda-feira manhã
    para a especialidade Clínica Geral (médicos do seed têm esse horário).
    """

    @pytest.fixture(scope="class")
    def slot_disponivel(
        self,
        paciente_cadastrado,
        especialidade_clinica_geral,
        proxima_segunda,
    ):
        """Descobre o primeiro médico+horário disponível."""
        resp = requests.get(
            f"{BASE_URL}/horarios-disponiveis/disponivel",
            headers=paciente_cadastrado["headers"],
            params={
                "especialidade_id": especialidade_clinica_geral["id"],
                "data": proxima_segunda,
                "periodo": "manha",
            },
        )
        assert resp.status_code == 200
        disponibilidades = resp.json()
        assert disponibilidades, "Nenhum slot disponível para o teste de agendamento."
        primeiro_medico = disponibilidades[0]
        return {
            "medico_id": primeiro_medico["medico_id"],
            "hora": primeiro_medico["horarios"][0],
        }

    @pytest.fixture(scope="class")
    def consulta_agendada(
        self,
        paciente_cadastrado,
        especialidade_clinica_geral,
        proxima_segunda,
        slot_disponivel,
    ):
        """Agenda a consulta e retorna o dict de resposta."""
        payload = {
            "medico_id": slot_disponivel["medico_id"],
            "especialidade_id": especialidade_clinica_geral["id"],
            "data_agendada": proxima_segunda,
            "hora": slot_disponivel["hora"],
        }
        resp = requests.post(
            f"{BASE_URL}/consultas",
            headers=paciente_cadastrado["headers"],
            json=payload,
        )
        assert resp.status_code == 201, f"Agendamento falhou: {resp.text}"
        return resp.json()

    def test_agendamento_retorna_201_com_id(self, consulta_agendada):
        assert "id" in consulta_agendada

    def test_listar_consultas_inclui_agendada(self, paciente_cadastrado, consulta_agendada):
        resp = requests.get(
            f"{BASE_URL}/consultas", headers=paciente_cadastrado["headers"]
        )
        assert resp.status_code == 200
        ids = [c["id"] for c in resp.json()]
        assert consulta_agendada["id"] in ids

    def test_conflito_no_mesmo_horario_retorna_422(
        self,
        paciente_cadastrado,
        especialidade_clinica_geral,
        proxima_segunda,
        slot_disponivel,
        consulta_agendada,
    ):
        """Tenta agendar outro paciente no mesmo médico/hora que acabou de ser ocupado."""
        import uuid
        sufixo = uuid.uuid4().hex[:8]
        payload_paciente2 = {
            "nome": "Conflito",
            "sobrenome": "Teste",
            "data_nascimento": "1995-01-01",
            "genero": "masculino",
            "email": f"conflito.{sufixo}@example.com",
            "senha": "Conflito@1234",
            "cpf": f"111{sufixo[:8]}",
            "telefone": "11988887777",
        }
        r = requests.post(f"{BASE_URL}/usuarios", json=payload_paciente2)
        assert r.status_code == 201
        token2 = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": payload_paciente2["email"], "senha": payload_paciente2["senha"]},
        ).json()["access_token"]

        resp = requests.post(
            f"{BASE_URL}/consultas",
            headers={"Authorization": f"Bearer {token2}"},
            json={
                "medico_id": slot_disponivel["medico_id"],
                "especialidade_id": especialidade_clinica_geral["id"],
                "data_agendada": proxima_segunda,
                "hora": slot_disponivel["hora"],
            },
        )
        assert resp.status_code == 422

    def test_cancelar_consulta(self, paciente_cadastrado, consulta_agendada):
        resp = requests.patch(
            f"{BASE_URL}/consultas/{consulta_agendada['id']}/cancelar",
            headers=paciente_cadastrado["headers"],
        )
        assert resp.status_code == 200
