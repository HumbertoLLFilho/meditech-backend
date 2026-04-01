import pytest

from src.usecases.horario_utils import sobrepostos, SLOTS_POR_PERIODO


class TestSobrepostos:
    def test_mesma_hora_se_sobrepoe(self):
        assert sobrepostos("09:00", "09:00") is True

    def test_30min_depois_se_sobrepoe(self):
        assert sobrepostos("09:30", "09:00") is True

    def test_59min_depois_se_sobrepoe(self):
        assert sobrepostos("09:59", "09:00") is True

    def test_exatamente_1h_depois_nao_sobrepos(self):
        assert sobrepostos("10:00", "09:00") is False

    def test_2h_depois_nao_sobrepos(self):
        assert sobrepostos("11:00", "09:00") is False

    def test_wrap_meia_noite_sobrepos(self):
        assert sobrepostos("00:00", "23:30") is True

    def test_wrap_meia_noite_nao_sobrepos(self):
        assert sobrepostos("01:30", "23:30") is False


class TestSlotsPorPeriodo:
    def test_todos_periodos_existem(self):
        assert "manha" in SLOTS_POR_PERIODO
        assert "tarde" in SLOTS_POR_PERIODO
        assert "noite" in SLOTS_POR_PERIODO

    def test_slots_sao_multiplos_de_30min(self):
        for periodo, slots in SLOTS_POR_PERIODO.items():
            for slot in slots:
                minutos = int(slot.split(":")[1])
                assert minutos in (0, 30), (
                    f"Slot {slot} em '{periodo}' nao e multiplo de 30min"
                )

    def test_manha_comeca_as_6h(self):
        assert SLOTS_POR_PERIODO["manha"][0] == "06:00"

    def test_noite_inclui_meia_noite(self):
        assert "00:00" in SLOTS_POR_PERIODO["noite"]
