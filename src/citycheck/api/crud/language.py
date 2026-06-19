from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.api.filters_forms.languages import LanguageQueryFilters
from citycheck.api.models.language import LanguageCreate
from citycheck.db.models import Language


async def create_language(data: LanguageCreate, session: Session) -> Language:
    language = Language(**data.model_dump())

    session.add(language)
    session.commit()

    return language


async def create_languages(
    data: list[LanguageCreate], session: Session
) -> list[Language]:
    languages = [Language(**d.model_dump()) for d in data]

    session.add_all(languages)
    session.commit()

    return languages


async def read_language(language_id: int, session: Session) -> Language:
    return session.get_one(Language, language_id)


async def read_languages(
    session: Session, filters: LanguageQueryFilters
) -> Sequence[Language]:
    stmt = filters.apply(select(Language))
    return session.scalars(stmt).all()


# def update_language(language_id: int, session: Session) -> Language: ...


async def delete_language(language_id: int, session: Session) -> None:
    try:
        language = await read_language(1, session)
        session.delete(language)
        print(f"Language #{language_id} ({repr(language.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
