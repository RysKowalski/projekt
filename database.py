from contextlib import contextmanager
from dataclasses import dataclass
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Generator
from declarations import Bitmap


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
        self.create_tables()

    @contextmanager
    def _connect(self) -> Generator[Connection]:
        conn: Connection = sqlite3.connect(self.dbPath)
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def create_tables(self) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password_hash TEXT NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    creation_date DATE NOT NULL DEFAULT CURRENT_TIME
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    edit_date DATE NOT NULL DEFAULT CURRENT_TIME,
                    create_date DATE NOT NULL DEFAULT CURRENT_TIME,
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
                INSERT INTO users (password_hash, username) VALUES (?, ?)
                """,
                (password_hash, username),
            )
            conn.commit()

    def add_project(self, name: int, user_id: str) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO projects (name, user_id) VALUES (?, ?)
            """,
                (name, user_id),
            )

    def add_bitmap(self, bitmap: Bitmap) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            for name, char in bitmap.items():
                char

    def _encode_grid(self, grid: list[list[bool]]) -> tuple[int, int, bytes]:
        size_y: int = len(grid)
        size_x: int = 

