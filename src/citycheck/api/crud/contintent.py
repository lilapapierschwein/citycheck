from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.core.validation.models.continent import BaseContinent
from citycheck.db.models import Continent


def create_continent(data: BaseContinent, session: Session) -> Continent:
    continent = Continent(**data.model_dump())

    session.add(continent)
    session.commit()

    return continent


def create_continents(data: list[BaseContinent], session: Session) -> list[Continent]:
    users = [Continent(**d.model_dump()) for d in data]

    session.add_all(users)
    session.commit()

    return users


def read_continent(continent_id: int, session: Session) -> Continent:
    return session.get_one(Continent, continent_id)


def read_continents(session: Session) -> Sequence[Continent]:
    return session.scalars(select(Continent)).all()


# def update_continent(continent_id: int, session: Session) -> Continent: ...


def delete_continent(continent_id: int, session: Session) -> None:
    try:
        continent = read_continent(1, session)
        session.delete(continent)
        print(f"Continent #{continent_id} ({repr(continent.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
