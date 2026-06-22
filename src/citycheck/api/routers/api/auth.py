from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from citycheck.api.security import WWW_AUTH_HEADER, Token, create_access_token, verify_credentials
from citycheck.api.utils import CRUDSession

router = APIRouter(prefix="/auth", tags=["api", "auth"])


@router.post("/token", response_model=Token)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: CRUDSession,
):
    user = await verify_credentials(form.username, form.password, session)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers=WWW_AUTH_HEADER,
        )
    token = create_access_token({"sub": user.username})
    return Token(access_token=token, token_type="bearer")
