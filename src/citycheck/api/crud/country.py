from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select

from citycheck.api.filters_forms import CountryQueryFilters
from citycheck.api.models.country import CountryCreate
from citycheck.db.models import Country, Currency, Language, Region, Subregion


async def create_country(data: CountryCreate, session: Session) -> Country:
    country = Country(**data.model_dump())

    session.add(country)
    session.commit()

    return country


async def create_countries(
    data: list[CountryCreate], session: Session
) -> list[Country]:
    users = [Country(**d.model_dump()) for d in data]

    session.add_all(users)
    session.commit()

    return users


async def read_country(contry_id: int, session: Session) -> Country:
    return session.get_one(Country, contry_id)


async def read_countries(
    session: Session, filters: CountryQueryFilters
) -> Sequence[Country]:
    stmt = select(Country)

    if filters.name:
        stmt = stmt.where(func.lower(Country.name) == filters.name.lower())
    if filters.code:
        stmt = stmt.where(func.lower(Country.code) == filters.code.lower())
    if filters.currency:
        stmt = stmt.join(Currency).where(
            Currency.name.ilike(f"%{filters.currency.lower()}%")
        )
    if filters.language:
        stmt = stmt.join(Language).where(
            func.lower(Language.name) == filters.language.lower()
        )
    if filters.region:
        stmt = stmt.join(Region).where(
            func.lower(Region.name) == filters.region.lower()
        )
    if filters.subregion:
        stmt = stmt.join(Subregion).where(
            func.lower(Subregion.name) == filters.subregion.lower()
        )
    stmt = stmt.limit(filters.limit).offset(filters.offset)

    return session.scalars(stmt).all()


# def update_country(contry_id: int, session: Session) -> Country: ...


async def delete_country(contry_id: int, session: Session) -> None:
    try:
        country = await read_country(1, session)
        session.delete(country)
        print(f"Country #{contry_id} ({repr(country.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
