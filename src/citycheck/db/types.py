from datetime import datetime as dt
from typing import Any, override
from zoneinfo import ZoneInfo

from sqlalchemy.engine import Dialect
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.types import TypeDecorator, TypeEngine


class DateTimeType(TypeDecorator[dt]):
    """Custom type subclassing `:class:sqlalchemy.types.String` to allow for
    smoother interaction between `:class:datetime.datetime` and sqlite's VARCHAR.
    """

    impl: TypeEngine[Any] | type[TypeEngine[Any]] = String
    cache_ok: bool | None = True

    @override
    def process_bind_param(self, value: object, dialect: Dialect) -> str | object:
        if isinstance(value, dt):
            return value.isoformat()
        return value

    @override
    def process_result_value(self, value: str | None, dialect: Dialect) -> dt | None:
        if value is not None:
            return dt.fromisoformat(value)
        return value


class ZoneInfoType(TypeDecorator[ZoneInfo]):
    """Custom type subclassing `:class:sqlalchemy.types.String` to allow for
    smoother interaction between `:class:zoneinfo.ZoneInfo` and sqlite's VARCHAR.
    """

    impl: TypeEngine[Any] | type[TypeEngine[Any]] = String
    cache_ok: bool | None = True

    @override
    def process_bind_param(self, value: object, dialect: Dialect) -> str | object:
        if isinstance(value, ZoneInfo):
            return value.key
        return value

    @override
    def process_result_value(
        self, value: str | None, dialect: Dialect
    ) -> ZoneInfo | None:
        if value is not None:
            return ZoneInfo(value)
        return value
