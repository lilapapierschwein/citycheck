from typing import final, override
from zoneinfo import ZoneInfo

from sqlalchemy import sql
from sqlalchemy.dialects.sqlite import INTEGER, REAL, TEXT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey

from citycheck.db.types import ZoneInfoType


class Base(DeclarativeBase): ...


@final
class User(Base):
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
    home_location: Mapped[Location | None] = relationship(back_populates="users")

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


@final
class Region(Base):
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
class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(
        "country_id", INTEGER, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column("name", VARCHAR(255), unique=True, nullable=False)
    official_name: Mapped[str] = mapped_column(
        "official_name", VARCHAR(255), unique=True, nullable=False
    )
    code: Mapped[str] = mapped_column("code", VARCHAR(2), unique=True, nullable=False)
    area: Mapped[float] = mapped_column("area", REAL, nullable=False)
    tld: Mapped[str] = mapped_column("tld", VARCHAR(10), nullable=False)
    flag: Mapped[str] = mapped_column("flag", VARCHAR(10), nullable=False)
    population: Mapped[int] = mapped_column("population", INTEGER, nullable=False)
    googlemaps: Mapped[str] = mapped_column("googlemaps", TEXT, nullable=False)
    openstreetmaps: Mapped[str] = mapped_column("openstreetmaps", TEXT, nullable=False)
    subregion_id: Mapped[int] = mapped_column(
        "subregion_id",
        INTEGER,
        ForeignKey("subregions.subregion_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
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
            f"googlemaps={repr(self.googlemaps)}, "
            f"openstreetmaps={repr(self.openstreetmaps)}, "
            f"subregion_id={repr(self.subregion_id)}"
            ")"
        )

    def get_region(self) -> Region:
        return self.subregion.region


@final
class Location(Base):
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
    users: Mapped[list[User]] = relationship(back_populates="home_location")

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
