from typing import Annotated, ClassVar, override
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    model_serializer,
)

from .country import CountrySchema


def validate_timezone(name: object) -> ZoneInfo:
    try:
        if not isinstance(name, (str, ZoneInfo)):
            raise TypeError(
                f"Timezone must of type `string` or `ZoneInfo`, not {type(name)}"
            )
        if isinstance(name, str):
            return ZoneInfo(name)
        return name
    except ZoneInfoNotFoundError as err:
        raise ZoneInfoNotFoundError(str(err)) from err
    except TypeError as err:
        raise TypeError(str(err)) from err


TimeZone = Annotated[ZoneInfo, BeforeValidator(validate_timezone)]


class LocationCreate(BaseModel):
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
            "LocationCreate("
            f"name={repr(self.name)}, "
            f"latitude={repr(self.latitude)}, "
            f"longitude={repr(self.longitude)}, "
            f"elevation={repr(self.elevation)}, "
            f"population={repr(self.population)}, "
            f"timezone={repr(self.timezone)}, "
            f"country_id={repr(self.country_id)}"
            ")"
        )


class LocationModel(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    elevation: float
    population: int
    timezone: TimeZone
    country_id: int
    country: CountrySchema

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __str__(self) -> str:
        return self.name

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


class LocationSchema(LocationModel):
    @model_serializer
    def serialize_model(self):
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "elevation": self.elevation,
            "population": self.population,
            "timezone": str(self.timezone),
            "country": self.country,
        }
