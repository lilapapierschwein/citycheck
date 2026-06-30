from datetime import datetime as dt
from typing import final, override
from zoneinfo import ZoneInfo

from sqlalchemy import Column, Table, func, sql
from sqlalchemy.dialects.sqlite import BOOLEAN, INTEGER, REAL, TEXT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey

from citycheck.core.utils import get_current_datetime
from citycheck.db.types import DateTimeType, ZoneInfoType


class Base(DeclarativeBase): ...


@final
class User(Base):
    """Represents a user of the application.

    Attributes:
        id (`int`): The unique identifier of the user.
        username (`str`): The username of the user.
        email (`str`): The email address of the user.
        is_disabled (`bool`): ...
        is_deleted (`bool`): ...
        home_location_id (`int | None`): The foreign key referencing the user's home location.

    Relationships:
        home_location (`Location | None`): The relationship to the user's home location.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column("user_id", INTEGER, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column("username", VARCHAR(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column("email", VARCHAR(255), nullable=False)
    is_disabled: Mapped[bool] = mapped_column(
        "is_disabled",
        BOOLEAN,
        default=False,
        server_default=sql.text("0"),
        nullable=False,
    )
    is_deleted: Mapped[bool] = mapped_column(
        "is_deleted",
        BOOLEAN,
        default=False,
        server_default=sql.text("0"),
        nullable=False,
    )
    home_location_id: Mapped[int | None] = mapped_column(
        "home_location_id",
        INTEGER,
        ForeignKey("locations.location_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        default=None,
        server_default=sql.text("null"),
    )
    home_location: Mapped[Location | None] = relationship(back_populates="users_homes")
    user_locations: Mapped[list[UserLocation]] = relationship(back_populates="user")
    passwords_hashes: Mapped[list[UserPassword]] = relationship(back_populates="user")
    activities: Mapped[list[UserActivity]] = relationship(back_populates="user")

    @override
    def __str__(self) -> str:
        return self.username

    @override
    def __repr__(self) -> str:
        return (
            "User("
            f"id={repr(self.id)}, "
            f"username={repr(self.username)}, "
            f"email={repr(self.email)}, "
            f"is_disabled={repr(self.is_disabled)}, "
            f"is_deleted={repr(self.is_deleted)}, "
            f"home_location_id={repr(self.home_location_id)}"
            ")"
        )

    @property
    def is_active(self) -> bool:
        return not self.is_disabled and not self.is_deleted

    @property
    def locations(self) -> list[Location]:
        return [loc.location for loc in self.user_locations]

    @property
    def favorites(self) -> list[Location]:
        return [loc.location for loc in self.user_locations if loc.is_favorite]

    @property
    def current_password(self) -> str:
        passwd_hashes_active = [upw.password_hash for upw in self.passwords_hashes if upw.is_valid]
        if not passwd_hashes_active:
            raise LookupError(f"No valid password found for user#{self.id}")
        elif len(passwd_hashes_active) > 1:
            raise LookupError(
                f"Too many valid passwords found for user#{self.id} ({len(passwd_hashes_active)})"
            )
        return passwd_hashes_active[0]


country_continent = Table(
    "countries_continents",
    Base.metadata,
    Column("country_id", ForeignKey("countries.country_id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
    Column("continent_id", ForeignKey("continents.continent_id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
)

country_currency = Table(
    "countries_currencies",
    Base.metadata,
    Column("country_id", ForeignKey("countries.country_id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
    Column("currency_id", ForeignKey("currencies.currency_id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
)

country_language = Table(
    "countries_languages",
    Base.metadata,
    Column("country_id", ForeignKey("countries.country_id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
    Column("language_id", ForeignKey("languages.language_id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
)


@final
class Activity(Base):
    """Represents and activity

    Attributes:
        id (`int`): The unique identifier of the activity.
        name (`str`): The name of the activity.
    """

    __tablename__ = "activities"

    id: Mapped[int] = mapped_column("activity_id", INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)

    entries: Mapped[list[UserActivity]] = relationship(back_populates="activity")

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"Activity(id={repr(self.id)}, name={repr(self.name)})"


@final
class UserActivity(Base):
    __tablename__ = "users_activities"

    id: Mapped[int] = mapped_column(
        "user_activity_id", INTEGER, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int | None] = mapped_column(
        "user_id",
        INTEGER,
        ForeignKey(
            "users.user_id",
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        nullable=True,
    )
    user: Mapped[User] = relationship(back_populates="activities")

    activity_id: Mapped[int] = mapped_column(
        "activity_id",
        INTEGER,
        ForeignKey(
            "activities.activity_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    activity: Mapped[Activity] = relationship(back_populates="entries")

    timestamp: Mapped[dt] = mapped_column(
        "timestamp",
        DateTimeType,
        default=get_current_datetime(),
        server_default=func.current_timestamp(),
        nullable=False,
    )

    @override
    def __str__(self) -> str:
        return f"{self.activity.name} ({self.user.username}) @{self.timestamp}"

    @override
    def __repr__(self) -> str:
        return (
            "UserActivity("
            f"id={repr(self.id)}, "
            f"user_id={repr(self.user_id)}, "
            f"activity_id={repr(self.activity_id)}, "
            f"timestamp={repr(self.timestamp)}"
            ")"
        )


@final
class Continent(Base):
    """Represents a continent.

    Attributes:
        id (`int`): The unique identifier of the continent.
        name (`str`): The name of the continent.
    """

    __tablename__ = "continents"

    id: Mapped[int] = mapped_column("continent_id", INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)

    countries: Mapped[list[Country]] = relationship(
        secondary=country_continent, back_populates="continents"
    )

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"Continent(id={repr(self.id)}, name={repr(self.name)})"


@final
class Region(Base):
    """Represents a region.

    Attributes:
        id (`int`): The unique identifier of the region.
        name (`str`): The name of the region.

    Relationships:
        subregions (list[`:class:Subregion`]): The list of subregions into which
                                      this region is divided.
    """

    __tablename__ = "regions"

    id: Mapped[int] = mapped_column("region_id", INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)
    subregions: Mapped[list[Subregion]] = relationship(back_populates="region")

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"Region(id={repr(self.id)}, name={repr(self.name)})"

    def get_countries(self) -> list[Country]:
        return [country for subregion in self.subregions for country in subregion.countries]


@final
class Subregion(Base):
    """Represents a subregion.

    Attributes:
        id (`int`): The unique identifier of the subregion.
        name (`str`): The name of the subregion.
        region_id (`int`): The foreign key referencing the parent region.

    Relationships:
        region (`:class:Region`): The relationship to the parent region.
        countries (list[`:class:Country`]): The list of countries in this subregion.
    """

    __tablename__ = "subregions"

    id: Mapped[int] = mapped_column("subregion_id", INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)
    region_id: Mapped[int] = mapped_column(
        "region_id",
        INTEGER,
        ForeignKey("regions.region_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    region: Mapped[Region] = relationship(back_populates="subregions")
    countries: Mapped[list[Country]] = relationship(back_populates="subregion")

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"Subregion(id={repr(self.id)}, name={repr(self.name)}, region_id={repr(self.region_id)})"


@final
class Language(Base):
    """Represents a language.

    Attributes:
        id (`int`): The unique identifier of the language.
        name (`str`): The name of the language.

    Relationships:
        countries (list[`:class:Country`]): The list of countries that speak this language.
    """

    __tablename__ = "languages"

    id: Mapped[int] = mapped_column("language_id", INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)

    countries: Mapped[list[Country]] = relationship(
        secondary=country_language, back_populates="languages"
    )

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"Language(id={repr(self.id)}, name={repr(self.name)})"


@final
class Currency(Base):
    """Represents a currency.

    Attributes:
        id (`int`): The unique identifier of the currency.
        code (`str`): The ISO 4217 code of the currency.
        name (`str`): The name of the currency.
        symbol (`str`): The symbol of the currency.

    Relationships:
        countries (list[`:class:Country`]): The list of countries that use this currency.
    """

    __tablename__ = "currencies"

    id: Mapped[int] = mapped_column("currency_id", INTEGER, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column("code", VARCHAR(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)
    symbol: Mapped[str] = mapped_column("symbol", VARCHAR(10), nullable=False)

    countries: Mapped[list[Country]] = relationship(
        secondary=country_currency, back_populates="currencies"
    )

    @override
    def __str__(self) -> str:
        return f"{self.symbol} ({self.name}, {self.code})"

    @override
    def __repr__(self) -> str:
        return f"Currency(id={repr(self.id)}, name={repr(self.name)}, symbol={repr(self.symbol)})"


@final
class Country(Base):
    """Represents a country.

    Attributes:
        id (`int`): The unique identifier of the country.
        name (`str`): The common name of the country.
        official_name (`str`): The official name of the country.
        code (`str`): The ISO 3166-1 alpha-2 code of the country.
        area_sqkm (`float`): The total area of the country in square kilometers.
        tld (`str`): The top-level domain of the country.
        flag (`str`): The emoji flag of the country.
        population (`int`): The population of the country.
        currency_id (`int`): The foreign key referencing the country's currency.
        googlemaps (`str`): The URL to the country's location on Google Maps.
        openstreetmaps (`str`): The URL to the country's location on OpenStreetMap.
        subregion_id (`int | None`): The foreign key referencing the country's subregion.

    Relationships:
        currency (`:class:Currency`): The relationship to the country's currency.
        language (`:class:Language`): The relationship to the country's primary language.
        subregion (`:class:Subregion | None`): The relationship to the country's subregion.
        locations (list[`:class:Location`]): The list of locations stored for this country.
    """

    __tablename__ = "countries"

    id: Mapped[int] = mapped_column("country_id", INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)
    official_name: Mapped[str] = mapped_column(
        "official_name", VARCHAR(255), unique=True, nullable=False
    )
    code: Mapped[str] = mapped_column("code", VARCHAR(2), nullable=False)
    area_sqkm: Mapped[float] = mapped_column("area", REAL, nullable=False)
    tld: Mapped[str] = mapped_column("tld", VARCHAR(10), nullable=False)
    flag: Mapped[str] = mapped_column("flag", VARCHAR(10), nullable=False)
    population: Mapped[int] = mapped_column("population", INTEGER, nullable=False)
    googlemaps: Mapped[str] = mapped_column("googlemaps", TEXT, nullable=False)
    openstreetmaps: Mapped[str] = mapped_column("openstreetmaps", TEXT, nullable=False)
    subregion_id: Mapped[int | None] = mapped_column(
        "subregion_id",
        INTEGER,
        ForeignKey("subregions.subregion_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
        default=None,
        server_default=sql.text("null"),
    )
    subregion: Mapped[Subregion] = relationship(back_populates="countries")
    locations: Mapped[list[Location]] = relationship(back_populates="country")

    continents: Mapped[list[Continent]] = relationship(
        secondary=country_continent, back_populates="countries"
    )
    currencies: Mapped[list[Currency]] = relationship(
        secondary=country_currency, back_populates="countries"
    )
    languages: Mapped[list[Language]] = relationship(
        secondary=country_language, back_populates="countries"
    )

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return (
            "Country("
            f"id={repr(self.id)}, "
            f"name={repr(self.name)}, "
            f"official_name={repr(self.official_name)}, "
            f"code={repr(self.code)}, "
            f"tld={repr(self.tld)}, "
            f"flag={repr(self.flag)}, "
            f"population={repr(self.population)}, "
            f"googlemaps={repr(self.googlemaps)}, "
            f"openstreetmaps={repr(self.openstreetmaps)}, "
            f"subregion_id={repr(self.subregion_id)}"
            ")"
        )

    def get_region(self) -> Region:
        return self.subregion.region


# @final
# class CountryContinent(Base):
#     __tablename__ = "countries_continents"
#
#     id: Mapped[int] = mapped_column(
#         "country_continent_id", INTEGER, primary_key=True, autoincrement=True
#     )
#     country_id: Mapped[int] = mapped_column(
#         "country_id",
#         INTEGER,
#         ForeignKey(
#             "countries.country_id",
#             onupdate="CASCADE",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#     )
#     country: Mapped[Country] = relationship(back_populates="country_continents")
#
#     continent_id: Mapped[int] = mapped_column(
#         "continent_id",
#         INTEGER,
#         ForeignKey(
#             "continents.continent_id",
#             onupdate="CASCADE",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#     )
#     continent: Mapped[Continent] = relationship(back_populates="continent_countries")
#
#     is_favorite: Mapped[bool] = mapped_column(
#         "is_favorite",
#         BOOLEAN,
#         nullable=False,
#         default=False,
#         server_default=sql.text("0"),
#     )


# @final
# class CountryCurrency(Base):
#     __tablename__ = "countries_currencies"
#
#     id: Mapped[int] = mapped_column(
#         "country_currency_id", INTEGER, primary_key=True, autoincrement=True
#     )
#     country_id: Mapped[int] = mapped_column(
#         "country_id",
#         INTEGER,
#         ForeignKey(
#             "countries.country_id",
#             onupdate="CASCADE",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#     )
#     country: Mapped[Country] = relationship(back_populates="country_currencies")
#
#     currency_id: Mapped[int] = mapped_column(
#         "currency_id",
#         INTEGER,
#         ForeignKey(
#             "currencies.currency_id",
#             onupdate="CASCADE",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#     )
#     currency: Mapped[Currency] = relationship(back_populates="currency_countries")
#
#     is_favorite: Mapped[bool] = mapped_column(
#         "is_favorite",
#         BOOLEAN,
#         nullable=False,
#         default=False,
#         server_default=sql.text("0"),
#     )
#
#
# @final
# class CountryLanguage(Base):
#     __tablename__ = "countries_languages"
#
#     id: Mapped[int] = mapped_column(
#         "country_language_id", INTEGER, primary_key=True, autoincrement=True
#     )
#     country_id: Mapped[int] = mapped_column(
#         "country_id",
#         INTEGER,
#         ForeignKey(
#             "countries.country_id",
#             onupdate="CASCADE",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#     )
#     country: Mapped[Country] = relationship(back_populates="country_languages")
#
#     language_id: Mapped[int] = mapped_column(
#         "language_id",
#         INTEGER,
#         ForeignKey(
#             "languages.language_id",
#             onupdate="CASCADE",
#             ondelete="CASCADE",
#         ),
#         nullable=False,
#     )
#     language: Mapped[Language] = relationship(back_populates="language_countries")
#
#     is_favorite: Mapped[bool] = mapped_column(
#         "is_favorite",
#         BOOLEAN,
#         nullable=False,
#         default=False,
#         server_default=sql.text("0"),
#     )


@final
class Location(Base):
    """Represents a location stored by a user.

    Attributes:
        id (`int`): The unique identifier of the location.
        name (`str`): The name of the location.
        latitude (`float`): The latitude of the location.
        longitude (`float`): The longitude of the location.
        elevation (`float`): The elevation of the location in meters.
        population (`int`): The population of the location.
        timezone (`ZoneInfo`): The timezone of the location.
        country_id (`int`): The foreign key referencing the country of the location.

    Relationships:
        country (`:class:Country`): The relationship to the country of the location.
        users (list[`:class:User`]): The list of users who have this location stored.
    """

    __tablename__ = "locations"

    id: Mapped[int] = mapped_column("location_id", INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)
    latitude: Mapped[float] = mapped_column("latitude", REAL, nullable=False)
    longitude: Mapped[float] = mapped_column("longitude", REAL, nullable=False)
    elevation: Mapped[float] = mapped_column("elevation", REAL, nullable=False)
    population: Mapped[int] = mapped_column("population", INTEGER, nullable=False)
    timezone: Mapped[ZoneInfo] = mapped_column(
        "timezone",
        ZoneInfoType(255),
        nullable=False,
        default=ZoneInfo("UTC"),
        server_default=sql.text("UTC"),
    )
    country_id: Mapped[int] = mapped_column(
        "country_id",
        INTEGER,
        ForeignKey(
            "countries.country_id",
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )
    country: Mapped[Country] = relationship(back_populates="locations")
    users_homes: Mapped[list[User]] = relationship(back_populates="home_location")
    users_locations: Mapped[list[UserLocation]] = relationship(back_populates="location")

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return (
            "User("
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


@final
class UserLocation(Base):
    __tablename__ = "users_locations"

    id: Mapped[int] = mapped_column(
        "user_location_id", INTEGER, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        "user_id",
        INTEGER,
        ForeignKey(
            "users.user_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    user: Mapped[User] = relationship(back_populates="user_locations")

    location_id: Mapped[int] = mapped_column(
        "location_id",
        INTEGER,
        ForeignKey(
            "locations.location_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    location: Mapped[Location] = relationship(back_populates="users_locations")

    is_favorite: Mapped[bool] = mapped_column(
        "is_favorite",
        BOOLEAN,
        nullable=False,
        default=False,
        server_default=sql.text("0"),
    )

    @override
    def __str__(self) -> str:
        return f"{self.location.name} ({self.user.username})"


@final
class UserPassword(Base):
    __tablename__ = "users_passwords"

    id: Mapped[int] = mapped_column(
        "user_password_id", INTEGER, primary_key=True, autoincrement=True
    )
    user_id: Mapped[int | None] = mapped_column(
        "user_id",
        INTEGER,
        ForeignKey(
            "users.user_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=True,
    )
    user: Mapped[User] = relationship(back_populates="passwords_hashes")

    password_hash: Mapped[str] = mapped_column(
        "password_hash",
        TEXT,
        nullable=False,
    )

    is_valid: Mapped[bool] = mapped_column(
        "is_valid",
        BOOLEAN,
        nullable=False,
        default=True,
        server_default=sql.text("1"),
    )
