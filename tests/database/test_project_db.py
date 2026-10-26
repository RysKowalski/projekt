import os
from database import Database, Project
from declarations import Bitmap


TEST_DB_PATH: str = "test_db.sqlite"
TEST_USERNAME: str = "username"
TEST_PROJECT_NAME: str = "project"
TEST_PASSWORD_HASH: str = "q1234#$"
TEST_BITMAPS: Bitmap = {
    "a": [
        [False, False, False],
        [True, True, True],
        [False, False, False],
    ],
    "b": [[True, True], [False, False], [True, True]],
}


class TestDatabase(Database):
    def __init__(self, db_path: str = TEST_DB_PATH) -> None:
        self.__del__()
        super().__init__(db_path)

    def __del__(self) -> None:
        try:
            os.remove(TEST_DB_PATH)
        except Exception:
            pass


def test_get_nonexistent() -> None:
    db: Database = TestDatabase()

    project: Project | None = db.get_project(-1)

    assert project is None


def test_add_get_project() -> None:
    db: Database = TestDatabase()
    user_id: int = db.add_user(TEST_USERNAME, TEST_PASSWORD_HASH)

    project_id: int = db.add_project(user_id, TEST_PROJECT_NAME)
    project: Project | None = db.get_project(project_id)

    assert project is not None
    assert project.name == TEST_PROJECT_NAME
    assert project.id == project_id
    assert project.creation_date == project.edit_date


def test_delete_project() -> None:
    db: Database = TestDatabase()
    user_id: int = db.add_user(TEST_USERNAME, TEST_PASSWORD_HASH)
    project_id: int = db.add_project(user_id, TEST_PROJECT_NAME)

    db.delete_project(project_id)

    assert db.get_project(project_id) is None


def test_get_project_list() -> None:
    db: Database = TestDatabase()
    user_id: int = db.add_user(TEST_USERNAME, TEST_PASSWORD_HASH)
    projects: set[tuple[int, str]] = set()
    for i in range(10):
        project_name: str = TEST_PROJECT_NAME + str(i)
        project_id: int = db.add_project(user_id, project_name)
        projects.add((project_id, project_name))

    result = db.get_project_list(user_id)

    for r in result:
        assert r in projects


def test_add_get_bitmap() -> None:
    db: Database = TestDatabase()
    user_id: int = db.add_user(TEST_USERNAME, TEST_PASSWORD_HASH)
    project_id: int = db.add_project(user_id, TEST_PROJECT_NAME)

    db.add_bitmap(project_id, TEST_BITMAPS)
    result: Bitmap = db.get_bitmap(project_id)

    assert result == TEST_BITMAPS
