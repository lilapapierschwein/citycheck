# ruff: noqa: E261, F401
# pyright: reportUnusedImport=false

from dataclasses import dataclass
from pprint import pprint
from typing import Any

import requests

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


def get_location_data(name: str, api: API):
    location_data: Any = None
    try:
        if name == "":
            raise ValueError("Location name cannot be empty")
        location_data = get_request(api, {"name": name, "count": 1})
    except Exception as e:
        print(e)
    return location_data["results"][0]


def run() -> None:
    # api = API("https://geocoding-api.open-meteo.com", 1, "search")
    # le_data = get_location_data("Leipzig", api)

    # pprint(le_data, sort_dicts=False)

    db = init_db()
    #
    # leipzig = Location(
    #     name="Leipzig", alias_name="Heeme", latitude=51.33962, longitude=12.37129
    # )
    # user = User(username="kai", email="kai@example.com")
    #
    with db.get_session() as Session:
        kai_db = Session.get(User, 1)
        if kai_db:
            kai = UserModel.model_validate(kai_db)
            pprint(kai)
            print(kai.home_location)
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


def main() -> None:
    run()
