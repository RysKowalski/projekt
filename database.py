from contextlib import contextmanager
from dataclasses import dataclass
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Generator
from declarations import Bitmap, Char


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

    def add_user(self, username: str, password_hash: str) -> int:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (password_hash, username) VALUES (?, ?)
                """,
                (password_hash, username),
            )
            id: int | None = cursor.lastrowid
            conn.commit()
        if not id:
            return -1
        return id

    def add_project(self, user_id: str, name: int) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO projects (name, user_id) VALUES (?, ?)
            """,
                (name, user_id),
            )

    def add_bitmap(self, project_id: int, bitmap: Bitmap) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            for name, char in bitmap.items():
                size_x, size_y, data = self._encode_char(char)
                cursor.execute(
                    """
                    INSERT INTO characters (project_id, name, sizex, sizey, data)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (project_id, name, size_x, size_y, data),
                )
            conn.commit()

    def _encode_char(self, grid: Char) -> tuple[int, int, bytes]:
        size_y: int = len(grid)
        size_x: int = len(grid[0])

        data: bytearray = bytearray((size_x * size_y + 7) // 8)

        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value:
                    index: int = y * size_x + x
                    data[index // 8] |= 1 << (index % 8)

        return size_x, size_y, bytes(data)

    def get_char(self, char_id: int) -> Char:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT sizex, sizey, data FROM characters WHERE id=?
            """,
                (char_id,),
            )
            result = cursor.fetchone()

        if not result:
            return []

        size_x: int
        size_y: int
        data: bytes
        size_x, size_y, data = result

        return self._decode_char(size_x, size_y, data)

    def _decode_char(self, size_x: int, size_y: int, data: bytes) -> Char:
        grid: list[list[bool]] = []
        i: int = 0

        for _ in range(size_y):
            row: list[bool] = []
            for _ in range(size_x):
                byte_index: int = i // 8
                bit_position: int = i % 8
                mask: int = 1 << bit_position
                bit: bool = bool(data[byte_index] & mask)

                row.append(bit)
            grid.append(row)

        return grid
