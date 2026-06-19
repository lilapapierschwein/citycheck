import re
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, Field, PrivateAttr


class QueryParams(BaseModel):
    """Parent class for query params of all endpoints. Contains common params
    like pagination and sorting."""

    limit: int = Field(default=100, ge=0, le=100)
    offset: int = Field(default=0, ge=0)
    sort: Literal["asc", "desc"] = "asc"

    _order_col: str = PrivateAttr(
        default_factory=lambda data: re.sub(
            # we have to replace uppercase characterss with their lowercase
            # pendant prefixed by "_" to match the actual column name
            r"([A-Z])",
            lambda m: f"_{m.group(1).lower()}",
            data.get("orderBy", "id"),
        )
    )


def validate_str_to_lowercase(s: object) -> str:
    if not isinstance(s, str):
        raise ValueError(f"Value must be a string, not {type(s).__name__}: {s!r}")
    if not s.islower():
        return s.lower()
    return s


# Convenience type for string query params that should be converted to lowercase
LowercaseStr = Annotated[str, BeforeValidator(validate_str_to_lowercase)]
