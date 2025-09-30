# db.py
import sqlite3
from typing import List, Tuple, Optional

DB_PATH = "news.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    # Общая таблица индекса новостей
    cur.execute("""
    CREATE TABLE IF NOT EXISTS news_index (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT,
        link TEXT
    )
    """)
    conn.commit()
    conn.close()

def clear_index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM news_index")
    conn.commit()
    conn.close()

def add_news_index(title: str, date: str, link: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO news_index (title, date, link) VALUES (?, ?, ?)", (title, date, link))
    nid = cur.lastrowid
    conn.commit()
    conn.close()
    return nid

def list_news() -> List[Tuple[int, str, str, str]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, date, link FROM news_index ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_news_meta(news_id: int) -> Optional[Tuple[int, str, str, str]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, date, link FROM news_index WHERE id = ?", (news_id,))
    row = cur.fetchone()
    conn.close()
    return row

def create_news_table(news_id: int):
    conn = get_conn()
    cur = conn.cursor()
    table_name = f"news_{news_id}"
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS "{table_name}" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        saved_at TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_article_text(news_id: int, content: str, saved_at: str):
    conn = get_conn()
    cur = conn.cursor()
    table_name = f"news_{news_id}"
    cur.execute(f"INSERT INTO \"{table_name}\" (content, saved_at) VALUES (?, ?)", (content, saved_at))
    conn.commit()
    conn.close()

def get_latest_article_text(news_id: int) -> Optional[str]:
    conn = get_conn()
    cur = conn.cursor()
    table_name = f"news_{news_id}"
    try:
        cur.execute(f"SELECT content FROM \"{table_name}\" ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
    except sqlite3.OperationalError:
        row = None
    conn.close()
    return row[0] if row else None
