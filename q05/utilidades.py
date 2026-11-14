"""Módulo de utilidades: leitura do teclado e separadores."""


def ler_texto(mensagem, vazio=False):
    """Lê um texto. Se vazio=False, repete até digitarem algo."""
    while True:
        texto = input(mensagem).strip()
        if texto != "" or vazio:
            return texto
        print("Digite algum texto.")


def ler_inteiro(mensagem, minimo=None, maximo=None):
    """Lê um número inteiro, conferindo os limites (se informados)."""
    while True:
        try:
            valor = int(input(mensagem).strip())
        except ValueError:
            print("Digite um número inteiro.")
            continue
        if minimo is not None and valor < minimo:
            print(f"O mínimo é {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"O máximo é {maximo}.")
        else:
            return valor


def linha(caractere="-", tamanho=40):
    """Devolve uma linha de separação."""
    return caractere * tamanho


# Este bloco só roda com:  python utilidades.py
if __name__ == "__main__":
    assert linha("=", 5) == "====="
    assert linha() == "-" * 40
    print("linha OK")
    print("Teste de ler_texto (digite algo):")
    print("Você digitou:", ler_texto("Nome: "))
    print("Teste de ler_texto com vazio=True (pode dar Enter):")
    print("Você digitou:", repr(ler_texto("Texto: ", vazio=True)))
    print("Teste de ler_inteiro de 1 a 6:")
    print("Você digitou:", ler_inteiro("Qtd: ", 1, 6))
