from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select

from citycheck.api.filters_forms.users import UserQueryFilters
from citycheck.api.models.user import UserCreate
from citycheck.db.models import User


async def create_user(data: UserCreate, session: Session) -> User:
    user = User(**data.model_dump())

    session.add(user)
    session.commit()

    return user


async def create_users(data: list[UserCreate], session: Session) -> list[User]:
    users = [User(**d.model_dump()) for d in data]

    session.add_all(users)
    session.commit()

    return users


async def read_user(user_id: int, session: Session) -> User | None:
    return session.scalar(select(User).where(User.id == user_id))


async def read_users(session: Session, filters: UserQueryFilters) -> tuple[Sequence[User], int]:
    total = session.scalar(select(func.count()).select_from(User)) or 0
    stmt = filters.apply(select(User))
    return session.scalars(stmt).all(), total


# def update_user(user_id: int, session: Session) -> User: ...


async def delete_user(user_id: int, session: Session) -> None:
    try:
        user = await read_user(user_id, session)
        if not user:
            raise NoResultFound(f"User with id {user_id} not found.")
        session.delete(user)
        session.commit()
        print(f"User #{user_id} ({repr(user.username)}) deleted.")
    except NoResultFound as err:
        raise NoResultFound(str(err)) from NoResultFound
    return None
