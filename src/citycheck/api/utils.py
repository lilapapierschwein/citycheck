from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from citycheck.db.db import DB


def get_session():
    session = DB._session_factoy()  # pyright: ignore[reportPrivateUsage]
    try:
        yield session
    finally:
        session.close()


CRUDSession = Annotated[Session, Depends(get_session)]
