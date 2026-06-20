from dataclasses import dataclass
from typing import Any, ClassVar, TypedDict, override

from pydantic import BaseModel, ConfigDict, computed_field, model_serializer
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_, select

from citycheck.api.models.continent import ContinentModel
from citycheck.api.models.currency import CurrencyModel
from citycheck.api.models.language import LanguageModel
from citycheck.db.models import Continent, Currency, Language, Subregion

from .region import RegionModel, SubregionSchema

# {
#         "names": {
#           "common": "Afghanistan",
#           "official": "Islamic Republic of Afghanistan"
#         },
#         "codes": {
#           "alpha_2": "AF"
#         },
#         "flag": {
#           "emoji": "🇦🇫"
#         },
#         "region": "Asia",
#         "subregion": "Southern Asia",
#         "area": {
#           "kilometers": 652230
#         },
#         "continents": ["Asia"],
#         "currencies": [
#           {
#             "code": "AFN",
#             "name": "Afghan afghani",
#             "symbol": "؋"
#           }
#         ],
#         "languages": [
#           {
#             "name": "Dari"
#           },
#           {
#             "name": "Pashto"
#           },
#           {
#             "name": "Turkmen"
#           }
#         ],
#         "links": {
#           "google_maps": "https://goo.gl/maps/BXBGw7yUUFknCfva9",
#           "open_street_maps": "https://www.openstreetmap.org/relation/303427"
#         },
#         "population": 35000000,
#         "tlds": [".af"],
#         "_meta": {
#           "lastUpdatedTimestamp": 1781804763
#         }
#       }


@dataclass
class CountryNames:
    common: str
    official: str


@dataclass
class CountryCodes:
    alpha_2: str


@dataclass
class CountryFlag:
    emoji: str


@dataclass
class CountryArea:
    kilometers: float


@dataclass
class CountryCurrency:
    code: str
    name: str
    symbol: str

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "name": self.name,
            "symbol": self.symbol,
        }


@dataclass
class CountryLanguage:
    name: str


@dataclass
class CountryLinks:
    google_maps: str
    open_street_maps: str


class CountryNameAndCode(TypedDict):
    name: str
    code: str


class CountryJunctions(TypedDict):
    country: CountryNameAndCode
    subregion_id: int
    continents_ids: list[int]
    currencies_ids: list[int]
    languages_ids: list[int]


class CountryIn(BaseModel):
    names: CountryNames
    codes: CountryCodes
    flag: CountryFlag
    region: str
    subregion: str
    area: CountryArea
    continents: list[str]
    currencies: list[CountryCurrency]
    languages: list[CountryLanguage]
    links: CountryLinks
    population: int
    tlds: list[str]
    subregion_id: int | None = None
    currency_ids: list[int] | None = None
    continent_ids: list[int] | None = None
    languages_ids: list[int] | None = None

    @override
    def model_post_init(self, context: Any, /) -> None:
        if not self.subregion and self.region == "Antarctic":
            self.subregion = self.region

    @model_serializer
    def serialize_model(self):
        return {
            "name": self.names.common,
            "official_name": self.names.official,
            "code": self.codes.alpha_2,
            "flag": self.flag.emoji,
            "subregion": self.subregion,
            "area_sqkm": self.area.kilometers,
            "continents": self.continents,
            "currencies": [curr.as_dict() for curr in self.currencies],
            "currency_ids": self.currency_ids,
            "languages": [lang.name for lang in self.languages],
            "googlemaps": self.links.google_maps,
            "openstreetmaps": self.links.open_street_maps,
            "population": self.population,
            "tld": self.tlds[0] if self.tlds else "",
            "subregion_id": self.subregion_id,
            "continent_ids": self.continent_ids,
            "languages_ids": self.languages_ids,
        }

    def get_junctions(self, session: Session) -> CountryJunctions:
        return CountryJunctions(
            country=CountryNameAndCode(name=self.names.common, code=self.codes.alpha_2),
            subregion_id=self.get_subregion_id(session),
            continents_ids=self.get_continents_ids(session),
            currencies_ids=self.get_currencies_ids(session),
            languages_ids=self.get_languages_ids(session),
        )

    def get_subregion_id(self, session: Session) -> int:
        if self.subregion == "":
            # think about the arctic!
            self.subregion = self.region

        self.subregion_id = session.scalar(
            select(Subregion.id).where(Subregion.name == self.subregion)
        )
        if not self.subregion_id:
            raise LookupError(f"subregion id missing ({self.subregion!r})")
        return self.subregion_id

    def get_continents_ids(self, session: Session):
        self.continent_ids = list(
            session.scalars(select(Continent.id).where(Continent.name.in_(self.continents))).all()
        )
        return self.continent_ids

    def get_currencies_ids(self, session: Session):
        self.currency_ids = (
            list(
                session.scalars(
                    select(Currency.id).where(
                        or_(
                            Currency.name.in_(curr.name for curr in self.currencies),
                            Currency.code.in_(curr.code for curr in self.currencies),
                        )
                    )
                ).all()
            )
            if self.currencies
            else []
        )
        return self.currency_ids

    def get_languages_ids(self, session: Session):
        self.languages_ids = (
            list(
                session.scalars(
                    select(Language.id).where(
                        Language.name.in_(lang.name for lang in self.languages)
                    )
                ).all()
            )
            if self.languages
            else []
        )
        return self.languages_ids


class CountryCreate(BaseModel):
    name: str
    official_name: str
    code: str
    flag: str
    area_sqkm: float
    population: int
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
            f"area_sqkm={repr(self.area_sqkm)}, "
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
    area_sqkm: float
    population: int
    tld: str
    googlemaps: str
    openstreetmaps: str
    subregion_id: int | None
    subregion: SubregionSchema | None

    continents: list[ContinentModel]
    currencies: list[CurrencyModel]
    languages: list[LanguageModel]

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
            f"area_sqkm={repr(self.area_sqkm)}, "
            f"population={repr(self.population)}, "
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
            "area_sqkm": self.area_sqkm,
            "population": self.population,
            "tld": self.tld,
            "googlemaps": self.googlemaps,
            "openstreetmaps": self.openstreetmaps,
            "regions": {"region": self.region, "subregion": self.subregion},
            "continents": self.continents,
            "currencies": self.currencies,
            "languages": self.languages,
        }
