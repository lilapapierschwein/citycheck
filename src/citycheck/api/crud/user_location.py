from sqlalchemy import and_, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.api.models.user import UserLocationCreate
from citycheck.db.models import UserLocation

from .location import read_location
from .user import read_user


async def create_user_location(
    user_location: UserLocationCreate, session: Session
) -> UserLocation:
    user_id, location_id = user_location.user_id, user_location.location_id

    user_location_existing = session.scalar(
        select(UserLocation).where(
            and_(UserLocation.user_id == user_id, UserLocation.location_id == location_id)
        )
    )
    if user_location_existing:
        return user_location_existing

    user = await read_user(user_location.user_id, session)
    if not user:
        raise NoResultFound(f"User with id {user_id} not found.")
    if user.home_location_id and user.home_location_id == location_id:
        raise LookupError(f"Location#{location_id} is already set as user home.")

    location = await read_location(location_id, session)
    if not location:
        raise NoResultFound(f"Location with id {location_id} not found.")

    user_location_in = UserLocation(**user_location.model_dump())
    session.add(user_location_in)
    session.commit()
    return user_location_in


async def read_user_location(user_location_id: int, session: Session) -> UserLocation | None:
    return session.scalar(select(UserLocation).where(UserLocation.id == user_location_id))


async def read_user_locations(session: Session):
    total = session.scalar(select(func.count()).select_from(UserLocation)) or 0
    return session.scalars(select(UserLocation)).all(), total
