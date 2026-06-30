from collections.abc import Mapping
from datetime import UTC
from datetime import datetime as dt
from datetime import timedelta as td
from typing import Annotated, Any

import jwt
from fastapi import Cookie, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from citycheck import get_config
from citycheck.api.crud.user import get_user_by_username
from citycheck.api.utils import CRUDSession, get_session
from citycheck.db.models import User

app_config = get_config()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

dotenv_file = app_config.paths.files.dotenv

JWT_SECRET_KEY = app_config.security.jwt_secret_key
JWT_ALGO = app_config.security.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = app_config.api.settings.access_token_expire_minutes


ByteStr = str | bytes

WWW_AUTH_HEADER = {"WWW-Authenticate": "Bearer"}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


pwd_context = PasswordHash.recommended()


def hash_password(pw: str) -> str:
    return pwd_context.hash(pw)


def verify_password(pw: str, hash: str) -> bool:
    return pwd_context.verify(pw, hash)


async def verify_credentials(username: str, pw: str, session: Session):
    user = await get_user_by_username(username, session)
    if not user:
        return None

    active_pw = next((pw for pw in user.passwords_hashes if pw.is_valid), None)
    if not active_pw or not verify_password(pw, active_pw.password_hash):
        return None
    return user


def create_access_token(data: dict[str, Any], expires_delta: td | None = None) -> str:
    payload = data.copy()
    expire = dt.now(UTC) + (expires_delta or td(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    payload["exp"] = expire
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGO)  # pyright: ignore[reportUnknownMemberType]


class CredentialsException(HTTPException):
    def __init__(
        self,
        status_code: int = HTTP_401_UNAUTHORIZED,
        detail: str = "Unable to verify credentials",
        headers: Mapping[str, str] | None = WWW_AUTH_HEADER,
    ) -> None:
        super().__init__(status_code, detail, headers)


def decode_access_token(token: ByteStr) -> TokenData:
    try:
        payload: dict[str, Any] = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGO])  # pyright: ignore[reportUnknownMemberType]
        username: Any | None = payload.get("sub")
        if username is None:
            raise CredentialsException
        return TokenData(username=username)
    except InvalidTokenError as err:
        raise CredentialsException from err


async def get_current_user(token: ByteStr, session: Session) -> User:
    token_data = decode_access_token(token)
    if token_data.username is None:
        raise CredentialsException

    user = await get_user_by_username(token_data.username, session)
    if user is None:
        raise CredentialsException
    return user


async def get_current_active_user(token: ByteStr, session: Session) -> User:
    user = await get_current_user(token, session)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


OAuth2Dep = Annotated[ByteStr, Depends(oauth2_scheme)]


async def api_get_current_user(token: OAuth2Dep, session: Session = Depends(get_session)) -> User:  # pyright: ignore[reportCallInDefaultInitializer]  # noqa: B008
    return await get_current_active_user(token, session)


# AccessToken = Annotated[str | None, Depends(Cookie(default=None))]


async def web_get_current_user(
    session: CRUDSession,
    access_token: str | None = Cookie(default=None),  # pyright: ignore[reportCallInDefaultInitializer]
) -> User | None:
    if access_token is None:
        return None
    try:
        return await get_current_active_user(access_token, session)
    except HTTPException:
        return None


CurrentUser = Annotated[User, Depends(api_get_current_user)]
WebCurrentUser = Annotated[User | None, Depends(web_get_current_user)]
