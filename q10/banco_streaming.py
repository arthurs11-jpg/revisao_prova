"""Banco de dados da Cineflix (SQLite)."""
import json
import sqlite3
from datetime import date


def conectar(arquivo="cineflix.db"):
    conn = sqlite3.connect(arquivo)
    conn.execute("PRAGMA foreign_keys = ON")   # o banco passa a conferir a chave estrangeira
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS titulos (
            id            INTEGER PRIMARY KEY,
            titulo        TEXT NOT NULL,
            tipo          TEXT NOT NULL,
            genero        TEXT NOT NULL,
            ano           INTEGER NOT NULL,
            duracao_min   INTEGER NOT NULL,
            classificacao INTEGER NOT NULL,
            nota          REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS visualizacoes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            perfil    TEXT NOT NULL,
            titulo_id INTEGER NOT NULL REFERENCES titulos(id),
            minutos   INTEGER NOT NULL,
            data      TEXT NOT NULL
        );
    """)
    conn.commit()
    return conn


def importar_catalogo(conn, caminho="catalogo.json"):
    """Importa o JSON só se a tabela titulos estiver vazia. Devolve quantos importou."""
    if conn.execute("SELECT COUNT(*) FROM titulos").fetchone()[0] > 0:
        return 0
    with open(caminho, "r", encoding="utf-8") as f:
        catalogo = json.load(f)
    for t in catalogo:
        conn.execute(
            "INSERT INTO titulos (id, titulo, tipo, genero, ano, duracao_min, "
            "classificacao, nota) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (t["id"], t["titulo"], t["tipo"], t["genero"], t["ano"],
             t["duracao_min"], t["classificacao"], t["nota"]))
    conn.commit()
    return len(catalogo)


def listar_titulos(conn):
    return conn.execute(
        "SELECT id, titulo, tipo, genero, ano, classificacao, nota "
        "FROM titulos ORDER BY id").fetchall()


def registrar(conn, perfil, titulo_id, minutos, data=None):
    """Registra uma sessão. Devolve False se o título não existe."""
    if data is None:
        data = date.today().isoformat()
    try:
        conn.execute(
            "INSERT INTO visualizacoes (perfil, titulo_id, minutos, data) "
            "VALUES (?, ?, ?, ?)", (perfil, titulo_id, minutos, data))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def historico(conn, perfil):
    """(data, título, minutos), do mais recente para o mais antigo."""
    return conn.execute(
        "SELECT visualizacoes.data, titulos.titulo, visualizacoes.minutos "
        "FROM visualizacoes JOIN titulos ON titulos.id = visualizacoes.titulo_id "
        "WHERE visualizacoes.perfil = ? "
        "ORDER BY visualizacoes.data DESC, visualizacoes.id DESC", (perfil,)).fetchall()


def mais_assistidos(conn, limite=5):
    """(título, vezes) de todos os perfis."""
    return conn.execute(
        "SELECT titulos.titulo, COUNT(*) AS vezes "
        "FROM visualizacoes JOIN titulos ON titulos.id = visualizacoes.titulo_id "
        "GROUP BY titulos.id ORDER BY vezes DESC, titulos.titulo LIMIT ?",
        (limite,)).fetchall()


def tempo_por_perfil(conn):
    """(perfil, minutos totais), do que mais assistiu para o que menos."""
    return conn.execute(
        "SELECT perfil, SUM(minutos) AS total FROM visualizacoes "
        "GROUP BY perfil ORDER BY total DESC, perfil").fetchall()
