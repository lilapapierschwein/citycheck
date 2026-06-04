from sqlalchemy.orm import Session

from citycheck.core.validation.models.user import BaseUser
from citycheck.db.models import User


def create_user(data: BaseUser, session: Session) -> User:
    user = User(**data.model_dump())

    session.add(user)
    session.commit()

    return user


def create_users(data: list[BaseUser], session: Session) -> list[User]:
    users = [User(**d.model_dump()) for d in data]

    session.add_all(users)
    session.commit()

    return users


def read_user(user_id: int, session: Session) -> User:
    return session.get_one(User, user_id)
