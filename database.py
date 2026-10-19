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

            conn.commit()
