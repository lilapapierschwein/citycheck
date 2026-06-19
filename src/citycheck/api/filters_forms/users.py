from typing import Annotated, Literal, override

from fastapi import Query
from pydantic import Field
from sqlalchemy import Select
from sqlalchemy.orm import InstrumentedAttribute, joinedload
from sqlalchemy.sql import func, or_
from sqlalchemy.sql.elements import UnaryExpression

from citycheck.db.models import (
    User,
)

from .query_params import LowercaseStr, QueryParams


class UserQueryParams(QueryParams):
    orderBy: Literal[
        "id",
        "username",
        "email",
        "homeLocation",
    ] = "id"
    username: LowercaseStr | None = None
    email: LowercaseStr | None = None
    is_disabled: bool | None = Field(validation_alias="isDisabled", default=None)
    is_deleted: bool | None = Field(validation_alias="isDeleted", default=None)
    home_location: LowercaseStr | None = Field(validation_alias="homeLocation", default=None)
    q: LowercaseStr | None = None

    @override
    def __str__(self) -> str:
        return "UserQueryParams"

    @override
    def __repr__(self) -> str:
        return (
            "UserQueryParams("
            f"orderBy={repr(self.orderBy)}, "
            f"username={repr(self.username)}, "
            f"email={repr(self.email)}, "
            f"is_disabled={repr(self.is_disabled)}, "
            f"is_deleted={repr(self.is_deleted)}, "
            f"home_location={repr(self.home_location)}, "
            f"q={repr(self.q)}"
            ")"
        )

    @property
    def order_by(
        self,
    ) -> UnaryExpression[InstrumentedAttribute[User]] | InstrumentedAttribute[User]:
        """Returns the SQLAlchemy order_by expression based on the orderBy and sort parameters."""
        return getattr(User, self._order_col).asc() if self.sort == "asc" else getattr(User, self._order_col).desc()

    def apply(self, stmt: Select[tuple[User]]) -> Select[tuple[User]]:
        if self.q:
            stmt = stmt.where(
                or_(
                    User.username.ilike(f"%{self.q}%"),
                    User.email.ilike(f"%{self.q}%"),
                )
            )
        else:
            if self.username:
                stmt = stmt.where(func.lower(User.username) == self.username)
            if self.email:
                stmt = stmt.where(func.lower(User.email) == self.email)
            if self.is_disabled:
                stmt = stmt.where(User.is_disabled)
            if self.is_deleted:
                stmt = stmt.where(User.is_deleted)
            # if self.home_location:
            #     stmt = stmt.where(func.lower(Location.name) == self.home_location)

        stmt = stmt.order_by(self.order_by)
        if self.limit > 0:
            stmt = stmt.limit(self.limit)
        stmt = stmt.offset(self.offset)

        return stmt.options(joinedload(User.home_location))


UserQueryFilters = Annotated[UserQueryParams, Query()]
