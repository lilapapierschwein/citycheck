from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from citycheck.api import crud
from citycheck.api.filters_forms.countries import CountryQueryFilters
from citycheck.api.models.country import CountryCreate, CountrySchema
from citycheck.api.utils import CRUDSession
from citycheck.core.utils import get_timestamp

router = APIRouter(prefix="/countries", tags=["countries"])


@router.get("/{country_id}")
async def get_country(country_id: int, session: CRUDSession):
    country = await crud.read_country(country_id, session)
    if not country:
        raise HTTPException(status_code=404, detail="Language not found.")
    schema = CountrySchema.model_validate(country)
    return schema


@router.get("")
async def get_countries(session: CRUDSession, query_params: CountryQueryFilters):
    countries, total = await crud.read_countries(session, query_params)
    return {
        "data": {
            "objects": [CountrySchema.model_validate(c) for c in countries],
            "meta": {
                "count": len(countries),
                "total": total,
                "limit": query_params.limit,
                "offset": query_params.offset,
                "timestamp": int(get_timestamp()),
            },
        }
    }


@router.post("")
async def post_country(data: CountryCreate, session: CRUDSession):
    try:
        country = await crud.create_country(data, session)
        schema = CountrySchema.model_validate(country)
        return schema
    except IntegrityError as err:
        return HTTPException(404, detail=err)


@router.delete("/{country_id}")
async def delete_country(country_id: int, session: CRUDSession):
    try:
        await crud.delete_country(country_id, session)
        return {"status": "success"}
    except NoResultFound as err:
        return {"status": str(err)}
