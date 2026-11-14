"""Questão 2 - Ônibus da excursão."""

LUGARES = 44
CUSTO_ONIBUS = 1800.00
ALUNOS_POR_PROFESSOR = 15


def ler_inteiro(mensagem, minimo, aviso):
    while True:
        try:
            valor = int(input(mensagem).strip())
        except ValueError:
            print(aviso)
            continue
        if valor < minimo:
            print(aviso)
        else:
            return valor


def main():
    print("=== EXCURSÃO DA ESCOLA ===")
    qtd_turmas = ler_inteiro("Quantas turmas vão participar? ", 1,
                             "Digite um número inteiro maior que zero.")
    nomes = []
    inscritos = []
    for i in range(1, qtd_turmas + 1):
        nome = input(f"Nome da turma {i}: ").strip()
        while nome == "":
            print("Digite o nome da turma.")
            nome = input(f"Nome da turma {i}: ").strip()
        n = ler_inteiro(f"Inscritos na turma {nome}: ", 0,
                        "Digite um número inteiro (0 ou mais).")
        nomes.append(nome)
        inscritos.append(n)

    alunos = sum(inscritos)
    professores = (alunos + ALUNOS_POR_PROFESSOR - 1) // ALUNOS_POR_PROFESSOR
    pessoas = alunos + professores
    onibus = (pessoas + LUGARES - 1) // LUGARES
    sobram = onibus * LUGARES - pessoas
    custo = onibus * CUSTO_ONIBUS
    maior = inscritos.index(max(inscritos))

    print("=== RESUMO ===")
    print(f"Alunos: {alunos}")
    print(f"Professores acompanhantes: {professores}")
    print(f"Total de pessoas: {pessoas}")
    print(f"Ônibus necessários: {onibus} (sobram {sobram} lugares)")
    print(f"Custo total: R$ {custo:.2f}")
    if alunos > 0:
        print(f"Valor por aluno: R$ {custo / alunos:.2f}")
    else:
        print("Valor por aluno: não há alunos inscritos.")
    print(f"Turma com mais inscritos: {nomes[maior]} ({inscritos[maior]} alunos)")


if __name__ == "__main__":
    main()
