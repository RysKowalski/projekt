from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Iterator


class InvalidUserError(Exception):
    def __init__(self, username: str) -> None:
        self.message = f"user {username} does not exist or has incorrect password"
        super().__init__(self.message)


@dataclass(frozen=True)
class User:
    id: int
    username: str
    creation_date: str


@dataclass(frozen=True)
class UserInDb(User):
    password_hash: str


class Database:
    def __init__(self) -> None:
        self.dbPath: str = "database.sqlite"
        self.init_db()

    @contextmanager
    def _connect(self) -> Iterator[Connection]:
        conn: Connection = sqlite3.connect(self.dbPath)
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_db(self) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password_hash TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    creation_date DATE NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    edit_date DATE NOT NULL,
                    create_date DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    name CHAR(1) NOT NULL,
                    sizex INTEGER NOT NULL,
                    sizey INTEGER NOT NULL,
                    data BLOB NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                );
            """)

            conn.commit()

    def get_user(self, username: str) -> UserInDb | None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, username, creation_date, password_hash FROM users WHERE username=?;
            """,
                (username,),
            )

            result = cursor.fetchone()
        if result is None:
            return

        return UserInDb(result[0], result[1], result[2], result[3])

    def add_user(self, username: str, password_hash: str) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (password_hash, username, creation_date) VALUES (?, ?, ?)
                """,
                (password_hash, username, datetime.now().strftime("%Y-%m-%d")),
            )
            conn.commit()
