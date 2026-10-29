from dataclasses import dataclass
from sqlite3 import Cursor

from .base import DatabaseBase


@dataclass(frozen=True)
class User:
    id: int
    username: str
    creation_date: str


@dataclass(frozen=True)
class UserInDb(User):
    password_hash: str


class UserDB(DatabaseBase):
    def get_user(self, username: str) -> UserInDb | None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, name, created, password_hash FROM users WHERE name=?;
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
