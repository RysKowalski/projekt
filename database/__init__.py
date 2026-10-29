from .base import DatabaseBase
from .project import Project, ProjectDB
from .user import User, UserInDb, UserDB


class Database(ProjectDB, UserDB): ...
