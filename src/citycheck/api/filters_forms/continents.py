from typing import Annotated, Literal, override

from fastapi import Query
from sqlalchemy import Select, func
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql.elements import UnaryExpression

from citycheck.db.models import (
    Continent,
)

from .query_params import LowercaseStr, QueryParams


class ContinentQueryParams(QueryParams):
    orderBy: Literal[
        "id",
        "name",
    ] = "id"
    name: LowercaseStr | None = None
    q: LowercaseStr | None = None

    @override
    def __str__(self) -> str:
        return "ContinentQueryParams"

    @override
    def __repr__(self) -> str:
        return (
            "CountryQueryParams("
            f"orderBy={repr(self.orderBy)}, "
            f"name={repr(self.name)}, "
            f"q={repr(self.q)}"
            ")"
        )

    @property
    def order_by(
        self,
    ) -> (
        UnaryExpression[InstrumentedAttribute[Continent]]
        | InstrumentedAttribute[Continent]
    ):
        """Returns the SQLAlchemy order_by expression based on the orderBy and sort parameters."""
        return (
            getattr(Continent, self._order_col).asc()
            if self.sort == "asc"
            else getattr(Continent, self._order_col).desc()
        )

    def apply(self, stmt: Select[tuple[Continent]]) -> Select[tuple[Continent]]:
        if self.q:
            stmt = stmt.where(Continent.name.ilike(f"%{self.q}%"))
        elif self.name:
            stmt = stmt.where(func.lower(Continent.name) == self.name)

        stmt = stmt.order_by(self.order_by)
        if self.limit > 0:
            stmt = stmt.limit(self.limit)
        stmt = stmt.offset(self.offset)

        return stmt


ContinentQueryFilters = Annotated[ContinentQueryParams, Query()]
