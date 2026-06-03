import re
from typing import Annotated, ClassVar

from pydantic import BaseModel, BeforeValidator, ConfigDict, ValidationError

from .location import LocationModel


def validate_email(u: object) -> str:
    if not isinstance(u, str) or u == "":
        raise ValidationError("E-Mail must be a non-empty string.")
    if not re.fullmatch(r"^\S+@\S+\.\S+$", u):
        raise ValidationError(f"E-Mail invalid: {repr(u)}")
    return u


ValidEmail = Annotated[str, BeforeValidator(validate_email)]


class BaseUser(BaseModel):
    username: str
    email: ValidEmail
    home_location_id: int | None


class UserModel(BaseUser):
    id: int
    home_location: LocationModel | None

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True
    )


class UserSchema(UserModel): ...
