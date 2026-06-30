from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select

from citycheck.api.filters_forms.countries import CountryQueryFilters
from citycheck.api.models.country import CountryCreate
from citycheck.db.models import (
    Country,
)


async def create_country(data: CountryCreate, session: Session) -> Country:
    country = Country(**data.model_dump())

    session.add(country)
    session.commit()

    return country


async def create_countries(data: list[CountryCreate], session: Session) -> list[Country]:
    countries = [Country(**d.model_dump()) for d in data]

    session.add_all(countries)
    session.commit()

    return countries


async def read_country(contry_id: int, session: Session) -> Country:
    return session.get_one(Country, contry_id)


async def read_country_by_code(country_code: str, session: Session) -> Country | None:
    return session.scalar(select(Country).where(Country.code == country_code))


async def read_countries(
    session: Session, filters: CountryQueryFilters
) -> tuple[Sequence[Country], int]:
    total = session.scalar(select(func.count()).select_from(Country)) or 0
    stmt = filters.apply(select(Country))
    return session.scalars(stmt).all(), total


# def update_country(contry_id: int, session: Session) -> Country: ...


async def delete_country(contry_id: int, session: Session) -> None:
    try:
        country = await read_country(contry_id, session)
        session.delete(country)
        print(f"Country #{contry_id} ({repr(country.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
