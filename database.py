import sqlite3
import secrets
import string
from datetime import datetime

DB_FILE = "nexus_mc.db"

def conn():
    c = sqlite3.connect(DB_FILE)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with conn() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            access_code TEXT,
            joined_at TEXT NOT NULL
        )""")
        db.execute("""CREATE TABLE IF NOT EXISTS access_codes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            created_at TEXT NOT NULL,
            revoked INTEGER DEFAULT 0
        )""")
        db.commit()

def make_code():
    alphabet = string.ascii_uppercase + string.digits
    return "NEXUS-" + "".join(secrets.choice(alphabet) for _ in range(8))

def generate_code():
    code = make_code()
    with conn() as db:
        db.execute("INSERT INTO access_codes(code, created_at) VALUES(?,?)",
                   (code, datetime.utcnow().isoformat()))
        db.commit()
    return code

def register_user(username, access_code):
    with conn() as db:
        db.execute("INSERT INTO users(username, access_code, joined_at) VALUES(?,?,?)",
                   (username, access_code, datetime.utcnow().isoformat()))
        db.commit()

def get_stats():
    with conn() as db:
        users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        codes = db.execute("SELECT COUNT(*) FROM access_codes").fetchone()[0]
        active = db.execute("SELECT COUNT(*) FROM access_codes WHERE revoked=0").fetchone()[0]
    return {"users":users, "codes":codes, "active_codes":active}

def get_users():
    with conn() as db:
        rows = db.execute("SELECT id, username, access_code, joined_at FROM users ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]

def get_codes():
    with conn() as db:
        rows = db.execute("SELECT id, code, created_at, revoked FROM access_codes ORDER BY id DESC").fetchall()
    return [dict(r) for r in rows]

def revoke_code(code):
    with conn() as db:
        db.execute("UPDATE access_codes SET revoked=1 WHERE code=?", (code,))
        db.commit()
