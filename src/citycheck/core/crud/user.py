from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

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


def read_users(session: Session) -> Sequence[User]:
    return session.scalars(select(User)).all()


# def update_user(user_id: int, session: Session) -> User: ...


def delete_user(user_id: int, session: Session) -> None:
    try:
        user = read_user(1, session)
        session.delete(user)
        session.commit()
        print(f"User #{user_id} ({repr(user.username)}) deleted.")
    except NoResultFound as err:
        print(err)
    return None
