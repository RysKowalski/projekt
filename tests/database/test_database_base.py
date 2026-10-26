import os

from database import DatabaseBase


def test_creates_db() -> None:
    TEST_DB_PATH: str = "test_db.sqlite"
    db = DatabaseBase(TEST_DB_PATH)

    assert os.path.exists(TEST_DB_PATH)
    os.remove(TEST_DB_PATH)
