from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from citycheck.api import crud
from citycheck.api.models.language import (
    LanguageCreate,
    LanguageSchema,
)
from citycheck.api.utils import CRUDSession

router = APIRouter(prefix="/languages", tags=["languages"])


@router.get("/{language_id}")
async def get_subregion(language_id: int, session: CRUDSession):
    language = await crud.read_language(language_id, session)
    if not language:
        raise HTTPException(status_code=404, detail="Language not found.")
    schema = LanguageSchema.model_validate(language)
    return schema


@router.get("")
async def get_languages(session: CRUDSession):
    languages = await crud.read_languages(session)
    if not languages:
        raise HTTPException(status_code=404, detail="No languages found.")
    return [LanguageSchema.model_validate(lang) for lang in languages]


@router.post("")
async def post_language(data: LanguageCreate, session: CRUDSession):
    try:
        language = await crud.create_language(data, session)
        schema = LanguageSchema.model_validate(language)
        return schema
    except IntegrityError as err:
        return HTTPException(404, detail=err)


@router.delete("/{language_id}")
async def delete_language(language_id: int, session: CRUDSession):
    try:
        await crud.delete_language(language_id, session)
        return {"status": "success"}
    except NoResultFound as err:
        return {"status", str(err)}
