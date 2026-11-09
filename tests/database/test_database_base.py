import os
from datetime import datetime, timezone, timedelta

from database import DatabaseBase
from encryption import Encryption


class DBTest(DatabaseBase):
    e = Encryption()

    def __init__(self, db_path: str) -> None:
        super().__init__(self.e, db_path)


def test_creates_db() -> None:
    TEST_DB_PATH: str = "test_db.sqlite"
    _ = DBTest(TEST_DB_PATH)

    assert os.path.exists(TEST_DB_PATH)
    os.remove(TEST_DB_PATH)


def test_to_sqlite_date() -> None:
    value: datetime = datetime(2024, 5, 15, 12, 30, 45, tzinfo=timezone.utc)

    result: str = DatabaseBase._to_sqlite_date(value)

    assert result == "2024-05-15T12:30:45+00:00".replace("+00:00", "Z")


def test_to_sqlite_date_converts_to_utc() -> None:
    value: datetime = datetime(
        2024,
        5,
        15,
        14,
        30,
        45,
        tzinfo=timezone(timedelta(hours=2)),
    )

    result: str = DatabaseBase._to_sqlite_date(value)

    assert result == "2024-05-15T12:30:45Z"


def test_from_sqlite_date() -> None:
    value: str = "2024-05-15T12:30:45Z"

    result: datetime = DatabaseBase._from_sqlite_date(value)

    assert result == datetime(2024, 5, 15, 12, 30, 45, tzinfo=timezone.utc)


def test_from_sqlite_date_with_offset() -> None:
    value: str = "2024-05-15T14:30:45+02:00"

    result: datetime = DatabaseBase._from_sqlite_date(value)

    assert result == datetime(
        2024,
        5,
        15,
        14,
        30,
        45,
        tzinfo=timezone(timedelta(hours=2)),
    )
