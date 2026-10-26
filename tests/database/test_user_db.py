import os
from database import UserDB, UserInDb


TEST_DB_PATH: str = "test_db.sqlite"


class TestUserDB(UserDB):
    def __init__(self, db_path: str = TEST_DB_PATH) -> None:
        self.__del__()
        super().__init__(db_path)

    def __del__(self) -> None:
        try:
            os.remove(TEST_DB_PATH)
        except Exception:
            pass


TEST_USERNAME: str = "username"
TEST_PASSWORD_HASH: str = "q1234#$"


def test_get_nonexistent_user() -> None:
    db: UserDB = TestUserDB()

    user: UserInDb | None = db.get_user(TEST_USERNAME)

    assert user is None


def test_add_get_user() -> None:
    db: UserDB = TestUserDB()

    db.add_user(TEST_USERNAME, TEST_PASSWORD_HASH)
    result: UserInDb | None = db.get_user(TEST_USERNAME)

    assert result is not None
    assert result.username == TEST_USERNAME
    assert result.password_hash == TEST_PASSWORD_HASH


def test_add_user_returns_correct_id() -> None:
    db: UserDB = TestUserDB()
    id: int = db.add_user(TEST_USERNAME, TEST_PASSWORD_HASH)

    user: UserInDb | None = db.get_user(TEST_USERNAME)

    if user is None:
        raise
    assert id == user.id


def test_delete_user() -> None:
    db: UserDB = TestUserDB()
    user_id: int = db.add_user(TEST_USERNAME, TEST_PASSWORD_HASH)

    db.delete_user(user_id)

    assert db.get_user(TEST_USERNAME) is None
