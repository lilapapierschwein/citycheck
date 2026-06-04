from typing import Annotated, ClassVar, override
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
)

from .country import CountryModel


def validate_timezone(name: object) -> ZoneInfo:
    try:
        if not isinstance(name, str):
            raise TypeError(f"Timezone must of type a `string`, not {type(name)}")
        zone = ZoneInfo(name)
    except ZoneInfoNotFoundError as err:
        raise ZoneInfoNotFoundError(str(err)) from err
    except TypeError as err:
        raise TypeError(str(err)) from err
    return zone


TimeZone = Annotated[ZoneInfo, BeforeValidator(validate_timezone)]


class BaseLocation(BaseModel):
    name: str
    latitude: float
    longitude: float
    elevation: float
    population: int
    timezone: TimeZone
    country_id: int

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return (
            "BaseLocation("
            f"name={repr(self.name)}, "
            f"latitude={repr(self.latitude)}, "
            f"longitude={repr(self.longitude)}, "
            f"elevation={repr(self.elevation)}, "
            f"population={repr(self.population)}, "
            f"timezone={repr(self.timezone)}, "
            f"country_id={repr(self.country_id)}"
            ")"
        )


class LocationModel(BaseLocation):
    id: int
    country: CountryModel

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.name}("
            f"id={repr(self.id)}, "
            f"name={repr(self.name)}, "
            f"latitude={repr(self.latitude)}, "
            f"longitude={repr(self.longitude)}, "
            f"elevation={repr(self.elevation)}, "
            f"population={repr(self.population)}, "
            f"timezone={repr(self.timezone)}, "
            f"country_id={repr(self.country_id)}"
            ")"
        )


class LocationSchema(LocationModel): ...
