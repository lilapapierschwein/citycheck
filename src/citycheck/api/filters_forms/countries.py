from typing import Annotated, Literal, override

from fastapi import Query
from sqlalchemy import Select, func
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.sql import or_
from sqlalchemy.sql.elements import UnaryExpression

from citycheck.db.models import (
    Continent,
    Country,
    Currency,
    Language,
    Region,
    Subregion,
)

from .query_params import LowercaseStr, QueryParams


class CountryQueryParams(QueryParams):
    orderBy: Literal[
        "id",
        "name",
        "official_name",
        "code",
        "region",
        "subregion",
    ] = "id"
    name: LowercaseStr | None = None
    official_name: LowercaseStr | None = None
    code: LowercaseStr | None = None
    currency: LowercaseStr | None = None
    language: LowercaseStr | None = None
    region: LowercaseStr | None = None
    subregion: LowercaseStr | None = None
    continent: LowercaseStr | None = None
    q: LowercaseStr | None = None

    @override
    def __str__(self) -> str:
        return "CountryQueryParams"

    @override
    def __repr__(self) -> str:
        return (
            "CountryQueryParams("
            f"orderBy={repr(self.orderBy)}, "
            f"name={repr(self.name)}, "
            f"official_name={repr(self.official_name)}, "
            f"code={repr(self.code)}, "
            f"currency={repr(self.currency)}, "
            f"language={repr(self.language)}, "
            f"region={repr(self.region)}, "
            f"subregion={repr(self.subregion)}, "
            f"continent={repr(self.continent)}, "
            f"q={repr(self.q)}"
            ")"
        )

    @property
    def order_by(
        self,
    ) -> UnaryExpression[InstrumentedAttribute[Country]] | InstrumentedAttribute[Country]:
        """Returns the SQLAlchemy order_by expression based on the orderBy and sort parameters."""
        return (
            getattr(Country, self._order_col).asc() if self.sort == "asc" else getattr(Country, self._order_col).desc()
        )

    def apply(self, stmt: Select[tuple[Country]]) -> Select[tuple[Country]]:
        if self.q:
            stmt = stmt.where(
                or_(
                    Country.name.ilike(f"%{self.q}%"),
                    Country.official_name.ilike(f"%{self.q}%"),
                    Country.code.ilike(f"%{self.q}%"),
                )
            )
        elif self.name:
            stmt = stmt.where(func.lower(Country.name) == self.name)

        if self.code:
            stmt = stmt.where(func.lower(Country.code) == self.code)
        if self.currency:
            stmt = stmt.where(
                or_(
                    Country.currencies.any(func.lower(Currency.name) == self.currency),
                    Country.currencies.any(func.lower(Currency.code) == self.currency),
                )
            )
        if self.language:
            stmt = stmt.where(Country.languages.any(func.lower(Language.name) == self.language))
        if self.continent:
            stmt = stmt.where(Country.continents.any(func.lower(Continent.name) == self.continent))
        if self.subregion or self.region:
            stmt = stmt.join(Subregion)
        if self.subregion:
            stmt = stmt.where(func.lower(Subregion.name) == self.subregion)
        if self.region:
            stmt = stmt.join(Region).where(func.lower(Region.name) == self.region)

        stmt = stmt.order_by(self.order_by)
        if self.limit > 0:
            stmt = stmt.limit(self.limit)
        stmt = stmt.offset(self.offset)

        return stmt


CountryQueryFilters = Annotated[CountryQueryParams, Query()]
