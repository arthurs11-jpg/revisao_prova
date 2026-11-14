"""Questão 4 - Planejador de maratona de série."""


def formatar_duracao(minutos):
    horas = minutos // 60
    resto = minutos % 60
    if horas == 0:
        return f"{resto}min"
    return f"{horas}h{resto:02d}min"


def tempo_total(duracoes):
    total = 0
    for d in duracoes:
        total = total + d
    return total


def dias_para_terminar(total_minutos, minutos_por_dia=120):
    return (total_minutos + minutos_por_dia - 1) // minutos_por_dia


def classificar_maratona(total_minutos):
    if total_minutos < 300:
        return "Leve"
    elif total_minutos <= 900:
        return "Média"
    else:
        return "Intensa"


def ler_inteiro(mensagem, minimo=1):
    while True:
        try:
            valor = int(input(mensagem).strip())
        except ValueError:
            print("Digite um número inteiro.")
            continue
        if valor < minimo:
            print(f"O valor mínimo é {minimo}.")
        else:
            return valor


def main():
    print("=== MARATONA DE SÉRIE ===")
    serie = input("Nome da série: ").strip()
    while serie == "":
        serie = input("Nome da série: ").strip()
    temporadas = ler_inteiro("Quantas temporadas? ")
    tempos = []
    for i in range(1, temporadas + 1):
        episodios = ler_inteiro(f"Temporada {i} - número de episódios: ")
        duracao = ler_inteiro(f"Temporada {i} - duração média do episódio (min): ")
        tempos.append(episodios * duracao)

    total = tempo_total(tempos)
    print(f"=== {serie.upper()} ===")
    for i in range(len(tempos)):
        print(f"Temporada {i + 1}: {formatar_duracao(tempos[i])}")
    print(f"Total: {formatar_duracao(total)} ({classificar_maratona(total)})")

    por_dia = ler_inteiro("Quantos minutos por dia você pode assistir? ")
    print(f"Você termina {serie} em {dias_para_terminar(total, por_dia)} dias.")
    print(f"Com 2 horas por dia (padrão), seriam {dias_para_terminar(total)} dias.")


if __name__ == "__main__":
    main()
