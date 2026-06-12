from typing import ClassVar, override

from pydantic import BaseModel, ConfigDict, computed_field, model_serializer

from citycheck.api.models.currency import CurrencyModel
from citycheck.api.models.language import LanguageModel

from .region import RegionModel, SubregionSchema


class CountryCreate(BaseModel):
    name: str
    official_name: str
    code: str
    flag: str
    area: float
    population: int
    currency_id: int
    language_id: int
    tld: str
    googlemaps: str
    openstreetmaps: str
    subregion_id: int | None

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
    currency_id: int
    currency: CurrencyModel
    language_id: int
    language: LanguageModel
    tld: str
    googlemaps: str
    openstreetmaps: str
    subregion_id: int | None
    subregion: SubregionSchema | None

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
            f"currency_id={repr(self.currency_id)}, "
            f"language={repr(self.language_id)}, "
            f"tld={repr(self.tld)}, "
            f"googlemaps={repr(self.googlemaps)}, "
            f"openstreetmaps={repr(self.openstreetmaps)}, "
            f"subregion_id={repr(self.subregion_id)}"
            ")"
        )

    @computed_field
    @property
    def region(self) -> RegionModel | None:
        if self.subregion is None:
            return None
        return self.subregion.region


class CountrySchema(CountryModel):
    @model_serializer
    def serialize_model(self):
        return {
            "id": self.id,
            "name": self.name,
            "official_name": self.official_name,
            "code": self.code,
            "flag": self.flag,
            "area": self.area,
            "population": self.population,
            "currency": self.currency,
            "language": self.language,
            "tld": self.tld,
            "googlemaps": self.googlemaps,
            "openstreetmaps": self.openstreetmaps,
            "subregion": self.subregion,
        }
