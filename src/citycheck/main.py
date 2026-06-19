from collections.abc import Sequence
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.api.models.location import LocationCreate
from citycheck.core.requests.get import get_request
from citycheck.core.requests.sources import (
    SourceAPI,
)
from citycheck.core.setup.setup import run_setup
from citycheck.core.utils import load_json
from citycheck.db.models import (
    Continent,
    Country,
    Currency,
    Language,
    Location,
    Region,
    Subregion,
)


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


def get_country_data(
    json_data: dict[str, Any], session: Session
) -> tuple[Country, Sequence[Currency], Sequence[Language], Sequence[Continent]]:
    data = {
        "name": json_data["names"]["common"],
        "official_name": json_data["names"]["official"],
        "code": json_data["codes"]["alpha_2"],
        "area": float(json_data["area"]["kilometers"]),
        "tld": json_data["tlds"][0] if len(json_data["tlds"]) > 0 else "",
        "flag": json_data["flag"]["emoji"],
        "population": json_data["population"],
    }

    data["googlemaps"] = json_data["links"]["google_maps"]
    data["openstreetmaps"] = json_data["links"]["open_street_maps"]

    subregion_name: str = json_data["subregion"]
    subregion = session.scalar(select(Subregion).where(Subregion.name == subregion_name))
    if not subregion:
        data["subregion_id"] = None
    else:
        data["subregion_id"] = subregion.id

    currency_codes: list[str] = [c["code"] for c in json_data["currencies"]]
    currencies = session.scalars(select(Currency).where(Currency.code.in_(currency_codes))).all()
    if not currencies:
        raise LookupError(f"Currencies not found: {currency_codes}")

    languages_names: list[str] = [lang["name"] for lang in json_data["languages"]]
    languages = session.scalars(select(Language).where(Language.name.in_(languages_names))).all()
    if not languages:
        raise LookupError(f"Languages not found: {languages_names}")

    continents_names: list[str] = [cont for cont in json_data["continents"]]
    continents = session.scalars(
        select(Continent).where(Continent.name.in_(continents_names))
    ).all()
    if not continents:
        raise LookupError(f"Continents not found: {continents_names}")

    country = Country(**data)
    return country, currencies, languages, continents


# def insert_countries(file: Path, session: Session) -> None:
#     countries_json: list[dict[str, Any]] = load_json(file)
#
#     for cj in countries_json:
#         country, currencies, languages, continents = get_country_data(cj, session)
#         session.add(country)
#         session.commit()
#
#         country_currencies = [
#             CountryCurrency(country_id=country.id, currency_id=cur.id)
#             for cur in currencies
#         ]
#         session.add_all(country_currencies)
#
#         country_languages = [
#             CountryLanguage(country_id=country.id, language_id=lang.id)
#             for lang in languages
#         ]
#         session.add_all(country_languages)
#
#         country_continents = [
#             CountryContinent(country_id=country.id, continent_id=cont.id)
#             for cont in continents
#         ]
#         session.add_all(country_continents)
#         session.commit()
#
#         print(f"country inserted: [#{country.id}] {country}")


def save_location(data: dict[str, Any], session: Session) -> None:
    country_code = str(data["country_code"])
    country = session.scalar(select(Country).where(Country.code == country_code))
    if not country:
        raise LookupError(f"No country found for code {repr(country_code)}")

    location_data = {
        "name": str(data["name"]),
        "latitude": float(data["latitude"]),
        "longitude": float(data["longitude"]),
        "elevation": float(data["elevation"]),
        "population": int(data["population"]),
        "timezone": str(data["timezone"]),
        "country_id": country.id,
    }
    location_create = LocationCreate.model_validate(location_data)
    location = Location(**location_create.model_dump())
    session.add(location)
    session.commit()
    print("location created:", location)


def run() -> None:
    run_setup(rebuild_db=True, update_init_data=True)
    # app_config = load_app_config(Path.cwd() / "configs" / "app_config.toml")
    # print(app_config)
    #
    # get_initial_data()
    # return

    # de = get_request(RESTCOUNTRIES_API_CODE, uid="de")[0]
    # pprint(de["translations"]["deu"])

    # loc = BaseLocation.model_validate(loc_data)
    # pprint(loc)
    # de = get_country_data("de")
    # pprint(de[0]["translations"]["deu"], indent=2, sort_dicts=False)

    # api = GEOCODING_API
    # le_data: list[dict[str, Any]] = get_location_data("Leipzig", api)
    # le = le_data[0]
    #
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
    #     #     # save_location(le, Session)
    #     insert_initial_data(INIT_DATA_FILE, Session)
    #     # insert_continents(ROOT / "continents.json", Session)
    #     # insert_regions_subregions(ROOT / "subregions.json", Session)
    #     # insert_languages(ROOT / "languages.json", Session)
    #     # insert_currencies(ROOT / "currencies.json", Session)
    #     # insert_countries(ROOT / "countries.json", Session)
    #
    #     result = Session.scalar(select(Country).where(Country.id == 232))
    #     if not result:
    #         print("MEH")
    #         return None
    #     de = CountrySchema.model_validate(result)
    #     print(de.model_dump_json())
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
