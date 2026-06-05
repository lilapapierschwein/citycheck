import re
from typing import Annotated, ClassVar, override

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, ValidationError

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
    home_location_id: int | None = Field(default=None)

    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)

    @override
    def __str__(self) -> str:
        return self.username

    @override
    def __repr__(self) -> str:
        return (
            "BaseUser("
            f"username={repr(self.username)}, "
            f"email={repr(self.email)}, "
            f"home_location_id={repr(self.username)}"
            ")"
        )


class UserModel(BaseUser):
    id: int
    home_location: LocationModel | None

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True
    )

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={repr(self.id)}, "
            f"username={repr(self.username)}, "
            f"email={repr(self.email)}, "
            f"home_location_id={repr(self.username)}"
            ")"
        )


class UserSchema(UserModel): ...
