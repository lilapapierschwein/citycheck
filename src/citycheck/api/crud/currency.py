from collections.abc import Sequence

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.api.models.currency import CurrencyCreate
from citycheck.db.models import Currency


async def create_currency(data: CurrencyCreate, session: Session) -> Currency:
    currency = Currency(**data.model_dump())

    session.add(currency)
    session.commit()

    return currency


async def create_currencies(
    data: list[CurrencyCreate], session: Session
) -> list[Currency]:
    currencies = [Currency(**d.model_dump()) for d in data]

    session.add_all(currencies)
    session.commit()

    return currencies


async def read_currency(currency_id: int, session: Session) -> Currency:
    return session.get_one(Currency, currency_id)


async def read_currencies(session: Session) -> Sequence[Currency]:
    return session.scalars(select(Currency)).all()


# def update_currency(currency_id: int, session: Session) -> Currency: ...


async def delete_currency(currency_id: int, session: Session) -> None:
    try:
        currency = await read_currency(1, session)
        session.delete(currency)
        print(f"Currency #{currency_id} ({repr(currency.name)}) deleted.")
        session.commit()
    except NoResultFound as err:
        print(err)
    return None
