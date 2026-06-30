from sqlalchemy.orm import Session

from citycheck.api.models.activity import ActivityCreate
from citycheck.db.models import Activity


async def create_activity(activity_data: ActivityCreate, session: Session) -> Activity:
    activity = Activity(**activity_data.model_dump())
    session.add(activity)
    session.commit()
    return activity


# async def read_user_location(user_location_id: int, session: Session) -> UserLocation | None:
#     return session.scalar(select(UserLocation).where(UserLocation.id == user_location_id))
#
#
# async def read_user_locations(session: Session):
#     total = session.scalar(select(func.count()).select_from(UserLocation)) or 0
#     return session.scalars(select(UserLocation)).all(), total
