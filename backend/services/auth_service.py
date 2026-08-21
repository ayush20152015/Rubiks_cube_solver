import os
import sqlite3
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from config import settings


class AuthService:
    def __init__(self) -> None:
        os.makedirs(os.path.dirname(settings.USER_DATABASE_PATH), exist_ok=True)
        with self._connection() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password_hash BLOB NOT NULL,
                    created_at TEXT NOT NULL
                )"""
            )

    def _connection(self) -> sqlite3.Connection:
        return sqlite3.connect(settings.USER_DATABASE_PATH)

    def register(self, email: str, password: str) -> None:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            with self._connection() as connection:
                connection.execute(
                    "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                    (email.lower(), password_hash, datetime.now(timezone.utc).isoformat()),
                )
        except sqlite3.IntegrityError as error:
            raise ValueError("An account with this email already exists") from error

    def authenticate(self, email: str, password: str) -> str | None:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT id, email, password_hash FROM users WHERE email = ?", (email.lower(),)
            ).fetchone()

        if row is None or not bcrypt.checkpw(password.encode(), row[2]):
            return None

        expiry = datetime.now(timezone.utc) + timedelta(minutes=settings.AUTH_JWT_EXPIRES_MINUTES)
        return jwt.encode({"sub": str(row[0]), "email": row[1], "exp": expiry}, settings.AUTH_JWT_SECRET, algorithm="HS256")

    def user_from_token(self, token: str) -> dict[str, str]:
        return jwt.decode(token, settings.AUTH_JWT_SECRET, algorithms=["HS256"])