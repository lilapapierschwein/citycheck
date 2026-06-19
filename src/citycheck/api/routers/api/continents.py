from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from citycheck.api import crud
from citycheck.api.filters_forms.continents import ContinentQueryFilters
from citycheck.api.models.continent import ContinentCreate, ContinentSchema
from citycheck.api.utils import CRUDSession
from citycheck.core.utils import get_timestamp

router = APIRouter(prefix="/continents", tags=["continents"])


@router.get("/{continent_id}")
async def get_continent(continent_id: int, session: CRUDSession):
    continent = await crud.read_continent(continent_id, session)
    if not continent:
        raise HTTPException(status_code=404, detail="Language not found.")
    schema = ContinentSchema.model_validate(continent)
    return schema


@router.get("")
async def get_continents(session: CRUDSession, filters: ContinentQueryFilters):
    continents, total = await crud.read_continents(session, filters)
    return {
        "data": {
            "objects": [ContinentSchema.model_validate(c) for c in continents],
            "meta": {
                "count": len(continents),
                "total": total,
                "limit": filters.limit,
                "offset": filters.offset,
                "timestamp": int(get_timestamp()),
            },
        }
    }


@router.post("")
async def post_continent(data: ContinentCreate, session: CRUDSession):
    try:
        continent = await crud.create_continent(data, session)
        schema = ContinentSchema.model_validate(continent)
        return schema
    except IntegrityError as err:
        return HTTPException(404, detail=err)


@router.delete("/{continent_id}")
async def delete_continent(continent_id: int, session: CRUDSession):
    try:
        await crud.delete_continent(continent_id, session)
        return {"status": "success"}
    except NoResultFound as err:
        return {"status", str(err)}
