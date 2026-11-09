import struct
from dataclasses import dataclass
from datetime import datetime
from sqlite3 import Cursor

from declarations import Bitmaps, Bitmap
from .base import DatabaseBase


@dataclass(frozen=True)
class Project:
    id: int
    name: str
    edited: datetime
    created: datetime


class ProjectDB(DatabaseBase):
    def add_project(self, user_id: int, name: str) -> int:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO projects (name, user_id) VALUES (?, ?)
            """,
                (self.enc.encrypt(name), user_id),
            )

            id: int | None = cursor.lastrowid
            conn.commit()

        if id is None:
            return -1
        return id

    def delete_project(self, project_id: int) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute("DELETE FROM projects WHERE id=?", (project_id,))

            conn.commit()

    def get_project_list(self, user_id: int) -> list[tuple[int, str]]:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, name FROM projects
                WHERE user_id=?
            """,
                (user_id,),
            )

            data: list[tuple[int, bytes]] = cursor.fetchall().copy()
        decrypted: list[tuple[int, str]] = []
        for id, name in data:
            decrypted.append((id, self.enc.decrypt_str(name)))

        return decrypted

    def get_project(self, project_id: int) -> Project | None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT name, edited, created
                FROM projects
                WHERE id=?
            """,
                (project_id,),
            )

            data = cursor.fetchone()
        if data is None:
            return

        name, edited, created = data

        return Project(
            project_id,
            self.enc.decrypt_str(name),
            self._from_sqlite_date(edited),
            self._from_sqlite_date(created),
        )

    def set_bitmap(self, project_id: int, bitmap: Bitmaps) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            for name, char in bitmap.items():
                data = self._encode_char(char)
                encrypted_data = self.enc.encrypt(data)
                cursor.execute(
                    """
                    INSERT INTO characters (project_id, name, bitmap)
                    VALUES (?, ?, ?)
                """,
                    (project_id, name, encrypted_data),
                )
            conn.commit()

    def get_bitmap(self, project_id: int) -> Bitmaps:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT name, bitmap
                FROM characters
                WHERE project_id=?
            """,
                (project_id,),
            )

            bitmap: Bitmaps = {}
            for name, data in cursor:
                bitmap[name] = self._decode_char(self.enc.decrypt(data))
        return bitmap

    def get_char(self, char_id: int) -> Bitmap:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT bitmap FROM characters WHERE id=?
                """,
                (char_id,),
            )
            result = cursor.fetchone()

        if not result:
            return []

        data: bytes = result[0]

        return self._decode_char(self.enc.decrypt(data))

    @staticmethod
    def _encode_char(bitmap: Bitmap) -> bytes:
        """Encode an RLE bitmap into binary data."""
        data = bytearray()

        data.extend(struct.pack("<I", len(bitmap)))

        for row in bitmap:
            data.extend(struct.pack("<I", len(row)))

            for value, count in row:
                data.extend(struct.pack("<BI", value, count))

        return bytes(data)

    @staticmethod
    def _decode_char(data: bytes) -> Bitmap:
        """Decode binary RLE data into a bitmap."""
        offset: int = 0

        def read(fmt: str) -> tuple:
            nonlocal offset

            size: int = struct.calcsize(fmt)

            if offset + size > len(data):
                raise ValueError("Invalid bitmap data")

            result: tuple = struct.unpack_from(fmt, data, offset)
            offset += size

            return result

        rows: int = read("<I")[0]
        bitmap: Bitmap = []

        for _ in range(rows):
            runs: int = read("<I")[0]
            row: list[tuple[bool, int]] = []

            for _ in range(runs):
                value, count = read("<BI")
                row.append((bool(value), count))

            bitmap.append(row)

        if offset != len(data):
            raise ValueError("Unexpected trailing bitmap data")

        return bitmap
