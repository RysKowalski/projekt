import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from sqlite3 import Connection, Cursor


class DatabaseBase:
    def __init__(self, db_path: str = "database.sqlite") -> None:
        self.db_path: str = db_path
        self.create_tables()

    @contextmanager
    def _connect(self) -> Generator[Connection]:
        conn: Connection = sqlite3.connect(self.db_path)
        try:
            conn.execute("PRAGMA foreign_keys = ON")
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
                    name TEXT UNIQUE NOT NULL,
                    created DATE NOT NULL DEFAULT CURRENT_TIME
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    edited DATE NOT NULL DEFAULT CURRENT_TIME,
                    created DATE NOT NULL DEFAULT CURRENT_TIME,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    name CHAR(1) NOT NULL,
                    sizex INTEGER NOT NULL,
                    sizey INTEGER NOT NULL,
                    bitmap BLOB NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
                );
            """)

            conn.commit()
