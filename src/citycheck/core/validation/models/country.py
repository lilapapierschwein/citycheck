from typing import ClassVar, override

from pydantic import BaseModel, ConfigDict

from .region import SubregionModel


class CountryCreate(BaseModel):
    name: str
    official_name: str
    code: str
    flag: str
    area: float
    population: int
    tld: str
    googlemaps: str
    openstreetmaps: str
    subregion_id: int

    @override
    def __str__(self) -> str:
        return f"{self.name} {self.flag}"

    @override
    def __repr__(self) -> str:
        return (
            "CountryCreate("
            f"name={repr(self.name)}, "
            f"official_name={repr(self.official_name)}, "
            f"code={repr(self.code)}, "
            f"flag={repr(self.flag)}, "
            f"area={repr(self.area)}, "
            f"population={repr(self.population)}, "
            f"tld={repr(self.tld)}, "
            f"googlemaps={repr(self.googlemaps)}, "
            f"openstreetmaps={repr(self.openstreetmaps)}, "
            f"subregion_id={repr(self.subregion_id)}"
            ")"
        )


class CountryModel(BaseModel):
    id: int
    name: str
    official_name: str
    code: str
    flag: str
    area: float
    population: int
    tld: str
    googlemaps: str
    openstreetmaps: str
    subregion_id: int
    subregion: SubregionModel

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)

    @override
    def __str__(self) -> str:
        return f"{self.name} {self.flag}"

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"name={repr(self.name)}, "
            f"official_name={repr(self.official_name)}, "
            f"code={repr(self.code)}, "
            f"flag={repr(self.flag)}, "
            f"area={repr(self.area)}, "
            f"population={repr(self.population)}, "
            f"tld={repr(self.tld)}, "
            f"googlemaps={repr(self.googlemaps)}, "
            f"openstreetmaps={repr(self.openstreetmaps)}, "
            f"subregion_id={repr(self.subregion_id)}"
            ")"
        )


class CountrySchema(CountryModel): ...
