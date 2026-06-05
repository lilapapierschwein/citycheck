from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.core.validation.models.country import BaseCountry
from citycheck.db.models import Country


def create_country(data: BaseCountry, session: Session) -> Country:
    country = Country(**data.model_dump())

    session.add(country)
    session.commit()

    return country


def create_countries(data: list[BaseCountry], session: Session) -> list[Country]:
    users = [Country(**d.model_dump()) for d in data]

    session.add_all(users)
    session.commit()

    return users


def read_country(contry_id: int, session: Session) -> Country:
    return session.get_one(Country, contry_id)


def read_countries(session: Session) -> Sequence[Country]:
    return session.scalars(select(Country)).all()


# def update_country(contry_id: int, session: Session) -> Country: ...


def delete_country(contry_id: int, session: Session) -> None:
    try:
        country = read_country(1, session)
        session.delete(country)
        print(f"Country #{contry_id} ({repr(country.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
