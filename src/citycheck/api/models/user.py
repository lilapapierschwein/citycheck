import re
from datetime import datetime as dt
from typing import Annotated, ClassVar, override

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationError,
    model_serializer,
)

from .activity import ActivityModel
from .location import LocationModel


class UserPasswordCreate(BaseModel):
    user_id: int
    password_hash: str
    is_valid: bool = Field(default=True)

    @override
    def __str__(self) -> str:
        return self.password_hash

    @override
    def __repr__(self) -> str:
        return (
            "UserPasswordCreate("
            f"user_id={repr(self.user_id)}, "
            f"password={repr(self.password_hash)}, "
            f"is_valid={repr(self.is_valid)}"
            ")"
        )


class UserPasswordModel(BaseModel):
    id: int
    user_id: int
    password_hash: str
    is_valid: bool
    user: UserModel

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __str__(self) -> str:
        return self.password_hash

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={repr(self.id)}, "
            f"user_id={repr(self.user_id)}, "
            f"password_hash={repr(self.password_hash)}, "
            f"is_valid={repr(self.is_valid)}"
            ")"
        )


class UserPasswordSchema(UserPasswordModel): ...


class UserActivityCreate(BaseModel):
    user_id: int
    activity_id: int
    timestamp: dt | None = None

    @override
    def __str__(self) -> str:
        return f"Activity#{self.activity_id} (User#{self.user_id})"

    @override
    def __repr__(self) -> str:
        return (
            "UserActivityCreate("
            f"activity_id={repr(self.activity_id)}, "
            f"user_id={repr(self.user_id)}, "
            f"timestamp={repr(self.timestamp)}"
            ")"
        )


class UserActivityModel(BaseModel):
    id: int
    user_id: int
    activity_id: int
    timestamp: dt
    user: UserModel
    activity: ActivityModel

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __str__(self) -> str:
        return f"{self.activity.name} ({self.user.username}) @{self.timestamp}"

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"user_id={repr(self.user_id)}, "
            f"activity_id={repr(self.activity_id)}, "
            f"timestamp={repr(self.timestamp)}"
            ")"
        )


class UserActivitySchema(UserActivityModel): ...


def validate_email(u: object) -> str:
    if not isinstance(u, str) or u == "":
        raise ValidationError("E-Mail must be a non-empty string.")
    if not re.fullmatch(r"^\S+@\S+\.\S+$", u):
        raise ValidationError(f"E-Mail invalid: {repr(u)}")
    return u


ValidEmail = Annotated[str, BeforeValidator(validate_email)]


class UserCreate(BaseModel):
    username: str
    email: ValidEmail
    is_disabled: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    home_location_id: int | None = Field(default=None)

    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)

    @override
    def __str__(self) -> str:
        return self.username

    @override
    def __repr__(self) -> str:
        return (
            "UserCreate("
            f"username={repr(self.username)}, "
            f"email={repr(self.email)}, "
            f"is_disabled={repr(self.is_disabled)}, "
            f"is_deleted={repr(self.is_deleted)}, "
            f"home_location_id={repr(self.username)}"
            ")"
        )


class UserModel(BaseModel):
    id: int
    username: str
    email: ValidEmail
    is_disabled: bool
    is_deleted: bool
    home_location_id: int | None
    home_location: LocationModel | None
    user_locations: list[UserLocationModel]
    activities: list[ActivityModel]

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True
    )

    @override
    def __str__(self) -> str:
        return self.username

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={repr(self.id)}, "
            f"username={repr(self.username)}, "
            f"email={repr(self.email)}, "
            f"is_disabled={repr(self.is_disabled)}, "
            f"is_deleted={repr(self.is_deleted)}, "
            f"home_location_id={repr(self.username)}, "
            f"user_locations={repr(self.user_locations)}"
            ")"
        )

    @property
    def is_active(self) -> bool:
        return not self.is_disabled and not self.is_deleted


class UserSchema(UserModel):
    @model_serializer
    def serialize_model(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_disabled": self.is_disabled,
            "is_deleted": self.is_deleted,
            "home_location": self.home_location,
        }


class UserLocationCreate(BaseModel):
    user_id: int
    location_id: int

    @override
    def __str__(self) -> str:
        return f"Location #{self.location_id}, User #{self.user_id}"

    @override
    def __repr__(self) -> str:
        return (
            "UserLocationCreate("
            f"user_id={repr(self.user_id)}, "
            f"location_id={repr(self.location_id)}"
            ")"
        )


class UserLocationModel(BaseModel):
    id: int
    user_id: int
    location_id: int

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True, arbitrary_types_allowed=True
    )

    @override
    def __str__(self) -> str:
        return f"Location #{self.location_id}, User #{self.user_id}"

    @override
    def __repr__(self) -> str:
        return (
            "UserLocationModel("
            f"user_id={repr(self.user_id)}, "
            # f"user={repr(self.user)}, "
            f"location_id={repr(self.location_id)}"
            # f"location={repr(self.location)}"
            ")"
        )


class UserLocationSchema(UserLocationModel):
    ...
    # @model_serializer
    # def serialize_model(self):
    #     return {"id": self.id, "user": self.user, "location": self.location}
