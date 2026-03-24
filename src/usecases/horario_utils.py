SLOTS_POR_PERIODO: dict[str, list[str]] = {
    "manha": [
        "06:00", "06:30", "07:00", "07:30", "08:00", "08:30",
        "09:00", "09:30", "10:00", "10:30", "11:00",
    ],
    "tarde": [
        "13:00", "13:30", "14:00", "14:30", "15:00",
        "15:30", "16:00", "16:30", "17:00",
    ],
    "noite": [
        "19:00", "19:30", "20:00", "20:30", "21:00", "21:30",
        "22:00", "22:30", "23:00", "23:30", "00:00", "00:30", "01:00",
    ],
}


def _minutos(hora: str) -> int:
    h, m = hora.split(":")
    return int(h) * 60 + int(m)


def sobrepostos(hora_a: str, hora_b: str) -> bool:
    """Retorna True se duas consultas de 1h iniciando em hora_a e hora_b se sobrepoem."""
    a = _minutos(hora_a)
    b = _minutos(hora_b)
    diff = abs(a - b)
    diff = min(diff, 24 * 60 - diff)  # wrap meia-noite
    return diff < 60
