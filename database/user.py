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
class UserInDb:
    id: int
    created: datetime
    password_hash: str


class UserDB(DatabaseBase):
    def get_user(self, username: str) -> UserInDb | None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, created, password_hash FROM users WHERE username_hash=?;
            """,
                (self.enc.hash_username(username),),
            )

            result = cursor.fetchone()
        if result is None:
            return

        id, created, password_hash = result

        return UserInDb(id, self._from_sqlite_date(created), password_hash)

    def add_user(self, username: str, password_hash: str) -> int:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (password_hash, username_hash) VALUES (?, ?)
                """,
                (password_hash, self.enc.hash_username(username)),
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
