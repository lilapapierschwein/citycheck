from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from citycheck.api import crud
from citycheck.api.filters_forms.users import UserQueryFilters
from citycheck.api.models.user import (
    UserCreate,
    UserSchema,
)
from citycheck.api.utils import CRUDSession

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: int, session: CRUDSession):
    user = await crud.read_user(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail=f"User #{user_id} not found.")
    user_schema = UserSchema.model_validate(user)
    return user_schema


@router.get("")
async def get_users(session: CRUDSession, filters: UserQueryFilters):
    users = await crud.read_users(session, filters)
    if not users:
        raise HTTPException(status_code=404, detail="No users not found.")
    return [UserSchema.model_validate(u) for u in users]


@router.post("")
async def post_user(user_data: UserCreate, session: CRUDSession):
    try:
        user = await crud.create_user(user_data, session)
        user_schema = UserSchema.model_validate(user)
        return user_schema
    except IntegrityError as err:
        raise HTTPException(404, detail=err) from err


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: CRUDSession):
    try:
        await crud.delete_user(user_id, session)
        return {"status": "success", "detail": f"User #{user_id} deleted."}
    except NoResultFound as err:
        raise HTTPException(status_code=404, detail=str(err)) from err
