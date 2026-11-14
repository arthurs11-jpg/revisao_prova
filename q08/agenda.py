"""Questão 8 - Agenda de shows (JSON)."""
import json
import os
from datetime import datetime

ARQUIVO = "shows.json"


def carregar(caminho=ARQUIVO):
    if not os.path.exists(caminho):
        return []
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except ValueError:
        print("Aviso: shows.json está com defeito; começando com a agenda vazia.")
        return []


def salvar(shows, caminho=ARQUIVO):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(shows, f, ensure_ascii=False, indent=2)


def converter_data(texto):
    return datetime.strptime(texto.strip(), "%d/%m/%Y")


def ordenados(shows):
    return sorted(shows, key=lambda s: converter_data(s["data"]))


def mostrar(lista):
    if len(lista) == 0:
        print("Nenhum show encontrado.")
    numero = 1
    for s in lista:
        if s["ingressos"] == 0:
            ing = "ESGOTADO"
        else:
            ing = f"{s['ingressos']} ingressos"
        print(f"{numero}. {s['data']} {s['artista']:<20} {s['cidade']:<14} "
              f"R$ {s['preco']:.2f} {ing}")
        numero = numero + 1


# ---------- leituras com validação ----------
def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Não pode ficar vazio.")


def ler_data(mensagem):
    texto = input(mensagem)
    while True:
        try:
            return converter_data(texto).strftime("%d/%m/%Y")
        except ValueError:
            texto = input("Data inválida. Digite no formato dd/mm/aaaa: ")


def ler_preco(mensagem):
    while True:
        texto = input(mensagem).replace("R$", "").strip().replace(",", ".")
        try:
            valor = float(texto)
            if valor >= 0 and valor != float("inf"):
                return valor
        except ValueError:
            pass
        print("Digite um valor válido (0 ou mais).")


def ler_inteiro(mensagem, minimo, maximo=None):
    while True:
        try:
            valor = int(input(mensagem).strip())
        except ValueError:
            print("Digite um número inteiro.")
            continue
        if valor < minimo:
            print(f"O mínimo é {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"O máximo é {maximo}.")
        else:
            return valor


def escolher_show(shows):
    """Mostra a lista e devolve o show escolhido pelo número."""
    lista = ordenados(shows)
    mostrar(lista)
    numero = ler_inteiro("Número do show: ", 1, len(lista))
    return lista[numero - 1]


# ---------- ações ----------
def cadastrar(shows):
    artista = ler_texto("Artista/banda: ")
    cidade = ler_texto("Cidade: ")
    data = ler_data("Data (dd/mm/aaaa): ")
    preco = ler_preco("Preço do ingresso: R$ ")
    ingressos = ler_inteiro("Ingressos disponíveis: ", 0)
    shows.append({"artista": artista, "cidade": cidade, "data": data,
                  "preco": preco, "ingressos": ingressos})
    salvar(shows)
    print("Show cadastrado e agenda salva.")


def shows_na_cidade(shows, cidade):
    return [s for s in ordenados(shows) if s["cidade"].lower() == cidade.strip().lower()]


def vender(shows):
    if len(shows) == 0:
        print("Nenhum show na agenda.")
        return
    show = escolher_show(shows)
    if show["ingressos"] == 0:
        print("Show esgotado.")
        return
    while True:
        qtd = ler_inteiro("Quantos ingressos? ", 1)
        if qtd <= show["ingressos"]:
            break
        print(f"Só restam {show['ingressos']} ingressos.")
    show["ingressos"] = show["ingressos"] - qtd
    salvar(shows)
    print(f"Venda: {qtd} x R$ {show['preco']:.2f} = R$ {qtd * show['preco']:.2f}")


def remover(shows):
    if len(shows) == 0:
        print("Nenhum show na agenda.")
        return
    show = escolher_show(shows)
    shows.remove(show)
    salvar(shows)
    print(f"Show de {show['artista']} removido.")


def main():
    shows = carregar()
    print(f"Agenda carregada: {len(shows)} shows.")
    while True:
        print("===== AGENDA DE SHOWS =====")
        print("1 - Listar shows\n2 - Cadastrar show\n3 - Shows em uma cidade")
        print("4 - Vender ingressos\n5 - Remover show\n0 - Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "1":
            mostrar(ordenados(shows))
        elif opcao == "2":
            cadastrar(shows)
        elif opcao == "3":
            mostrar(shows_na_cidade(shows, input("Cidade: ")))
        elif opcao == "4":
            vender(shows)
        elif opcao == "5":
            remover(shows)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
