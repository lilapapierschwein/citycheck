from pathlib import Path
from typing import Any

from colorama import Fore, Style
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from citycheck.api.models.continent import ContinentCreate
from citycheck.api.models.country import CountryCreate, CountryIn
from citycheck.api.models.currency import CurrencyCreate
from citycheck.api.models.language import LanguageCreate
from citycheck.api.models.region import RegionCreate, SubregionCreate
from citycheck.core.utils import load_json
from citycheck.db.models import (
    Continent,
    Country,
    Currency,
    Language,
    Region,
    Subregion,
)

from .utils import ProgressBar, get_term_width, print_headline


def insert_continents(data: list[str], session: Session, verbose: bool = True) -> None:
    id_pad = len(str(len(data)))
    print("inserting continents...", end="\r")

    data_validated = [ContinentCreate.model_validate({"name": d}) for d in data]
    continents = [Continent(**dv.model_dump()) for dv in data_validated]
    session.add_all(continents)
    session.commit()

    print(f"inserting continents...{Fore.GREEN}DONE{Style.RESET_ALL}")
    if verbose:
        inserts: list[str] = [
            f"INSERT: [continent#{str(cont.id).zfill(id_pad)}] {cont}" for cont in continents
        ]
        print("\n".join(inserts))


def insert_languages(data: list[str], session: Session, verbose: bool = True) -> None:
    id_pad = len(str(len(data)))
    print("inserting languages...", end="\r")

    data_validated = [LanguageCreate.model_validate({"name": d}) for d in data]
    languages = [Language(**dv.model_dump()) for dv in data_validated]

    session.add_all(languages)
    session.commit()

    print(f"inserting languages...{Fore.GREEN}DONE{Style.RESET_ALL}")

    if verbose:
        inserts: list[str] = [
            f"INSERT: [language#{str(lang.id).zfill(id_pad)}] {lang}" for lang in languages
        ]
        print("\n".join(inserts))


def insert_currencies(data: list[dict[str, str]], session: Session, verbose: bool = True) -> None:
    id_pad = len(str(len(data)))
    print("inserting currencies...", end="\r")

    data_validated = [CurrencyCreate.model_validate(d) for d in data]
    currencies = [Currency(**dv.model_dump()) for dv in data_validated]

    session.add_all(currencies)
    session.commit()

    inserts = [f"INSERT: [currency#{str(curr.id).zfill(id_pad)}] {curr}" for curr in currencies]
    print(f"inserting currencies...{Fore.GREEN}DONE{Style.RESET_ALL}")

    if verbose:
        print("\n".join(inserts))


def insert_regions_subregions(
    data: dict[str, list[str]], session: Session, verbose: bool = True
) -> None:
    regions_total = len(data.keys())
    subregions_total = len([subregion for subregions in data.values() for subregion in subregions])
    id_pad_region, id_pad_subregion = (
        len(str(regions_total)),
        len(str(subregions_total)),
    )
    print("inserting regions and subregions...", end="\r")

    inserts: list[str] = []
    for k, v in data.items():
        region_validated = RegionCreate.model_validate({"name": k})
        region = Region(**region_validated.model_dump())
        session.add(region)
        session.flush()
        session.refresh(region)

        inserts.append(f"INSERT: [region#{str(region.id).zfill(id_pad_region)}] {region}")

        subregions_validated = [
            SubregionCreate.model_validate({"name": sr, "region_id": region.id}) for sr in v
        ]
        subregions = [Subregion(**srv.model_dump()) for srv in subregions_validated]
        session.add_all(subregions)
        session.commit()

        inserts.extend(
            [
                f"INSERT: [subregion#{str(sr.id).zfill(id_pad_subregion)}] {sr} ({region})"
                for sr in subregions
            ]
        )

    print(f"inserting regions and subregions...{Fore.GREEN}DONE{Style.RESET_ALL}")
    if verbose:
        print("\n".join(inserts))


def get_country_data(json_data: dict[str, Any], session: Session) -> Country:
    country_in = CountryIn.model_validate(json_data)
    junctions = country_in.get_junctions(session)

    country_data = CountryCreate.model_validate(country_in.model_dump(), from_attributes=True)
    country = Country(**country_data.model_dump())
    with session.no_autoflush:
        if junctions["currencies_ids"]:
            country.currencies.extend(
                session.scalars(
                    select(Currency).where(Currency.id.in_(junctions["currencies_ids"]))
                ).all()
            )
        if junctions["languages_ids"]:
            country.languages.extend(
                session.scalars(
                    select(Language).where(Language.id.in_(junctions["languages_ids"]))
                ).all()
            )
        if junctions["continents_ids"]:
            country.continents.extend(
                session.scalars(
                    select(Continent).where(Continent.id.in_(junctions["continents_ids"]))
                ).all()
            )
    return country


# class ProgressBar:
#     def __init__(
#         self, total: int, scale: Literal[10, 20, 50, 100] = 50, char: Literal["#", "*"] = "#"
#     ) -> None:
#         self.total: int = total
#         self.scale: int = scale
#         self.char: str = char
#
#         self.bar_value: float = 100 / self.scale
#         self.bar_empty: str = "." * self.scale
#
#     def __call__(self, c: int) -> str:
#         percentage = self._get_percentage(c)
#         bars_count = self._get_bars_count(percentage)
#         bars = self._get_bars(bars_count)
#         return f"[{self._get_current_bar(bars, bars_count)}]"
#
#     def _get_percentage(self, c: int | float) -> float:
#         return (c / self.total) * 100
#
#     def _get_bars_count(self, p: float) -> int:
#         return int(p // self.bar_value)
#
#     def _get_bars(self, c: int) -> str:
#         return self.char * c
#
#     def _get_current_bar(self, b: str, c: int) -> str:
#         return b + self.bar_empty[c:]


def insert_countries(data: list[dict[str, Any]], session: Session, verbose: bool = True) -> None:
    text_width = get_term_width()
    total = len(data)
    pad = len(str(total))
    pbar = ProgressBar(total)

    for i, cj in enumerate(data):
        print(f"inserting countries...{pbar(i + 1)} ({str(i + 1).zfill(pad)}/{total})", end="\r")
        country = get_country_data(cj, session)
        session.add(country)
        session.commit()
        if verbose:
            stmt = f"INSERT: [country#{str(country.id).zfill(pad)}] {country}"
            print(
                stmt + " " * (text_width - len(stmt)),
            )

    print(
        f"inserting countries...{pbar(total)} ({str(total).zfill(pad)}/{total})",
        f"{Fore.GREEN}DONE{Style.RESET_ALL}",
        sep="...",
    )


def insert_initial_data(
    file: Path, session: Session, text_width: int = 80, verbose: bool = True
) -> None:
    print_headline("collecting data...", text_width)

    print(f"loading data from file {file}...", end="\r")
    data: dict[str, Any] = load_json(file)
    print(f"loading data from file {file}...{Fore.GREEN}DONE{Style.RESET_ALL}")

    objects: dict[str, Any] = data["objects"]

    if verbose:
        print_headline("inserting initial data into database...", text_width)

    insert_continents(objects["continents"], session, verbose)
    insert_languages(objects["languages"], session, verbose)
    insert_currencies(objects["currencies"], session, verbose)
    insert_regions_subregions(objects["regions"], session, verbose)
    insert_countries(objects["countries"], session)
