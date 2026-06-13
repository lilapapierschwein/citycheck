from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from citycheck.db.db import DB


def get_session():
    session = DB._session_factory()  # pyright: ignore[reportPrivateUsage]
    try:
        yield session
    finally:
        session.close()


CRUDSession = Annotated[Session, Depends(get_session)]


def is_hx_request(request: Request) -> bool:
    hxr: str | None = request.headers.get("hx-request", None)
    return hxr is not None


HxReq = Annotated[bool, Depends(is_hx_request)]


def is_web_request(request: Request) -> bool:
    return "application/json" not in request.headers.get("accept", "").split()


WebReq = Annotated[bool, Depends(is_web_request)]
