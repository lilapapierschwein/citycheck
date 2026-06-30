from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from citycheck.api import crud
from citycheck.api.models.user import (
    UserLocationCreate,
    UserLocationSchema,
)
from citycheck.api.utils import CRUDSession
from citycheck.core.utils import get_timestamp

router = APIRouter(prefix="/users_locations", tags=["users_location"])


@router.get("/{user_location_id}")
async def get_user_location(user_location_id: int, session: CRUDSession):
    user_location = await crud.read_user_location(user_location_id, session)
    if not user_location:
        raise HTTPException(status_code=404, detail=f"UserLocation #{user_location_id} not found.")
    schema = UserLocationSchema.model_validate(user_location)
    return schema


@router.get("")
async def get_users_locations(session: CRUDSession):
    users_locations, total = await crud.read_user_locations(session)
    return {
        "data": {
            "objects": [UserLocationSchema.model_validate(ul) for ul in users_locations],
            "meta": {
                "count": len(users_locations),
                "total": total,
                # "limit": filters.limit,
                # "offset": filters.offset,
                "timestamp": int(get_timestamp()),
            },
        }
    }


@router.post("")
async def post_user_location(user_location_data: UserLocationCreate, session: CRUDSession):
    try:
        user_location = await crud.create_user_location(user_location_data, session)
        schema = UserLocationSchema.model_validate(user_location)
        return schema
    except (IntegrityError, NoResultFound, LookupError) as err:
        raise HTTPException(404, detail=err) from err


# @router.delete("/{user_location_id}")
# async def delete_user_location(user_location_id: int, session: CRUDSession):
#     try:
#         await crud.delete_user(user_id, session)
#         return {"status": "success", "detail": f"User #{user_id} deleted."}
#     except NoResultFound as err:
#         raise HTTPException(status_code=404, detail=str(err)) from err
