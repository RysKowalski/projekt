import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime, timezone
from sqlite3 import Connection, Cursor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from encryption import Encryption


class DatabaseBase:
    def __init__(
        self, encryption: "Encryption", db_path: str = "database.sqlite"
    ) -> None:
        self.enc: "Encryption" = encryption
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
                    created DATETIME NOT NULL DEFAULT (
                        strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                    )
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name BLOB NOT NULL,
                    user_id INTEGER NOT NULL,
                    edited DATETIME NOT NULL DEFAULT (
                        strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                    ),
                    created DATETIME NOT NULL DEFAULT (
                        strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                    ),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER NOT NULL,
                    name CHAR(1) NOT NULL,
                    bitmap BLOB NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
                );
            """)

            conn.commit()

    @staticmethod
    def _to_sqlite_date(value: datetime) -> str:
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def _from_sqlite_date(value: str) -> datetime:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
