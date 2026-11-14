"""Questão 1 - Mochila de camping."""
import math

LIMITE = 15.0


def ler_peso():
    """Pede o peso até receber um número maior que zero (aceita vírgula)."""
    while True:
        texto = input("Peso (kg): ").strip()
        try:
            peso = float(texto.replace(",", "."))
        except ValueError:
            print("Digite um número, por exemplo 1.5")
            continue
        if not math.isfinite(peso):
            print("Digite um número, por exemplo 1.5")
        elif peso <= 0:
            print("O peso deve ser maior que zero.")
        else:
            return peso


def main():
    nomes = []
    pesos = []
    print("=== MOCHILA DE CAMPING ===")
    print("Digite os itens. Para terminar, digite FIM.")
    while True:
        nome = input("Item: ").strip()
        if nome.upper() == "FIM":
            break
        if nome == "":
            print("Digite o nome do item.")
            continue
        peso = ler_peso()
        nomes.append(nome)
        pesos.append(peso)
        total = sum(pesos)
        if total > LIMITE:
            print(f"Atenção: a mochila já tem {round(total, 2)} kg (limite 15 kg)!")

    if len(nomes) == 0:
        print("A mochila está vazia.")
        return

    total = sum(pesos)
    print("=== RESUMO ===")
    for i in range(len(nomes)):
        print(f"{i + 1}. {nomes[i]} {round(pesos[i], 2)} kg")
    mais_pesado = pesos.index(max(pesos))
    print(f"Itens: {len(nomes)}")
    print(f"Peso total: {round(total, 2)} kg")
    print(f"Peso médio: {total / len(nomes):.2f} kg")
    print(f"Item mais pesado: {nomes[mais_pesado]} ({round(pesos[mais_pesado], 2)} kg)")
    if total > LIMITE:
        print(f"Tire {round(total - LIMITE, 2)} kg da mochila para ficar dentro do limite.")
    else:
        print(f"Ainda cabem {round(LIMITE - total, 2)} kg na mochila.")


if __name__ == "__main__":
    main()
