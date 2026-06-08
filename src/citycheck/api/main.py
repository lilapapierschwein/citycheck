from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from citycheck.api import crud
from citycheck.core.validation.models.user import BaseUser, UserModel, UserSchema
from citycheck.db.db import DB

app = FastAPI()


def get_session():
    session = DB._session_factoy()  # pyright: ignore[reportPrivateUsage]
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
async def get_root():
    return {"Hello": "World"}


@app.get("/users/{user_id}")
async def get_user(user_id: int, session: SessionDep):
    user = await crud.read_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user_model = UserModel.model_validate(user)
    return user_model


@app.get("/users/")
async def get_users(session: SessionDep):
    users = await crud.read_users(session)
    if not users:
        raise HTTPException(status_code=404, detail="No users not found.")
    return [UserSchema.model_validate(u) for u in users]


@app.post("/users")
async def post_user(user_data: BaseUser, session: SessionDep):
    try:
        user = await crud.create_user(user_data, session)
        return user
    except IntegrityError as err:
        return HTTPException(404, detail=err)


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: SessionDep):
    try:
        await crud.delete_user(user_id, session)
        return {"status": "success"}
    except NoResultFound as err:
        return {"status", str(err)}


def main() -> None:
    uvicorn.run(
        app="main:app",
        app_dir=str(Path("/home/kelsa/Projects/citycheck/src/citycheck/api")),
        port=8000,
    )


if __name__ == "__main__":
    main()
