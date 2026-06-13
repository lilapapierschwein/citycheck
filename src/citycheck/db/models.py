from typing import final, override
from zoneinfo import ZoneInfo

from sqlalchemy import sql
from sqlalchemy.dialects.sqlite import BOOLEAN, INTEGER, REAL, TEXT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey

from citycheck.db.types import ZoneInfoType


class Base(DeclarativeBase): ...


@final
class User(Base):
    """Represents a user of the application.

    Attributes:
        id (`int`): The unique identifier of the user.
        username (`str`): The username of the user.
        email (`str`): The email address of the user.
        home_location_id (`int | None`): The foreign key referencing the user's home location.

    Relationships:
        home_location (`Location | None`): The relationship to the user's home location.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        "user_id", INTEGER, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        "username", VARCHAR(255), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        "email", VARCHAR(255), unique=True, nullable=False
    )
    home_location_id: Mapped[int | None] = mapped_column(
        "home_location_id",
        INTEGER,
        ForeignKey("locations.location_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=True,
        default=None,
        server_default=sql.text("null"),
    )
    home_location: Mapped[Location | None] = relationship(back_populates="users_homes")
    user_locations: Mapped[list[UserLocation]] = relationship(back_populates="user")

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
            f"home_location_id={repr(self.home_location_id)}"
            ")"
        )

    @property
    def locations(self) -> list[Location]:
        return [loc.location for loc in self.user_locations]

    @property
    def favorites(self) -> list[Location]:
        return [loc.location for loc in self.user_locations if loc.is_favorite]


@final
class Continent(Base):
    """Represents a continent.

    Attributes:
        id (`int`): The unique identifier of the continent.
        name (`str`): The name of the continent.
    """

    __tablename__ = "continents"

    id: Mapped[int] = mapped_column(
        "continent_id", INTEGER, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)

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

    id: Mapped[int] = mapped_column(
        "region_id", INTEGER, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)
    subregions: Mapped[list[Subregion]] = relationship(back_populates="region")

    @override
    def __str__(self) -> str:
        return self.name

    @override
    def __repr__(self) -> str:
        return f"Region(id={repr(self.id)}, name={repr(self.name)})"

    def get_countries(self) -> list[Country]:
        return [
            country for subregion in self.subregions for country in subregion.countries
        ]


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

    id: Mapped[int] = mapped_column(
        "subregion_id", INTEGER, primary_key=True, autoincrement=True
    )
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
        return (
            "Subregion("
            f"id={repr(self.id)}, "
            f"name={repr(self.name)}, "
            f"region_id={repr(self.region_id)}"
            ")"
        )


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

    id: Mapped[int] = mapped_column(
        "language_id", INTEGER, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)

    countries: Mapped[list[Country]] = relationship(back_populates="language")

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

    id: Mapped[int] = mapped_column(
        "currency_id", INTEGER, primary_key=True, autoincrement=True
    )
    code: Mapped[str] = mapped_column("code", VARCHAR(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)
    symbol: Mapped[str] = mapped_column("symbol", VARCHAR(10), nullable=False)

    countries: Mapped[list[Country]] = relationship(back_populates="currency")

    @override
    def __str__(self) -> str:
        return f"{self.symbol} ({self.name}, {self.code})"

    @override
    def __repr__(self) -> str:
        return f"Currency(id={repr(self.id)}, name={repr(self.name)})"


@final
class Country(Base):
    """Represents a country.

    Attributes:
        id (`int`): The unique identifier of the country.
        name (`str`): The common name of the country.
        official_name (`str`): The official name of the country.
        code (`str`): The ISO 3166-1 alpha-2 code of the country.
        area (`float`): The total area of the country in square kilometers.
        tld (`str`): The top-level domain of the country.
        flag (`str`): The emoji flag of the country.
        population (`int`): The population of the country.
        currency_id (`int`): The foreign key referencing the country's currency.
        language_id (`int`): The foreign key referencing the country's primary language.
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

    id: Mapped[int] = mapped_column(
        "country_id", INTEGER, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)
    official_name: Mapped[str] = mapped_column(
        "official_name", VARCHAR(255), unique=True, nullable=False
    )
    code: Mapped[str] = mapped_column("code", VARCHAR(2), nullable=False)
    area: Mapped[float] = mapped_column("area", REAL, nullable=False)
    tld: Mapped[str] = mapped_column("tld", VARCHAR(10), nullable=False)
    flag: Mapped[str] = mapped_column("flag", VARCHAR(10), nullable=False)
    population: Mapped[int] = mapped_column("population", INTEGER, nullable=False)
    currency_id: Mapped[int] = mapped_column(
        "currency",
        INTEGER,
        ForeignKey("currencies.currency_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    currency: Mapped[Currency] = relationship(back_populates="countries")
    language_id: Mapped[int] = mapped_column(
        "language_id",
        INTEGER,
        ForeignKey("languages.language_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    language: Mapped[Language] = relationship(back_populates="countries")
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
            f"currency_id={repr(self.currency_id)}, "
            f"googlemaps={repr(self.googlemaps)}, "
            f"openstreetmaps={repr(self.openstreetmaps)}, "
            f"subregion_id={repr(self.subregion_id)}"
            ")"
        )

    def get_region(self) -> Region:
        return self.subregion.region


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

    id: Mapped[int] = mapped_column(
        "location_id", INTEGER, primary_key=True, autoincrement=True
    )
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
    users_locations: Mapped[list[UserLocation]] = relationship(
        back_populates="location"
    )

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
