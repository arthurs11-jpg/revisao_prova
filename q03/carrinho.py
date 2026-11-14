"""Questão 3 - Carrinho da loja virtual."""

CUPONS = {"PROMO10": 10, "VOLTAASAULAS": 15, "BLACK25": 25}


def subtotal_item(preco, quantidade=1):
    return preco * quantidade


def aplicar_cupom(total, cupom):
    """Devolve (novo_total, percentual). Cupom inválido ou vazio = 0%."""
    chave = str(cupom).replace(" ", "").upper()
    percentual = CUPONS.get(chave, 0)
    novo_total = total - total * percentual / 100
    return novo_total, percentual


def calcular_frete(total, gratis_acima=200.0, valor=25.0):
    if total >= gratis_acima:
        return 0.0
    return valor


def valor_parcela(total, parcelas=1):
    if parcelas <= 6:
        return total / parcelas
    return total * (1 + 0.02 * parcelas) / parcelas


# ---------- leitura do teclado ----------
def ler_preco():
    while True:
        texto = input("Preço: R$ ").strip().replace("R$", "").strip()
        try:
            valor = float(texto.replace(",", "."))
        except ValueError:
            valor = 0
        if valor > 0 and valor != float("inf"):
            return valor
        print("Digite um valor maior que zero.")


def ler_quantidade():
    while True:
        try:
            q = int(input("Quantidade: ").strip())
        except ValueError:
            q = 0
        if q > 0:
            return q
        print("Digite uma quantidade inteira maior que zero.")


def ler_parcelas():
    while True:
        try:
            p = int(input("Em quantas parcelas (1 a 12)? ").strip())
        except ValueError:
            p = 0
        if 1 <= p <= 12:
            return p
        print("Digite um número inteiro de 1 a 12.")


def main():
    print("=== LOJA VIRTUAL ===")
    carrinho = 0.0
    while True:
        produto = input("Produto (Enter para fechar o carrinho): ").strip()
        if produto == "":
            break
        preco = ler_preco()
        quantidade = ler_quantidade()
        sub = subtotal_item(preco, quantidade)
        carrinho = carrinho + sub
        print(f" {quantidade} x {produto} = R$ {sub:.2f} (carrinho: R$ {carrinho:.2f})")

    if carrinho == 0:
        print("Carrinho vazio. Nada a pagar.")
        return

    cupom = input("Cupom de desconto (Enter se não tiver): ")
    com_desconto, percentual = aplicar_cupom(carrinho, cupom)
    if cupom.strip() != "" and percentual == 0:
        print("Cupom inválido. Nenhum desconto aplicado.")
    frete = calcular_frete(com_desconto)
    total = com_desconto + frete
    parcelas = ler_parcelas()

    print("=== NOTA ===")
    print(f"Subtotal: R$ {carrinho:.2f}")
    print(f"Desconto: {percentual}% (R$ {carrinho - com_desconto:.2f})")
    print(f"Frete: R$ {frete:.2f}")
    print(f"Total: R$ {total:.2f}")
    print(f"Pagamento: {parcelas} x R$ {valor_parcela(total, parcelas):.2f}")


if __name__ == "__main__":
    main()
