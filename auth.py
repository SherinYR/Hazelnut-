"""
Authentication and user management (SQLite).

Provides:
- User dataclass
- Password hashing and validation
- CRUD operations for users
- Authentication and password reset
"""

from __future__ import annotations

import hashlib
import os
import re
import secrets
import sqlite3
from dataclasses import dataclass
from typing import List, Optional, Tuple


DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(__file__) if "__file__" in globals() else os.getcwd(),
    "users.db",
)


@dataclass(frozen=True)
class User:
    """Represents an authenticated application user."""
    id: int
    username: str
    is_admin: bool


def _connect(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Open a SQLite connection with Row factory enabled."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def _hash_password(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    """Hash a password using PBKDF2-HMAC-SHA256 with a provided salt."""
    if not isinstance(password, str) or password == "":
        raise ValueError("Password must be a non-empty string.")
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def validate_password_rules(password: str) -> Tuple[bool, str]:
    """
    Validate password complexity rules.

    Rules:
    - at least 8 characters
    - at least 1 lowercase, 1 uppercase, 1 digit, 1 special char
    """
    if not isinstance(password, str):
        return False, "Password must be text."
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[^\w\s]", password):
        return False, "Password must contain at least one special character (e.g., !@#$%)."
    return True, "OK"


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Initialize the SQLite user database and seed demo accounts (idempotent)."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    with _connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                salt BLOB NOT NULL,
                pw_hash BLOB NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()

    seed_users = [
        ("admin", "Admin123!", True),
        ("student1", "Student123!", False),
        ("student2", "Student123!", False),
        ("guest", "Guest123!", False),
    ]
    for username, password, is_admin in seed_users:
        if get_user_by_username(username, db_path=db_path) is None:
            create_user(username, password, is_admin=is_admin, db_path=db_path, enforce_rules=False)


def create_user(
    username: str,
    password: str,
    is_admin: bool = False,
    db_path: str = DEFAULT_DB_PATH,
    enforce_rules: bool = True,
) -> None:
    """Create a new user record with a salted password hash."""
    username = (username or "").strip()
    if not username:
        raise ValueError("Username cannot be empty.")
    if enforce_rules:
        ok, msg = validate_password_rules(password)
        if not ok:
            raise ValueError(msg)

    salt = secrets.token_bytes(16)
    pw_hash = _hash_password(password, salt)
    with _connect(db_path) as conn:
        conn.execute(
            "INSERT INTO users (username, salt, pw_hash, is_admin, created_at) VALUES (?, ?, ?, ?, datetime('now'))",
            (username, salt, pw_hash, 1 if is_admin else 0),
        )
        conn.commit()


def delete_user(username: str, db_path: str = DEFAULT_DB_PATH) -> bool:
    """Delete a user by username. Returns True if a row was deleted."""
    username = (username or "").strip()
    if not username:
        return False
    with _connect(db_path) as conn:
        cur = conn.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        return cur.rowcount > 0


def list_users(db_path: str = DEFAULT_DB_PATH) -> List[Tuple[str, bool]]:
    """Return a list of (username, is_admin) sorted with admins first."""
    with _connect(db_path) as conn:
        rows = conn.execute("SELECT username, is_admin FROM users ORDER BY is_admin DESC, username ASC").fetchall()
        return [(r["username"], bool(r["is_admin"])) for r in rows]


def get_user_by_username(username: str, db_path: str = DEFAULT_DB_PATH) -> Optional[User]:
    """Fetch a user by username, returning a User object or None."""
    username = (username or "").strip()
    if not username:
        return None
    with _connect(db_path) as conn:
        row = conn.execute("SELECT id, username, is_admin FROM users WHERE username = ?", (username,)).fetchone()
        if row is None:
            return None
        return User(id=int(row["id"]), username=row["username"], is_admin=bool(row["is_admin"]))


def authenticate(username: str, password: str, db_path: str = DEFAULT_DB_PATH) -> Optional[User]:
    """Authenticate a user and return a User on success, otherwise None."""
    username = (username or "").strip()
    if not username:
        return None
    with _connect(db_path) as conn:
        row = conn.execute(
            "SELECT id, username, salt, pw_hash, is_admin FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if row is None:
            return None
        salt = row["salt"]
        expected = row["pw_hash"]
        try:
            candidate = _hash_password(password, salt)
        except ValueError:
            return None
        if secrets.compare_digest(candidate, expected):
            return User(id=int(row["id"]), username=row["username"], is_admin=bool(row["is_admin"]))
        return None


def set_password(username: str, new_password: str, db_path: str = DEFAULT_DB_PATH) -> bool:
    """Set a new password for an existing user. Returns True if updated."""
    username = (username or "").strip()
    if not username:
        return False
    ok, msg = validate_password_rules(new_password)
    if not ok:
        raise ValueError(msg)

    salt = secrets.token_bytes(16)
    pw_hash = _hash_password(new_password, salt)
    with _connect(db_path) as conn:
        cur = conn.execute(
            "UPDATE users SET salt = ?, pw_hash = ? WHERE username = ?",
            (salt, pw_hash, username),
        )
        conn.commit()
        return cur.rowcount > 0
