# ruff: noqa: E261, F401
# pyright: reportUnusedImport=false

from dataclasses import dataclass
from modulefinder import test
from pathlib import Path
from pprint import pprint
from typing import Any

import requests
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.api.crud import create_user, delete_user, read_location, read_user
from citycheck.api.models.continent import ContinentCreate
from citycheck.api.models.location import LocationCreate
from citycheck.api.models.user import UserCreate, UserModel
from citycheck.core.requests.get import get_request
from citycheck.core.requests.sources import SourceAPI
from citycheck.core.setup import insert_initial_data
from citycheck.core.utils import load_json
from citycheck.db.db import SqliteDB, init_db
from citycheck.db.models import (
    Continent,
    Country,
    Currency,
    Language,
    Location,
    Region,
    Subregion,
    User,
)
from citycheck.settings import DATA_DIR, ROOT


def get_location_data(name: str, api: SourceAPI) -> Any:
    location_data: Any = None
    try:
        if name == "":
            raise ValueError("Location name cannot be empty")
        location_data = get_request(api, params={"name": name, "count": 10})
    except Exception as e:
        print(e)
    return location_data["results"]


# def get_country_data(code: str) -> Any:
#     country_data: Any = None
#     try:
#         if len(code) != 2:
#             raise ValueError("Country code must be consist of 2 characters.")
#         response = get_request(api=RESTCOUNTRIES_API_CODE, uid=code)
#         if response.status_code != 200:
#             response.raise_for_status()
#         country_data = response.json()
#     except Exception as e:
#         print(e)
#     return country_data


def insert_continents(file: Path, session: Session) -> None:
    continents_json: list[str] = load_json(file)
    continents = [Continent(name=c) for c in continents_json]
    session.add_all(continents)
    session.commit()

    print("continents inserted:")
    for cont in continents:
        print(f"[#{cont.id}] {cont}")


def insert_languages(file: Path, session: Session) -> None:
    languages_json: list[str] = load_json(file)
    languages = [Language(name=lang) for lang in languages_json]

    session.add_all(languages)
    session.commit()

    print("langages inserted:")
    for lang in languages:
        print(f"[#{lang.id}] {lang}")


def insert_currencies(file: Path, session: Session) -> None:
    currencies_json: list[dict[str, str]] = load_json(file)
    currencies = [Currency(**curr) for curr in currencies_json]

    session.add_all(currencies)
    session.commit()

    print("currencies inserted:")
    for curr in currencies:
        print(f"[#{curr.id}] {curr}")


def insert_regions_subregions(file: Path, session: Session) -> None:
    regions_subregions: dict[str, list[str]] = load_json(file)

    for k, v in regions_subregions.items():
        region = Region(name=k)
        session.add(region)
        if len(v) == 0:
            session.commit()
            print(f"region inserted: [#{region.id}] {region}")
            continue
        session.flush()
        session.refresh(region)
        region_id = region.id
        subregions = [Subregion(name=sr, region_id=region_id) for sr in v]
        session.add_all(subregions)
        session.commit()

        print(f"region inserted: [#{region_id}] {region} with subregions:")
        for sr in subregions:
            print(f"[#{sr.id}] {sr}")


def get_country_data(json_data: dict[str, Any], session: Session) -> Country:
    data = {
        "name": json_data["names"]["common"],
        "official_name": json_data["names"]["official"],
        "code": json_data["codes"]["alpha_2"],
        "area": float(json_data["area"]["kilometers"]),
        "tld": json_data["tlds"][0] if len(json_data["tlds"]) > 0 else "",
        "flag": json_data["flag"]["emoji"],
        "population": json_data["population"],
    }

    currency_code: str = (
        json_data["currencies"][0]["code"]
        if len(json_data["currencies"]) > 0
        else "USD"
    )
    currency = session.scalar(select(Currency).where(Currency.code == currency_code))
    if not currency:
        raise LookupError(f"Currency not found: {currency_code}")
    data["currency_id"] = currency.id

    language_name: str = (
        json_data["languages"][0]["name"]
        if len(json_data["languages"]) > 0
        else "English"
    )
    language = session.scalar(select(Language).where(Language.name == language_name))
    if not language:
        raise LookupError(f"Language not found: {language_name}")
    data["language_id"] = language.id

    data["googlemaps"] = json_data["links"]["google_maps"]
    data["openstreetmaps"] = json_data["links"]["open_street_maps"]

    subregion_name: str = json_data["subregion"]
    subregion = session.scalar(
        select(Subregion).where(Subregion.name == subregion_name)
    )
    if not subregion:
        data["subregion_id"] = None
    else:
        data["subregion_id"] = subregion.id

    country = Country(**data)
    return country


def insert_countries(file: Path, session: Session) -> None:
    countries_json: list[dict[str, Any]] = load_json(file)

    for cj in countries_json:
        country = get_country_data(cj, session)
        session.add(country)
        session.commit()
        print(f"country inserted: [#{country.id}] {country}")


def run() -> None:
    # de = get_request(RESTCOUNTRIES_API_CODE, uid="de")[0]
    # pprint(de["translations"]["deu"])

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

    db = init_db()
    with db.get_session() as Session:
        insert_initial_data(DATA_DIR / "initial_data.json", Session)
        # insert_continents(ROOT / "continents.json", Session)
        # insert_regions_subregions(ROOT / "subregions.json", Session)
        # insert_languages(ROOT / "languages.json", Session)
        # insert_currencies(ROOT / "currencies.json", Session)
        # insert_countries(ROOT / "countries.json", Session)
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
