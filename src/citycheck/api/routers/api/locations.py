from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from citycheck.api import crud
from citycheck.api.models.location import (
    LocationCreate,
    LocationSchema,
)
from citycheck.api.utils import CRUDSession

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/{location_id}")
async def get_location(location_id: int, session: CRUDSession):
    location = await crud.read_location(location_id, session)
    if not location:
        raise HTTPException(status_code=404, detail="Language not found.")
    schema = LocationSchema.model_validate(location)
    return schema


@router.get("")
async def get_locations(session: CRUDSession):
    locations = await crud.read_locations(session)
    if not locations:
        raise HTTPException(status_code=404, detail="No locations found.")
    return [LocationSchema.model_validate(loc) for loc in locations]


@router.post("")
async def post_location(data: LocationCreate, session: CRUDSession):
    try:
        location = await crud.create_location(data, session)
        schema = LocationSchema.model_validate(location)
        return schema
    except IntegrityError as err:
        return HTTPException(404, detail=err)


@router.delete("/{location_id}")
async def delete_location(location_id: int, session: CRUDSession):
    try:
        await crud.delete_location(location_id, session)
        return {"status": "success"}
    except NoResultFound as err:
        return {"status", str(err)}
