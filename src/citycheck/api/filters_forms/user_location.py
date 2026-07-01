from typing import Annotated, Literal, override

from fastapi import Query
from sqlalchemy import Select
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import func, or_
from sqlalchemy.sql.elements import UnaryExpression

from citycheck.db.models import (
    Location,
    User,
    UserLocation,
)

from .query_params import LowercaseStr, QueryParams


class UserLocationQueryParams(QueryParams):
    orderBy: Literal[
        "id",
        "location_name",
    ] = "id"
    user_id: int | None = None
    username: LowercaseStr | None = None
    location_id: int | None = None
    location_name: LowercaseStr | None = None
    q: LowercaseStr | None = None

    @override
    def __str__(self) -> str:
        return "UserLocationQueryParams"

    @override
    def __repr__(self) -> str:
        return (
            "UserLocationQueryParams("
            f"orderBy={repr(self.orderBy)}, "
            f"user_id={repr(self.user_id)}, "
            f"username={repr(self.username)}, "
            f"location_id={repr(self.location_id)}, "
            f"location_name={repr(self.location_name)}, "
            f"q={repr(self.q)}"
            ")"
        )

    @property
    def order_by(
        self,
    ) -> (
        UnaryExpression[InstrumentedAttribute[UserLocation]] | InstrumentedAttribute[UserLocation]
    ):
        """Returns the SQLAlchemy order_by expression based on the orderBy and sort parameters."""
        return (
            getattr(UserLocation, self._order_col).asc()
            if self.sort == "asc"
            else getattr(UserLocation, self._order_col).desc()
        )

    def apply(self, stmt: Select[tuple[UserLocation]]) -> Select[tuple[UserLocation]]:
        stmt = stmt.join(UserLocation.user).join(UserLocation.location)
        if self.q:
            stmt = stmt.where(
                or_(
                    User.username.ilike(f"%{self.q}%"),
                    Location.name.ilike(f"%{self.q}%"),
                )
            )
        else:
            if self.user_id:
                stmt = stmt.where(User.id == self.user_id)
            if self.username:
                stmt = stmt.where(func.lower(User.username) == self.username)
            if self.location_id:
                stmt = stmt.where(Location.id == self.location_id)
            if self.location_name:
                stmt = stmt.where(func.lower(Location.name) == self.location_name)

        stmt = stmt.order_by(self.order_by)
        if self.limit > 0:
            stmt = stmt.limit(self.limit)
        stmt = stmt.offset(self.offset)

        return stmt


UserLocationQueryFilters = Annotated[UserLocationQueryParams, Query()]
