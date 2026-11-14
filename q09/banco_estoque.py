"""Comandos SQL do estoque da loja de camping."""
import sqlite3


def conectar(arquivo="estoque.db"):
    conn = sqlite3.connect(arquivo)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nome       TEXT NOT NULL,
            categoria  TEXT NOT NULL,
            preco      REAL NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            minimo     INTEGER NOT NULL DEFAULT 5
        )
    """)
    conn.commit()
    return conn


COLUNAS = "id, nome, categoria, preco, quantidade, minimo"


def cadastrar(conn, nome, categoria, preco, quantidade=0, minimo=5):
    cursor = conn.execute(
        "INSERT INTO produtos (nome, categoria, preco, quantidade, minimo) "
        "VALUES (?, ?, ?, ?, ?)", (nome, categoria, preco, quantidade, minimo))
    conn.commit()
    return cursor.lastrowid


def listar(conn):
    return conn.execute(
        f"SELECT {COLUNAS} FROM produtos ORDER BY nome COLLATE NOCASE").fetchall()


def buscar(conn, texto):
    return conn.execute(
        f"SELECT {COLUNAS} FROM produtos WHERE nome LIKE ? ORDER BY nome COLLATE NOCASE",
        ("%" + texto + "%",)).fetchall()


def entrada(conn, id, quantidade):
    """Soma ao estoque. Devolve False se o id não existe."""
    if quantidade < 1:
        raise ValueError("A quantidade deve ser pelo menos 1.")
    cursor = conn.execute(
        "UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, id))
    conn.commit()
    return cursor.rowcount > 0


def saida(conn, id, quantidade):
    """Tira do estoque sem deixar negativo. Devolve uma mensagem."""
    if quantidade < 1:
        return "Quantidade inválida."
    linha = conn.execute(
        "SELECT nome, quantidade FROM produtos WHERE id = ?", (id,)).fetchone()
    if linha is None:
        return "Produto não encontrado."
    nome, tem = linha
    if quantidade > tem:
        return f"Estoque insuficiente: há {tem} unidade(s) de {nome}."
    conn.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?",
                 (quantidade, id))
    conn.commit()
    return f"Saída registrada: {quantidade} x {nome}."


def estoque_baixo(conn):
    return conn.execute(
        f"SELECT {COLUNAS} FROM produtos WHERE quantidade < minimo "
        "ORDER BY nome COLLATE NOCASE").fetchall()


def valor_total(conn):
    total = conn.execute("SELECT SUM(preco * quantidade) FROM produtos").fetchone()[0]
    if total is None:
        return 0
    return round(total, 2)
