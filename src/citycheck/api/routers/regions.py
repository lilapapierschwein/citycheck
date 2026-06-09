from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from citycheck.api import crud
from citycheck.api.models.region import (
    RegionCreate,
    RegionSchema,
    SubregionCreate,
    SubregionSchema,
)
from citycheck.api.utils import CRUDSession

subregions_router = APIRouter(prefix="/subregions", tags=["subregions"])


@subregions_router.get("/{subregion_id}")
async def get_subregion(subregion_id: int, session: CRUDSession):
    subregion = await crud.read_subregion(subregion_id, session)
    if not subregion:
        raise HTTPException(status_code=404, detail="Subregion not found.")
    schema = SubregionSchema.model_validate(subregion)
    return schema


@subregions_router.get("")
async def get_subregions(session: CRUDSession):
    subregions = await crud.read_subregions(session)
    if not subregions:
        raise HTTPException(status_code=404, detail="No subregions found.")
    return [SubregionSchema.model_validate(s) for s in subregions]


@subregions_router.post("")
async def post_subregion(data: SubregionCreate, session: CRUDSession):
    try:
        subregion = await crud.create_subregion(data, session)
        schema = SubregionSchema.model_validate(subregion)
        return schema
    except IntegrityError as err:
        return HTTPException(404, detail=err)


@subregions_router.delete("/{subregion_id}")
async def delete_subregion(subregion_id: int, session: CRUDSession):
    try:
        await crud.delete_subregion(subregion_id, session)
        return {"status": "success"}
    except NoResultFound as err:
        return {"status", str(err)}


regions_router = APIRouter(prefix="/regions", tags=["regions"])


@regions_router.get("/{region_id}")
async def get_region(region_id: int, session: CRUDSession):
    region = await crud.read_region(region_id, session)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found.")
    schema = RegionSchema.model_validate(region)
    return schema


@regions_router.get("")
async def get_regions(session: CRUDSession):
    regions = await crud.read_regions(session)
    if not regions:
        raise HTTPException(status_code=404, detail="No subregions found.")
    return [RegionSchema.model_validate(r) for r in regions]


@regions_router.post("")
async def post_user(data: RegionCreate, session: CRUDSession):
    try:
        region = await crud.create_region(data, session)
        schema = RegionSchema.model_validate(region)
        return schema
    except IntegrityError as err:
        return HTTPException(404, detail=err)


@regions_router.delete("/{region_id}")
async def delete_user(region_id: int, session: CRUDSession):
    try:
        await crud.delete_region(region_id, session)
        return {"status": "success"}
    except NoResultFound as err:
        return {"status": str(err)}
