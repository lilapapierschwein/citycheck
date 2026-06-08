from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.core.validation.models.region import BaseSubregion
from citycheck.db.models import Subregion


def create_region(data: BaseSubregion, session: Session) -> Subregion:
    subregion = Subregion(**data.model_dump())

    session.add(subregion)
    session.commit()

    return subregion


def create_regions(data: list[BaseSubregion], session: Session) -> list[Subregion]:
    subregions = [Subregion(**d.model_dump()) for d in data]

    session.add_all(subregions)
    session.commit()

    return subregions


def read_region(region_id: int, session: Session) -> Subregion:
    return session.get_one(Subregion, region_id)


def read_regions(session: Session) -> Sequence[Subregion]:
    return session.scalars(select(Subregion)).all()


# def update_region(region_id: int, session: Session) -> Subregion: ...


def delete_region(region_id: int, session: Session) -> None:
    try:
        subregion = read_region(1, session)
        session.delete(subregion)
        print(f"Subregion #{region_id} ({repr(subregion.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
