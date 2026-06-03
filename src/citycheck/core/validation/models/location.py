from typing import Annotated, ClassVar, override
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import AfterValidator, BaseModel, ConfigDict


def validate_timezone(name: str) -> ZoneInfo:
    try:
        zone = ZoneInfo(name)
    except ZoneInfoNotFoundError as err:
        raise ValueError(str(err)) from err
    return zone


TimeZone = Annotated[ZoneInfo, AfterValidator(validate_timezone)]


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


class LocationModel(BaseLocation):
    id: int
    # country: CountryModel

    medel_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class LocationSchema(LocationModel): ...
