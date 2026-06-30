from sqlalchemy.orm import Session

from citycheck.api.models.user import UserActivityCreate
from citycheck.db.models import UserActivity


async def create_user_activity(
    user_activity_data: UserActivityCreate, session: Session
) -> UserActivity:
    user_activity = UserActivity(**user_activity_data.model_dump())
    session.add(user_activity)
    session.commit()
    return user_activity


# async def read_user_location(user_location_id: int, session: Session) -> UserLocation | None:
#     return session.scalar(select(UserLocation).where(UserLocation.id == user_location_id))
#
#
# async def read_user_locations(session: Session):
#     total = session.scalar(select(func.count()).select_from(UserLocation)) or 0
#     return session.scalars(select(UserLocation)).all(), total
