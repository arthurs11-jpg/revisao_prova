"""Questão 6 - Balcão de devoluções da biblioteca."""
from datetime import date

import multas


def ler_data(mensagem, enter_e_hoje=False):
    while True:
        texto = input(mensagem).strip()
        if texto == "" and enter_e_hoje:
            return date.today()
        try:
            return multas.converter_data(texto)
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")


def main():
    print("=== BALCÃO DE DEVOLUÇÕES ===")
    devolvidos = 0
    com_atraso = 0
    arrecadado = 0.0
    while True:
        titulo = input("Título do livro (Enter para encerrar): ").strip()
        if titulo == "":
            break
        prevista = ler_data("Data prevista (dd/mm/aaaa): ")
        devolucao = ler_data("Data da devolução (Enter = hoje): ", enter_e_hoje=True)
        dias = multas.dias_de_atraso(prevista, devolucao)
        devolvidos = devolvidos + 1
        if dias == 0:
            print(f"'{titulo}' devolvido no prazo. Obrigado!")
        else:
            multa = multas.valor_multa(dias)
            com_atraso = com_atraso + 1
            arrecadado = arrecadado + multa
            print(f"'{titulo}' com {dias} dia(s) de atraso. Multa: R$ {multa:.2f}")

    print("=== FECHAMENTO DO DIA ===")
    print(f"Livros devolvidos: {devolvidos}")
    print(f"Com atraso: {com_atraso}")
    print(f"Total em multas: R$ {arrecadado:.2f}")


if __name__ == "__main__":
    main()
