"""Questão 5 - Sorteio de brindes da Feira de Ciências."""
import random
from datetime import datetime

import utilidades


def ler_participantes():
    print("Digite os nomes dos participantes (Enter vazio para terminar).")
    participantes = []
    while True:
        nome = utilidades.ler_texto(f"Participante {len(participantes) + 1}: ", vazio=True)
        if nome == "":
            return participantes
        existentes = [p.lower() for p in participantes]
        if nome.lower() in existentes:
            print(f"{nome} já está na lista.")
        else:
            participantes.append(nome)


def main():
    print(utilidades.linha("="))
    print("SORTEIO DE BRINDES - FEIRA DE CIÊNCIAS")
    print(utilidades.linha("="))
    participantes = ler_participantes()
    if len(participantes) == 0:
        print("Nenhum participante: não há o que sortear.")
        return

    qtd = utilidades.ler_inteiro(f"Quantos brindes (1 a {len(participantes)})? ",
                                 1, len(participantes))
    brindes = []
    for i in range(1, qtd + 1):
        brindes.append(utilidades.ler_texto(f"Brinde {i}: "))

    ganhadores = random.sample(participantes, qtd)
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    print(utilidades.linha())
    print(f"Sorteio realizado em {agora}")
    print(f"{len(participantes)} participantes, {qtd} brindes")
    print(utilidades.linha())
    for i in range(qtd):
        print(f"{brindes[i]} -> {ganhadores[i]}")


if __name__ == "__main__":
    main()
