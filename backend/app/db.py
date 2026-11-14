import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "mostashar.db"

def _conn():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL, content TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
    return c

def add(role, content):
    with _conn() as c:
        c.execute("INSERT INTO messages(role, content) VALUES (?,?)", (role, content))

def recent(limit=12):
    with _conn() as c:
        rows = c.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [{"role": r, "content": t} for r, t in reversed(rows)]

def clear():
    with _conn() as c:
        c.execute("DELETE FROM messages")
