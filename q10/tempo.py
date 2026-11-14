"""Módulo de tempo (reaproveitado da Questão 4)."""


def formatar_duracao(minutos):
    horas = minutos // 60
    resto = minutos % 60
    if horas == 0:
        return f"{resto}min"
    return f"{horas}h{resto:02d}min"


if __name__ == "__main__":
    assert formatar_duracao(125) == "2h05min"
    assert formatar_duracao(45) == "45min"
    assert formatar_duracao(120) == "2h00min"
    print("tempo.py OK")
