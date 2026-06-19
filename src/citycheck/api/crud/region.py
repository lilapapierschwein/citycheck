from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select

from citycheck.api.filters_forms.regions import RegionQueryFilters
from citycheck.api.models.region import RegionCreate
from citycheck.db.models import Region


async def create_region(data: RegionCreate, session: Session) -> Region:
    region = Region(**data.model_dump())

    session.add(region)
    session.commit()

    return region


async def create_regions(data: list[RegionCreate], session: Session) -> list[Region]:
    users = [Region(**d.model_dump()) for d in data]

    session.add_all(users)
    session.commit()

    return users


async def read_region(region_id: int, session: Session) -> Region:
    return session.get_one(Region, region_id)


async def read_regions(session: Session, filters: RegionQueryFilters) -> tuple[Sequence[Region], int]:
    total = session.scalar(select(func.count()).select_from(Region)) or 0
    stmt = filters.apply(select(Region))
    return session.scalars(stmt).all(), total


# def update_region(region_id: int, session: Session) -> Region: ...


async def delete_region(region_id: int, session: Session) -> None:
    try:
        region = await read_region(1, session)
        session.delete(region)
        print(f"Region #{region_id} ({repr(region.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
