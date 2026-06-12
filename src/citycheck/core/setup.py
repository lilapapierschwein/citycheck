# pyright: reportUnknownArgumentType=false

import os
from pathlib import Path
from typing import Any, Literal

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


def get_term_width() -> int:
    return os.get_terminal_size().columns


def print_headline(
    headline: str,
    width: int = 80,
    fillchar: str = "=",
    color: Literal["green", "yellow", "red"] | None = None,
) -> None:
    headline = f" {headline.strip()} ".center(width, fillchar)
    if color:
        match color:
            case "green":
                headline = f"{Fore.GREEN}{headline}"
            case "yellow":
                headline = f"{Fore.YELLOW}{headline}"
            case "red":
                headline = f"{Fore.RED}{headline}"
        headline = f"{headline}{Style.RESET_ALL}"
    print(headline)


def insert_continents(data: list[str], session: Session, verbose: bool = True) -> None:
    term_width = get_term_width() if verbose else 80
    if verbose:
        print_headline("inserting countries...", term_width)

    continents = [Continent(name=d) for d in data]
    session.add_all(continents)
    session.commit()

    if verbose:
        for cont in continents:
            print(f"INSERT: [continent#{cont.id}] {cont}")
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


def insert_languages(data: list[str], session: Session, verbose: bool = True) -> None:
    term_width = get_term_width() if verbose else 80
    if verbose:
        print_headline("inserting languages...", term_width)

    languages = [Language(name=d) for d in data]

    session.add_all(languages)
    session.commit()

    if verbose:
        for lang in languages:
            print(f"INSERT: [language#{lang.id}] {lang}")
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


def insert_currencies(
    data: list[dict[str, str]], session: Session, verbose: bool = True
) -> None:
    term_width = get_term_width() if verbose else 80
    if verbose:
        print_headline("inserting currencies...", term_width)

    currencies = [Currency(**d) for d in data]

    session.add_all(currencies)
    session.commit()

    if verbose:
        for curr in currencies:
            print(f"INSERT  [currency#{curr.id}] {curr}")
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


def insert_regions_subregions(
    data: dict[str, list[str]], session: Session, verbose: bool = True
) -> None:
    term_width = get_term_width() if verbose else 80
    if verbose:
        print_headline("inserting regions...", term_width)

    for k, v in data.items():
        region = Region(name=k)
        session.add(region)
        session.flush()
        session.refresh(region)
        if verbose:
            print(f"INSERT: [region#{region.id}] {region}")

        subregions = [Subregion(name=sr, region_id=region.id) for sr in v]
        session.add_all(subregions)
        session.commit()

        if verbose:
            for sr in subregions:
                print(f"INSERT: [subregion#{sr.id}] {sr} ({region})")

    if verbose:
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


def get_country_data(data: dict[str, Any], session: Session) -> Country:
    country_data = {
        "name": str(data["names"]["common"]),
        "official_name": str(data["names"]["official"]),
        "code": str(data["codes"]["alpha_2"]),
        "area": float(data["area"]["kilometers"]),
        "tld": str(data["tlds"][0]) if len(data["tlds"]) > 0 else "",
        "flag": str(data["flag"]["emoji"]),
        "population": int(data["population"]),
    }

    currency_code: str = (
        str(data["currencies"][0]["code"]) if len(data["currencies"]) > 0 else "USD"
    )
    currency = session.scalar(select(Currency).where(Currency.code == currency_code))
    if not currency:
        raise LookupError(f"Currency not found: {currency_code}")
    country_data["currency_id"] = currency.id

    language_name: str = (
        str(data["languages"][0]["name"]) if len(data["languages"]) > 0 else "English"
    )
    language = session.scalar(select(Language).where(Language.name == language_name))
    if not language:
        raise LookupError(f"Language not found: {language_name}")
    country_data["language_id"] = language.id

    country_data["googlemaps"] = data["links"]["google_maps"]
    country_data["openstreetmaps"] = data["links"]["open_street_maps"]

    subregion_name: str = str(data["subregion"])
    subregion = session.scalar(
        select(Subregion).where(Subregion.name == subregion_name)
    )
    if not subregion:
        raise LookupError(f"Subregion not found: {subregion_name}")
    country_data["subregion_id"] = subregion.id

    country = Country(**country_data)
    return country


def insert_countries(
    data: list[dict[str, Any]], session: Session, verbose: bool = True
) -> None:
    term_width = get_term_width() if verbose else 80
    if verbose:
        print_headline("inserting countries...", term_width)

    for cj in data:
        country = get_country_data(cj, session)
        session.add(country)
        session.commit()
        if verbose:
            print(f"INSERT: [country#{country.id}] {country}")

    if verbose:
        print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")


def insert_initial_data(file: Path, session: Session, verbose: bool = True) -> None:
    term_width = get_term_width() if verbose else 80
    if verbose:
        print_headline("inserting initial data into database...", term_width)

    if verbose:
        print(f"loading data from file {file}...")
    data: dict[str, Any] = load_json(file)

    insert_continents(data["continents"], session, verbose)
    insert_languages(data["languages"], session, verbose)
    insert_currencies(data["currencies"], session, verbose)
    insert_regions_subregions(data["regions"], session, verbose)
    insert_countries(data["countries"], session, verbose)

    if verbose:
        print_headline("data inserted", term_width, color="green")
