import sqlite3
from datetime import datetime

DB_FILE = "nexus_mc.db"


def get_connection():
    connection = sqlite3.connect(DB_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the users table if it doesn't already exist."""
    with get_connection() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                access_code TEXT NOT NULL,
                joined_at TEXT NOT NULL
            )
        """)
        db.commit()


def register_user(username, access_code="mtfverse"):
    """Register a player."""
    username = username.strip()

    if not username:
        return False

    with get_connection() as db:
        # Don't create duplicate entries for the same username.
        existing = db.execute(
            "SELECT id FROM users WHERE LOWER(username) = LOWER(?)",
            (username,)
        ).fetchone()

        if existing:
            return False

        db.execute(
            """
            INSERT INTO users (username, access_code, joined_at)
            VALUES (?, ?, ?)
            """,
            (
                username,
                access_code,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )

        db.commit()

    return True


def get_stats():
    """Return basic portal statistics."""
    with get_connection() as db:
        total_users = db.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

    return {
        "users": total_users,
        "codes": 1,
        "active_codes": 1
    }


def get_users():
    """Return all registered players."""
    with get_connection() as db:
        rows = db.execute("""
            SELECT
                id,
                username,
                access_code,
                joined_at
            FROM users
            ORDER BY id DESC
        """).fetchall()

    return [dict(row) for row in rows]


def delete_user(user_id):
    """Delete a player by database ID."""
    with get_connection() as db:
        db.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
        db.commit()


def delete_user_by_username(username):
    """Delete a player by username."""
    with get_connection() as db:
        db.execute(
            "DELETE FROM users WHERE LOWER(username) = LOWER(?)",
            (username.strip(),)
        )
        db.commit()


def user_exists(username):
    """Check whether a username is already registered."""
    with get_connection() as db:
        row = db.execute(
            "SELECT id FROM users WHERE LOWER(username) = LOWER(?)",
            (username.strip(),)
        ).fetchone()

    return row is not None
