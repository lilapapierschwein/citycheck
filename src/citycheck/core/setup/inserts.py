from pathlib import Path
from typing import Any

from colorama import Fore, Style
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.core.utils import load_json
from citycheck.db.models import (
    Continent,
    Country,
    Currency,
    Language,
    Region,
    Subregion,
)

from .utils import print_headline


def insert_continents(data: list[str], session: Session, verbose: bool = True) -> None:
    id_pad = len(str(len(data)))

    if verbose:
        print("inserting countries...")

    continents = [Continent(name=d) for d in data]
    session.add_all(continents)
    session.commit()

    if verbose:
        for cont in continents:
            print(f"INSERT: [continent#{str(cont.id).zfill(id_pad)}] {cont}")
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


def insert_languages(data: list[str], session: Session, verbose: bool = True) -> None:
    id_pad = len(str(len(data)))

    if verbose:
        print("inserting languages...")

    languages = [Language(name=d) for d in data]

    session.add_all(languages)
    session.commit()

    if verbose:
        for lang in languages:
            print(f"INSERT: [language#{str(lang.id).zfill(id_pad)}] {lang}")
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


def insert_currencies(
    data: list[dict[str, str]], session: Session, verbose: bool = True
) -> None:
    id_pad = len(str(len(data)))
    if verbose:
        print("inserting currencies...")

    currencies = [Currency(**d) for d in data]

    session.add_all(currencies)
    session.commit()

    if verbose:
        for curr in currencies:
            print(f"INSERT: [currency#{str(curr.id).zfill(id_pad)}] {curr}")
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


def insert_regions_subregions(
    data: dict[str, list[str]], session: Session, verbose: bool = True
) -> None:
    regions_total = len(data.keys())
    subregions_total = len(
        [subregion for subregions in data.values() for subregion in subregions]
    )
    id_pad_region, id_pad_subregion = (
        len(str(regions_total)),
        len(str(subregions_total)),
    )
    if verbose:
        print("inserting regions and subregions...")

    for k, v in data.items():
        region = Region(name=k)
        session.add(region)
        session.flush()
        session.refresh(region)
        if verbose:
            print(f"INSERT: [region#{str(region.id).zfill(id_pad_region)}] {region}")

        subregions = [Subregion(name=sr, region_id=region.id) for sr in v]
        session.add_all(subregions)
        session.commit()

        if verbose:
            for sr in subregions:
                print(
                    f"INSERT: [subregion#{str(sr.id).zfill(id_pad_subregion)}] {sr} ({region})"
                )

    if verbose:
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


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

    currency_codes: list[str] = [c["code"] for c in json_data["currencies"]]
    currencies = session.scalars(
        select(Currency).where(Currency.code.in_(currency_codes))
    ).all()
    country.currencies.extend(currencies)

    languages_names: list[str] = [lang["name"] for lang in json_data["languages"]]
    with session.no_autoflush:
        languages = session.scalars(
            select(Language).where(Language.name.in_(languages_names))
        ).all()
        country.languages.extend(languages)

        continents_names: list[str] = [cont for cont in json_data["continents"]]
        continents = session.scalars(
            select(Continent).where(Continent.name.in_(continents_names))
        ).all()
        country.continents.extend(continents)

    return country


def insert_countries(
    data: list[dict[str, Any]], session: Session, verbose: bool = True
) -> None:
    id_pad = len(str(len(data)))
    if verbose:
        print("inserting countries...")

    for cj in data:
        country = get_country_data(cj, session)
        session.add(country)
        session.commit()
        print(f"INSERT: [country#{str(country.id).zfill(id_pad)}] {country}")

    if verbose:
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


def insert_initial_data(
    file: Path, session: Session, text_width: int = 80, verbose: bool = True
) -> None:
    if verbose:
        print_headline("collecting data...", text_width)

    if verbose:
        print(f"loading data from file {file}...", end="\r")
    data: dict[str, Any] = load_json(file)
    if verbose:
        print(f"loading data from file {file}...{Fore.GREEN}DONE{Style.RESET_ALL}")

    objects: dict[str, Any] = data["objects"]

    if verbose:
        print_headline("inserting initial data into database...", text_width)

    insert_continents(objects["continents"], session, verbose)
    insert_languages(objects["languages"], session, verbose)
    insert_currencies(objects["currencies"], session, verbose)
    insert_regions_subregions(objects["regions"], session, verbose)
    insert_countries(objects["countries"], session, verbose)
