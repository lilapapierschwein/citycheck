from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.core.validation.models.country import CountryCreate
from citycheck.db.models import Country


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


async def read_countries(session: Session) -> Sequence[Country]:
    return session.scalars(select(Country)).all()


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
