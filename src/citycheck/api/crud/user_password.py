from sqlalchemy.orm import Session

from citycheck.api.models.user import UserPasswordCreate
from citycheck.db.models import UserPassword

from .user import read_user


async def create_user_password(
    user_password: UserPasswordCreate, session: Session
) -> UserPassword:
    user = await read_user(user_password.user_id, session)
    if not user:
        raise LookupError("User not found")
    for pw in user.passwords_hashes:
        pw.is_valid = False

    user_password_in = UserPassword(**user_password.model_dump())
    session.add(user_password_in)
    session.commit()
    return user_password_in
