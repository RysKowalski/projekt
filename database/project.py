from dataclasses import dataclass
from sqlite3 import Cursor

from declarations import Bitmaps, Bitmap
from .base import DatabaseBase


@dataclass(frozen=True)
class Project:
    id: int
    name: str
    edit_date: str
    creation_date: str


class ProjectDB(DatabaseBase):
    def add_project(self, user_id: int, name: str) -> int:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO projects (name, user_id) VALUES (?, ?)
            """,
                (name, user_id),
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

            data = cursor.fetchall()
        return data.copy()

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

        return Project(project_id, data[0], data[1], data[2])

    def set_bitmap(self, project_id: int, bitmap: Bitmaps) -> None:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            for name, char in bitmap.items():
                size_x, size_y, data = self._encode_char(char)
                cursor.execute(
                    """
                    INSERT INTO characters (project_id, name, sizex, sizey, bitmap)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (project_id, name, size_x, size_y, data),
                )
            conn.commit()

    def _encode_char(self, grid: Bitmap) -> tuple[int, int, bytes]:
        size_y: int = len(grid)
        size_x: int = len(grid[0])

        data: bytearray = bytearray((size_x * size_y + 7) // 8)

        for y, row in enumerate(grid):
            for x, value in enumerate(row):
                if value:
                    index: int = y * size_x + x
                    data[index // 8] |= 1 << (index % 8)

        return size_x, size_y, bytes(data)

    def get_bitmap(self, project_id: int) -> Bitmaps:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT name, sizex, sizey, bitmap
                FROM characters
                WHERE project_id=?
            """,
                (project_id,),
            )

            bitmap: Bitmaps = {}
            for row in cursor:
                bitmap[row[0]] = self._decode_char(row[1], row[2], row[3])
        return bitmap

    def get_char(self, char_id: int) -> Bitmap:
        with self._connect() as conn:
            cursor: Cursor = conn.cursor()

            cursor.execute(
                """
                SELECT sizex, sizey, bitmap FROM characters WHERE id=?
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

    def _decode_char(self, size_x: int, size_y: int, data: bytes) -> Bitmap:
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
                i += 1
            grid.append(row)

        return grid
