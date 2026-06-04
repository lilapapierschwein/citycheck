# ruff: noqa: E261, F401
# pyright: reportUnusedImport=false

from dataclasses import dataclass
from pprint import pprint
from typing import Any

import requests
from sqlalchemy.sql import select

from citycheck.core.crud.user_crud import create_user
from citycheck.core.validation.models.location import BaseLocation
from citycheck.core.validation.models.user import BaseUser, UserModel
from citycheck.db.db import init_db
from citycheck.db.models import User


@dataclass
class API:
    base_url: str
    api_version: int
    endpoint: str

    @property
    def url(self) -> str:
        return f"{self.base_url}/v{self.api_version}/{self.endpoint}"


def get_request(api: API, params: dict[str, Any]) -> Any:
    response = requests.get(api.url, params)
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()


def get_location_data(name: str, api: API) -> Any:
    location_data: Any = None
    try:
        if name == "":
            raise ValueError("Location name cannot be empty")
        location_data = get_request(api, {"name": name, "count": 10})
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

    # new_user = BaseUser(
    #     username="lilapapierschwein", email="lilapapierschwein@example.com"
    # )

    # db = init_db()
    # with db.get_session() as Session:
    #     user = Session.scalar(select(User).where(User.id == 1))
    #     if user is None:
    #         print("User not not found.")
    #         return None
    #
    #     print(repr(user))

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
