from dataclasses import dataclass
from datetime import datetime
from sqlite3 import Cursor

from .base import DatabaseBase


@dataclass(frozen=True)
class User:
    id: int
    username: str
    created: datetime


@dataclass(frozen=True)
class UserInDb(User):
    password_hash: str


class UserDB(DatabaseBase):
    def get_user(self, username: str) -> UserInDb | None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, created, password_hash FROM users WHERE name=?;
            """,
                (username,),
            )

            result = cursor.fetchone()
        if result is None:
            return

        id, created, password_hash = result

        return UserInDb(id, username, self._from_sqlite_date(created), password_hash)

    def add_user(self, username: str, password_hash: str) -> int:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (password_hash, name) VALUES (?, ?)
                """,
                (password_hash, username),
            )
            id: int | None = cursor.lastrowid
            conn.commit()
        if not id:
            return -1
        return id

    def delete_user(self, user_id: int) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM users WHERE id=?
                """,
                (user_id,),
            )

            conn.commit()
