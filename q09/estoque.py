"""Questão 9 - Estoque da loja de camping (menu)."""
import banco_estoque


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Não pode ficar vazio.")


def ler_inteiro(mensagem, minimo, vazio=None):
    while True:
        texto = input(mensagem).strip()
        if texto == "" and vazio is not None:
            return vazio
        try:
            valor = int(texto)
        except ValueError:
            print("Digite um número inteiro.")
            continue
        if valor < minimo:
            print(f"O valor mínimo é {minimo}.")
        else:
            return valor


def ler_preco(mensagem):
    while True:
        texto = input(mensagem).replace("R$", "").strip().replace(",", ".")
        try:
            valor = float(texto)
            if 0 < valor < float("inf"):
                return valor
        except ValueError:
            pass
        print("Digite um preço maior que zero.")


def mostrar(linhas, marcar=True):
    if len(linhas) == 0:
        print("Nenhum produto encontrado.")
        return
    print(f"{'Id':>3} {'Produto':<20} {'Categoria':<12} {'Preço':>8} {'Qtd':>4}")
    for id, nome, categoria, preco, qtd, minimo in linhas:
        aviso = " <- repor" if marcar and qtd < minimo else ""
        print(f"{id:>3} {nome:<20} {categoria:<12} {preco:>8.2f} {qtd:>4}{aviso}")


def main():
    conn = banco_estoque.conectar()
    while True:
        print("===== ESTOQUE - LOJA DE CAMPING =====")
        print("1 - Cadastrar produto\n2 - Listar produtos\n3 - Buscar por nome")
        print("4 - Entrada (chegou mercadoria)\n5 - Saída (venda)")
        print("6 - Produtos para repor\n7 - Valor total do estoque\n0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            nome = ler_texto("Nome: ")
            categoria = ler_texto("Categoria: ")
            preco = ler_preco("Preço: R$ ")
            qtd = ler_inteiro("Quantidade inicial (Enter = 0): ", 0, vazio=0)
            minimo = ler_inteiro("Estoque mínimo (Enter = 5): ", 0, vazio=5)
            novo = banco_estoque.cadastrar(conn, nome, categoria, preco, qtd, minimo)
            print(f"Cadastrado com id {novo}.")
        elif opcao == "2":
            mostrar(banco_estoque.listar(conn))
        elif opcao == "3":
            mostrar(banco_estoque.buscar(conn, input("Parte do nome: ").strip()))
        elif opcao == "4":
            id = ler_inteiro("Id do produto: ", 1)
            qtd = ler_inteiro("Quantidade que chegou: ", 1)
            if banco_estoque.entrada(conn, id, qtd):
                print("Entrada registrada.")
            else:
                print("Produto não encontrado.")
        elif opcao == "5":
            id = ler_inteiro("Id do produto: ", 1)
            qtd = ler_inteiro("Quantidade vendida: ", 1)
            print(banco_estoque.saida(conn, id, qtd))
        elif opcao == "6":
            mostrar(banco_estoque.estoque_baixo(conn))
        elif opcao == "7":
            print(f"Valor total em estoque: R$ {banco_estoque.valor_total(conn):.2f}")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
    conn.close()


if __name__ == "__main__":
    main()
