from typing import Annotated, Literal, override

from fastapi import Query
from sqlalchemy import Select, UnaryExpression, func
from sqlalchemy.orm import InstrumentedAttribute, joinedload
from sqlalchemy.sql import or_

from citycheck.db.models import (
    Region,
    Subregion,
)

from .query_params import LowercaseStr, QueryParams


class RegionQueryParams(QueryParams):
    orderBy: Literal["id", "name"] = "id"
    name: LowercaseStr | None = None
    q: LowercaseStr | None = None

    @override
    def __str__(self) -> str:
        return "RegionQueryParams"

    @override
    def __repr__(self) -> str:
        return (
            "RegionQueryParams("
            f"orderBy={repr(self.orderBy)}, "
            f"name={repr(self.name)}"
            f"q={repr(self.q)}"
            ")"
        )

    @property
    def order_by(
        self,
    ) -> UnaryExpression[InstrumentedAttribute[Region]] | InstrumentedAttribute[Region]:
        """Returns the SQLAlchemy order_by expression based on the orderBy and sort parameters."""
        return (
            getattr(Region, self._order_col).asc()
            if self.sort == "asc"
            else getattr(Region, self._order_col).desc()
        )

    def apply(self, stmt: Select[tuple[Region]]) -> Select[tuple[Region]]:
        if self.q:
            stmt = stmt.where(Region.name.ilike(f"%{self.q}%"))
        elif self.name:
            stmt = stmt.where(func.lower(Region.name) == self.name)

        stmt = stmt.order_by(self.order_by)
        if self.limit > 0:
            stmt = stmt.limit(self.limit)
        stmt = stmt.offset(self.offset)

        return stmt


RegionQueryFilters = Annotated[RegionQueryParams, Query()]


class SubregionQueryParams(QueryParams):
    orderBy: Literal["id", "name"] = "id"
    name: LowercaseStr | None = None
    region: LowercaseStr | None = None
    q: LowercaseStr | None = None

    @override
    def __str__(self) -> str:
        return "SubregionQueryParams"

    @override
    def __repr__(self) -> str:
        return (
            "SubregionQueryParams("
            f"orderBy={repr(self.orderBy)}, "
            f"name={repr(self.name)}, "
            f"region={repr(self.region)}, "
            f"q={repr(self.q)}"
            ")"
        )

    @property
    def order_by(
        self,
    ) -> (
        UnaryExpression[InstrumentedAttribute[Subregion]]
        | InstrumentedAttribute[Subregion]
    ):
        """Returns the SQLAlchemy order_by expression based on the orderBy and sort parameters."""
        return (
            getattr(Subregion, self._order_col).asc()
            if self.sort == "asc"
            else getattr(Subregion, self._order_col).desc()
        )

    def apply(self, stmt: Select[tuple[Subregion]]) -> Select[tuple[Subregion]]:
        stmt = stmt.join(Subregion.region)
        if self.q:
            stmt = stmt.where(
                or_(
                    Subregion.name.ilike(f"%{self.q}%"),
                    Region.name.ilike(f"%{self.q}%"),
                )
            )
        else:
            if self.name:
                stmt = stmt.where(func.lower(Subregion.name) == self.name)
            if self.region:
                stmt = stmt.where(func.lower(Region.name) == self.region)

        stmt = stmt.order_by(self.order_by)
        if self.limit > 0:
            stmt = stmt.limit(self.limit)
        stmt = stmt.offset(self.offset)

        return stmt.options(joinedload(Subregion.region))


SubregionQueryFilters = Annotated[SubregionQueryParams, Query()]
