import sqlite3
import secrets
import string
from datetime import datetime, timezone

DB = "nexus.db"

def connect():
    c = sqlite3.connect(DB)
    c.execute("PRAGMA foreign_keys=ON")
    return c

def init_db():
    with connect() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            access_code TEXT,
            joined_at TEXT NOT NULL
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS access_codes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            active INTEGER DEFAULT 1,
            used INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )""")
        if c.execute("SELECT COUNT(*) FROM access_codes").fetchone()[0] == 0:
            c.execute("INSERT INTO access_codes(code,created_at) VALUES(?,?)",
                      ("NEXUS2026", datetime.now(timezone.utc).isoformat()))

def verify_access_code(code):
    with connect() as c:
        row = c.execute("SELECT id,active,used FROM access_codes WHERE code=?",(code,)).fetchone()
        if not row:
            return False, "Invalid access code."
        if not row[1]:
            return False, "This access code has been revoked."
        if row[2]:
            return False, "This access code has already been used."
        c.execute("UPDATE access_codes SET used=1 WHERE id=?",(row[0],))
        return True, "Verified"

def register_user(username, code):
    try:
        with connect() as c:
            c.execute("INSERT INTO users(username,access_code,joined_at) VALUES(?,?,?)",
                      (username,code,datetime.now(timezone.utc).isoformat()))
        return True
    except sqlite3.IntegrityError:
        return False

def get_stats():
    with connect() as c:
        users=c.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active=c.execute("SELECT COUNT(*) FROM access_codes WHERE active=1 AND used=0").fetchone()[0]
        used=c.execute("SELECT COUNT(*) FROM access_codes WHERE used=1").fetchone()[0]
    return {"users":users,"active_codes":active,"used_codes":used}

def get_users():
    with connect() as c:
        return c.execute("SELECT id,username,access_code,joined_at FROM users ORDER BY id DESC").fetchall()

def delete_user(user_id):
    with connect() as c:
        c.execute("DELETE FROM users WHERE id=?",(user_id,))

def generate_code():
    alphabet=string.ascii_uppercase+string.digits
    code="NEXUS-"+''.join(secrets.choice(alphabet) for _ in range(8))
    with connect() as c:
        c.execute("INSERT INTO access_codes(code,created_at) VALUES(?,?)",
                  (code,datetime.now(timezone.utc).isoformat()))
    return code

def revoke_code(code_id):
    with connect() as c:
        c.execute("UPDATE access_codes SET active=0 WHERE id=?",(code_id,))

def get_codes():
    with connect() as c:
        return c.execute("SELECT id,code,active,used,created_at FROM access_codes ORDER BY id DESC").fetchall()
