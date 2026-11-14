"""Regras de multa da biblioteca."""
from datetime import datetime, date


def converter_data(texto):
    """'dd/mm/aaaa' -> date. Data inválida gera ValueError."""
    return datetime.strptime(texto.strip(), "%d/%m/%Y").date()


def dias_de_atraso(data_prevista, data_devolucao):
    dias = (data_devolucao - data_prevista).days
    if dias < 0:
        return 0
    return dias


def valor_multa(dias, por_dia=1.50, maximo=30.00):
    valor = dias * por_dia
    if valor > maximo:
        return maximo
    return valor


# Testes: rode  python multas.py
if __name__ == "__main__":
    assert converter_data("05/11/2026") == date(2026, 11, 5)
    try:
        converter_data("31/09/2026")
        assert False, "31/09 deveria dar ValueError"
    except ValueError:
        pass
    assert dias_de_atraso(date(2026, 11, 5), date(2026, 11, 10)) == 5
    assert dias_de_atraso(date(2026, 11, 5), date(2026, 11, 1)) == 0
    assert valor_multa(5) == 7.5
    assert valor_multa(40) == 30.0
    assert valor_multa(5, por_dia=2) == 10
    print("Todos os testes passaram!")
