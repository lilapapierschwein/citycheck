from typing import final, override
from zoneinfo import ZoneInfo

from sqlalchemy import sql
from sqlalchemy.dialects.sqlite import INTEGER, REAL, VARCHAR
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
    # country_id: Mapped[int]

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
            f"population={repr(self.population)}"
            ")"
        )
