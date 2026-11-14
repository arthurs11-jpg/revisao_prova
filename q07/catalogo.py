"""Questão 7 - Catálogo da plataforma de streaming (JSON)."""
import json

ARQUIVO = "catalogo.json"


def carregar_catalogo(caminho=ARQUIVO):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def classificacao_texto(t):
    return "L" if t["classificacao"] == 0 else str(t["classificacao"])


def mostrar(titulos):
    if len(titulos) == 0:
        print("Nenhum título encontrado.")
    for t in titulos:
        print(f"{t['id']:>2}. {t['titulo']:<20} {t['tipo']:<6} {t['genero']:<13} "
              f"{t['ano']} {classificacao_texto(t):>2} nota {t['nota']}")


def generos(catalogo):
    """Gêneros existentes, sem repetição e em ordem."""
    return sorted(set(t["genero"] for t in catalogo))


def filtrar_por_genero(catalogo, genero):
    return [t for t in catalogo if t["genero"].lower() == genero.strip().lower()]


def buscar_titulo(catalogo, parte):
    return [t for t in catalogo if parte.strip().lower() in t["titulo"].lower()]


def titulos_para_idade(catalogo, idade):
    return [t for t in catalogo if t["classificacao"] <= idade]


def mais_bem_avaliados(catalogo, n=5):
    return sorted(catalogo, key=lambda t: t["nota"], reverse=True)[:n]


def estatisticas(catalogo):
    filmes = len([t for t in catalogo if t["tipo"] == "Filme"])
    series = len([t for t in catalogo if t["tipo"] == "Série"])
    media = sum(t["nota"] for t in catalogo) / len(catalogo) if catalogo else 0
    return {"total": len(catalogo), "filmes": filmes, "series": series,
            "media": media, "generos": generos(catalogo)}


def ler_inteiro(mensagem, minimo, vazio=None):
    """Lê inteiro >= minimo. Se vazio for informado, Enter devolve esse valor."""
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


def main():
    catalogo = carregar_catalogo()
    print(f"Catálogo carregado: {len(catalogo)} títulos.")
    while True:
        print("===== CINEFLIX =====")
        print("1 - Listar tudo")
        print("2 - Filtrar por gênero")
        print("3 - Buscar título")
        print("4 - Títulos para a minha idade")
        print("5 - Mais bem avaliados")
        print("6 - Estatísticas")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            mostrar(catalogo)
        elif opcao == "2":
            print("Gêneros:", ", ".join(generos(catalogo)))
            mostrar(filtrar_por_genero(catalogo, input("Gênero: ")))
        elif opcao == "3":
            mostrar(buscar_titulo(catalogo, input("Parte do título: ")))
        elif opcao == "4":
            mostrar(titulos_para_idade(catalogo, ler_inteiro("Sua idade: ", 0)))
        elif opcao == "5":
            n = ler_inteiro("Quantos (Enter = 5)? ", 1, vazio=5)
            mostrar(mais_bem_avaliados(catalogo, n))
        elif opcao == "6":
            est = estatisticas(catalogo)
            print(f"Títulos: {est['total']} (filmes: {est['filmes']}, séries: {est['series']})")
            print(f"Nota média: {est['media']:.2f}")
            print("Gêneros:", ", ".join(est["generos"]))
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
