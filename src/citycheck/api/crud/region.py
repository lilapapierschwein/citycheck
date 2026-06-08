from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.core.validation.models.region import BaseRegion
from citycheck.db.models import Region


def create_region(data: BaseRegion, session: Session) -> Region:
    region = Region(**data.model_dump())

    session.add(region)
    session.commit()

    return region


def create_regions(data: list[BaseRegion], session: Session) -> list[Region]:
    users = [Region(**d.model_dump()) for d in data]

    session.add_all(users)
    session.commit()

    return users


def read_region(region_id: int, session: Session) -> Region:
    return session.get_one(Region, region_id)


def read_regions(session: Session) -> Sequence[Region]:
    return session.scalars(select(Region)).all()


# def update_region(region_id: int, session: Session) -> Region: ...


def delete_region(region_id: int, session: Session) -> None:
    try:
        region = read_region(1, session)
        session.delete(region)
        print(f"Region #{region_id} ({repr(region.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
