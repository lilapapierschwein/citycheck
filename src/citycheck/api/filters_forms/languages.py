from typing import Annotated, Literal, override

from fastapi import Query
from sqlalchemy import Select, UnaryExpression, func
from sqlalchemy.orm import InstrumentedAttribute

from citycheck.db.models import (
    Language,
)

from .query_params import LowercaseStr, QueryParams


class LanguageQueryParams(QueryParams):
    orderBy: Literal["id", "name"] = "id"
    name: LowercaseStr | None = None
    q: LowercaseStr | None = None

    @override
    def __str__(self) -> str:
        return "LanguageQueryParams"

    @override
    def __repr__(self) -> str:
        return (
            "LanguageQueryParams("
            f"orderBy={repr(self.orderBy)}, "
            f"name={repr(self.name)}"
            f"q={repr(self.q)}"
            ")"
        )

    @property
    def order_by(
        self,
    ) -> (
        UnaryExpression[InstrumentedAttribute[Language]]
        | InstrumentedAttribute[Language]
    ):
        """Returns the SQLAlchemy order_by expression based on the orderBy and sort parameters."""
        return (
            getattr(Language, self._order_col).asc()
            if self.sort == "asc"
            else getattr(Language, self._order_col).desc()
        )

    def apply(self, stmt: Select[tuple[Language]]) -> Select[tuple[Language]]:
        if self.q:
            stmt = stmt.where(Language.name.ilike(f"%{self.q}%"))
        elif self.name:
            stmt = stmt.where(func.lower(Language.name) == self.name)

        stmt = stmt.order_by(self.order_by)
        if self.limit > 0:
            stmt = stmt.limit(self.limit)
        stmt = stmt.offset(self.offset)

        return stmt


LanguageQueryFilters = Annotated[LanguageQueryParams, Query()]
