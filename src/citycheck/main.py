# ruff: noqa: E261, F401
# pyright: reportUnusedImport=false

from dataclasses import dataclass
from modulefinder import test
from pprint import pprint
from typing import Any

import requests
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql import select

from citycheck.api.crud.location import read_location
from citycheck.api.crud.user import create_user, delete_user, read_user
from citycheck.core.requests.get import get_request
from citycheck.core.requests.sources import SourceAPI
from citycheck.core.validation.models.location import BaseLocation
from citycheck.core.validation.models.user import BaseUser, UserModel
from citycheck.db.db import init_db
from citycheck.db.models import Country, Location, User


def get_location_data(name: str, api: SourceAPI) -> Any:
    location_data: Any = None
    try:
        if name == "":
            raise ValueError("Location name cannot be empty")
        location_data = get_request(api, params={"name": name, "count": 10})
    except Exception as e:
        print(e)
    return location_data["results"]


def get_country_data(code: str) -> Any:
    country_data: Any = None
    try:
        if len(code) != 2:
            raise ValueError("Country code must be consist of 2 characters.")
        response = requests.get(f"https://restcountries.com/v3.1/alpha/{code}")
        if response.status_code != 200:
            response.raise_for_status()
        country_data = response.json()
    except Exception as e:
        print(e)
    return country_data


def run() -> None:
    db = init_db()

    with db.get_session() as Session:
        geocoding_api = SourceAPI("https://geocoding-api.open-meteo.com", "1", "search")
        loc_data: dict[str, Any] = get_location_data("Leipzig", geocoding_api)[0]
        name: str = loc_data["name"]

        loc_db = Session.scalar(select(Location).where(Location.name == name))
        # if not in db, create a new one
        if loc_db is not None:
            print(loc_db)
            return None

        # check if country is stored first
        country_code: str = loc_data["country_code"]
        country_db = Session.scalar(select(Country).where(Country.code == country_code))
        if country_db is not None:
            print(country_db)
            return None

        country_data = get_country_data(country_code)
        pprint(country_data)

        # loc = BaseLocation.model_validate(loc_data)
        # pprint(loc)
    # de = get_country_data("de")
    # pprint(de[0]["translations"]["deu"], indent=2, sort_dicts=False)

    # api = API("https://geocoding-api.open-meteo.com", 1, "search")
    # le_data: list[dict[str, Any]] = get_location_data("Leipzig", api)
    # pprint(le_data, sort_dicts=False)
    #
    # le = le_data[0]
    # print(le["country_code"])

    # base_le = BaseLocation.model_validate(le)
    # print(base_le.country_id)

    # testuser = {
    #     "username": "testuser",
    #     "email": "testuser@example.com",
    # }

    # db = init_db()
    # with db.get_session() as Session:
    #     # user = create_user(BaseUser(**testuser), Session)
    #
    #     try:
    #         user = read_user(1, Session)
    #     except NoResultFound as err:
    #         print(err)
    #         return None
    #
    #     print(repr(user))

    # delete_user(1, Session)/www.openstreetmap.org/relation/51477"

    # "population": 83491249,

    #     users = Session.scalars(
    #         select(User).where(User.home_location_id.is_(None))
    #     ).all()
    #     if not users:
    #         return None
    #     for user in users:
    #         print(f"User#{user.id}: {user} | {user.email} | Home: {user.home_location}")

    # kai_db = Session.get(User, 1)
    # if kai_db:
    #     kai = UserModel.model_validate(kai_db)
    #     pprint(kai)
    #     print(kai.home_location)
    #     Session.add(leipzig)
    #     Session.flush()
    #     Session.refresh(leipzig)
    #
    #     user.home_location_id = leipzig.id
    #     Session.add(user)
    #     Session.commit()
    #
    #     print(user, repr(user), user.home_location, sep="\n", end="\n\n")
    #     print(leipzig, repr(leipzig), leipzig.users, sep="\n")
    return None


def main() -> None:
    run()
