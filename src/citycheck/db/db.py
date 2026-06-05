from collections.abc import Generator
from pathlib import Path
from typing import override

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base


class SqliteDB:
    def __init__(self, file: Path, create_metadata: bool = True) -> None:
        self.file: Path = file
        self.engine: Engine = create_engine(f"sqlite:///{self.file}")

        self._base: type[Base] = Base
        self._session_factoy: sessionmaker[Session] = sessionmaker(self.engine)

        self.Session: Generator[Session] = self._create_session_generator()

        if create_metadata:
            self._create_metadata()

    @override
    def __str__(self) -> str:
        return "SqliteDB"

    def get_session(self) -> Session:
        return next(self.Session)

    def _create_session_generator(self) -> Generator[Session]:
        session = self._session_factoy()
        try:
            yield session
        finally:
            session.close()

    def _create_metadata(self) -> None:
        self._base.metadata.create_all(self.engine)

    def drop_all_tables(self, create: bool = True) -> None:
        self._base.metadata.drop_all(self.engine)
        if create:
            self._create_metadata()
        return None


DB_FILE = Path("citycheck.db")


def init_db(db_file: Path = DB_FILE) -> SqliteDB:
    return SqliteDB(db_file)


DB = init_db()
