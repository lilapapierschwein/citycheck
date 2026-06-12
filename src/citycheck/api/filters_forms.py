from typing import Annotated, Literal

from fastapi import Query
from pydantic import BaseModel, Field


class QueryParams(BaseModel):
    limit: int = Field(default=100, gt=0, le=100)
    offset: int = Field(default=0, ge=0)
    sort: Literal["asc", "desc"] = "asc"


class CountryQueryParams(QueryParams):
    orderBy: Literal[
        "countryId",
        "name",
        "officialName",
        "code",
        "currency",
        "language",
        "region",
        "subregion",
    ] = "countryId"
    name: str | None = None
    code: str | None = None
    currency: str | None = None
    language: str | None = None
    region: str | None = None
    subregion: str | None = None


CountryQueryFilters = Annotated[CountryQueryParams, Query()]
