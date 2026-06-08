from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.api.models.region import SubregionCreate
from citycheck.db.models import Subregion


async def create_subregion(data: SubregionCreate, session: Session) -> Subregion:
    subregion = Subregion(**data.model_dump())

    session.add(subregion)
    session.commit()

    return subregion


async def create_subregions(
    data: list[SubregionCreate], session: Session
) -> list[Subregion]:
    subregions = [Subregion(**d.model_dump()) for d in data]

    session.add_all(subregions)
    session.commit()

    return subregions


async def read_subregion(region_id: int, session: Session) -> Subregion:
    return session.get_one(Subregion, region_id)


async def read_subregions(session: Session) -> Sequence[Subregion]:
    return session.scalars(select(Subregion)).all()


# def update_region(region_id: int, session: Session) -> Subregion: ...


async def delete_subregion(region_id: int, session: Session) -> None:
    try:
        subregion = await read_subregion(1, session)
        session.delete(subregion)
        print(f"Subregion #{region_id} ({repr(subregion.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
