from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.core.validation.models.language import BaseLanguage
from citycheck.db.models import Language


def create_language(data: BaseLanguage, session: Session) -> Language:
    language = Language(**data.model_dump())

    session.add(language)
    session.commit()

    return language


def create_languages(data: list[BaseLanguage], session: Session) -> list[Language]:
    languages = [Language(**d.model_dump()) for d in data]

    session.add_all(languages)
    session.commit()

    return languages


def read_language(language_id: int, session: Session) -> Language:
    return session.get_one(Language, language_id)


def read_languages(session: Session) -> Sequence[Language]:
    return session.scalars(select(Language)).all()


# def update_language(language_id: int, session: Session) -> Language: ...


def delete_language(language_id: int, session: Session) -> None:
    try:
        language = read_language(1, session)
        session.delete(language)
        print(f"Language #{language_id} ({repr(language.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
