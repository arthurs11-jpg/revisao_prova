"""Questão 10 - Cineflix: histórico e relatórios."""
import json
from datetime import date

import banco_streaming
import tempo

ARQ_RELATORIO = "relatorio.json"


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("Não pode ficar vazio.")


def ler_inteiro(mensagem, minimo):
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


def mostrar_catalogo(conn):
    for id, titulo, tipo, genero, ano, classif, nota in banco_streaming.listar_titulos(conn):
        c = "L" if classif == 0 else str(classif)
        print(f"{id:>2}. {titulo:<20} {tipo:<6} {genero:<13} {ano} {c:>2} nota {nota}")


def mostrar_historico(conn, perfil):
    linhas = banco_streaming.historico(conn, perfil)
    if len(linhas) == 0:
        print("Você ainda não assistiu nada.")
        return
    total = 0
    for data, titulo, minutos in linhas:
        print(f"{data} {titulo} {tempo.formatar_duracao(minutos)}")
        total = total + minutos
    print(f"Total: {tempo.formatar_duracao(total)} em {len(linhas)} sessões")


def exportar_relatorio(conn):
    top = banco_streaming.mais_assistidos(conn)
    perfis = banco_streaming.tempo_por_perfil(conn)
    relatorio = {
        "data": date.today().isoformat(),
        "mais_assistidos": [{"titulo": t, "vezes": v} for t, v in top],
        "tempo_por_perfil": [{"perfil": p, "minutos": m, "tempo": tempo.formatar_duracao(m)}
                             for p, m in perfis],
    }
    with open(ARQ_RELATORIO, "w", encoding="utf-8") as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    print(f"{ARQ_RELATORIO} gravado ({len(top)} títulos, {len(perfis)} perfis).")


def main():
    conn = banco_streaming.conectar()
    importados = banco_streaming.importar_catalogo(conn)
    if importados > 0:
        print(f"{importados} títulos importados do catalogo.json.")
    perfil = ler_texto("Nome do perfil: ")

    while True:
        print(f"===== CINEFLIX ({perfil}) =====")
        print("1 - Ver catálogo\n2 - Registrar que assisti\n3 - Meu histórico")
        print("4 - Mais assistidos\n5 - Tempo assistido por perfil")
        print("6 - Exportar relatório JSON\n7 - Trocar de perfil\n0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            mostrar_catalogo(conn)
        elif opcao == "2":
            id = ler_inteiro("Id do título: ", 1)
            minutos = ler_inteiro("Quantos minutos você assistiu? ", 1)
            if banco_streaming.registrar(conn, perfil, id, minutos):
                print("Registrado!")
            else:
                print("Não existe título com esse id.")
        elif opcao == "3":
            mostrar_historico(conn, perfil)
        elif opcao == "4":
            posicao = 1
            for titulo, vezes in banco_streaming.mais_assistidos(conn):
                print(f"{posicao}º {titulo} {vezes} vez(es)")
                posicao = posicao + 1
            if posicao == 1:
                print("Ninguém assistiu nada ainda.")
        elif opcao == "5":
            linhas = banco_streaming.tempo_por_perfil(conn)
            for nome, minutos in linhas:
                print(f"{nome} {tempo.formatar_duracao(minutos)}")
            if len(linhas) == 0:
                print("Ninguém assistiu nada ainda.")
        elif opcao == "6":
            exportar_relatorio(conn)
        elif opcao == "7":
            perfil = ler_texto("Nome do perfil: ")
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
    conn.close()


if __name__ == "__main__":
    main()
