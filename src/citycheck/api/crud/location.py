from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.core.validation.models.location import LocationCreate
from citycheck.db.models import Location


async def create_location(data: LocationCreate, session: Session) -> Location:
    location = Location(**data.model_dump())

    session.add(location)
    session.commit()

    return location


async def create_locations(
    data: list[LocationCreate], session: Session
) -> list[Location]:
    users = [Location(**d.model_dump()) for d in data]

    session.add_all(users)
    session.commit()

    return users


async def read_location(location_id: int, session: Session) -> Location:
    return session.get_one(Location, location_id)


async def read_locations(session: Session) -> Sequence[Location]:
    return session.scalars(select(Location)).all()


# def update_country(location_id: int, session: Session) -> Location: ...


async def delete_location(location_id: int, session: Session) -> None:
    try:
        location = await read_location(1, session)
        session.delete(location)
        print(f"Location #{location_id} ({repr(location.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
