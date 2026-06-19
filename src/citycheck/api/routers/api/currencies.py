from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from citycheck.api import crud
from citycheck.api.filters_forms.currencies import CurrencyQueryFilters
from citycheck.api.models.currency import CurrencyCreate, CurrencySchema
from citycheck.api.utils import CRUDSession
from citycheck.core.utils import get_timestamp

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("/{currency_id}")
async def get_currency(currency_id: int, session: CRUDSession):
    currency = await crud.read_currency(currency_id, session)
    if not currency:
        raise HTTPException(status_code=404, detail="Language not found.")
    schema = CurrencySchema.model_validate(currency)
    return schema


@router.get("")
async def get_currencies(session: CRUDSession, filters: CurrencyQueryFilters):
    currencies, total = await crud.read_currencies(session, filters)
    return {
        "data": {
            "objects": [CurrencySchema.model_validate(c) for c in currencies],
            "meta": {
                "count": len(currencies),
                "total": total,
                "limit": filters.limit,
                "offset": filters.offset,
                "timestamp": int(get_timestamp()),
            },
        }
    }


@router.post("")
async def post_currency(data: CurrencyCreate, session: CRUDSession):
    try:
        currency = await crud.create_currency(data, session)
        schema = CurrencySchema.model_validate(currency)
        return schema
    except IntegrityError as err:
        return HTTPException(404, detail=err)


@router.delete("/{currency_id}")
async def delete_currency(currency_id: int, session: CRUDSession):
    try:
        await crud.delete_language(currency_id, session)
        return {"status": "success"}
    except NoResultFound as err:
        return {"status": str(err)}
