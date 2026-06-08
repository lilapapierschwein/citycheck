import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from citycheck.api import crud
from citycheck.api.utils import CRUDSession
from citycheck.core.validation.models.user import (
    UserCreate,
    UserModel,
    UserSchema,
)
from citycheck.settings import ROOT

app = FastAPI()


@app.get("/")
async def get_root():
    return {"Hello": "World"}


@app.get("/users/{user_id}")
async def get_user(user_id: int, session: CRUDSession):
    user = await crud.read_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    user_model = UserModel.model_validate(user)
    return user_model


@app.get("/users/")
async def get_users(session: CRUDSession):
    users = await crud.read_users(session)
    if not users:
        raise HTTPException(status_code=404, detail="No users not found.")
    return [UserSchema.model_validate(u) for u in users]


@app.post("/users")
async def post_user(user_data: UserCreate, session: CRUDSession):
    try:
        user = await crud.create_user(user_data, session)
        return user
    except IntegrityError as err:
        return HTTPException(404, detail=err)


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, session: CRUDSession):
    try:
        await crud.delete_user(user_id, session)
        return {"status": "success"}
    except NoResultFound as err:
        return {"status", str(err)}


def main() -> None:
    uvicorn.run(
        app="main:app",
        app_dir=str(ROOT / "src" / "citycheck" / "api"),
        port=8000,
    )


if __name__ == "__main__":
    main()
