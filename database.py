from contextlib import contextmanager
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Iterator


class Database:
    def __init__(self) -> None:
        self.dbPath: str = "database.sqlite"

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
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    password_hash TEXT NOT NULL,
                    username TEXT NOT NULL,
                    creation_date DATE NOT NULL
                );
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    name TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    edit_date DATE NOT NULL,
                    create_date DATE NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    project_id INTEGER NOT NULL,
                    name CHAR(1) NOT NULL,
                    sizex INTEGER NOT NULL,
                    sizey INTEGER NOT NULL,
                    data BLOB NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                );
            """)

            conn.commit()
