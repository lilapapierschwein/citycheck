from typing import Annotated, Literal, override

from fastapi import Query
from sqlalchemy import Select, UnaryExpression, func
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import or_

from citycheck.db.models import (
    Currency,
)

from .query_params import LowercaseStr, QueryParams


class CurrencyQueryParams(QueryParams):
    orderBy: Literal["id", "code", "name", "symbol"] = "id"
    code: LowercaseStr | None = None
    name: LowercaseStr | None = None
    symbol: str | None = None
    q: LowercaseStr | None = None

    @override
    def __str__(self) -> str:
        return "CurrencyQueryParams"

    @override
    def __repr__(self) -> str:
        return (
            "CurrencyQueryParams("
            f"orderBy={repr(self.orderBy)}, "
            f"code={repr(self.code)}, "
            f"name={repr(self.name)}, "
            f"symbol={repr(self.symbol)}, "
            f"q={repr(self.q)}"
            ")"
        )

    @property
    def order_by(
        self,
    ) -> (
        UnaryExpression[InstrumentedAttribute[Currency]]
        | InstrumentedAttribute[Currency]
    ):
        """Returns the SQLAlchemy order_by expression based on the orderBy and sort parameters."""
        return (
            getattr(Currency, self._order_col).asc()
            if self.sort == "asc"
            else getattr(Currency, self._order_col).desc()
        )

    def apply(self, stmt: Select[tuple[Currency]]) -> Select[tuple[Currency]]:
        if self.q:
            stmt = stmt.where(
                or_(
                    Currency.name.ilike(f"%{self.q}%"),
                    Currency.code.ilike(f"%{self.q}%"),
                )
            )
            stmt = stmt.order_by(self.order_by)
            if self.limit > 0:
                stmt = stmt.limit(self.limit)
            stmt = stmt.offset(self.offset)
            return stmt

        if self.name:
            stmt = stmt.where(func.lower(Currency.name) == self.name)
        if self.code:
            stmt = stmt.where(func.lower(Currency.code) == self.code)
        if self.symbol:
            stmt = stmt.where(func.lower(Currency.symbol) == self.symbol)

        stmt = stmt.order_by(self.order_by)
        if self.limit > 0:
            stmt = stmt.limit(self.limit)
        stmt = stmt.offset(self.offset)

        return stmt


CurrencyQueryFilters = Annotated[CurrencyQueryParams, Query()]
