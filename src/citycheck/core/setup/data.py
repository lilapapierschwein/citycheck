from datetime import datetime as dt
from pathlib import Path
from typing import Any, TypedDict

from colorama import Fore, Style

from citycheck import app_config
from citycheck.core.requests.get import get_request
from citycheck.core.requests.sources import (
    RESTCOUNTRIES_API,
    RESTCOUNTRIES_API_AUTH,
    APIAuth,
    SourceAPI,
)
from citycheck.core.utils import format_timedelta, load_json, save_json

from .utils import get_term_width, print_headline


class CountriesData(TypedDict):
    objects: list[dict[str, Any]]
    total: int
    timestamp: int


def get_countries_data(
    api: SourceAPI = RESTCOUNTRIES_API,
    auth: APIAuth = RESTCOUNTRIES_API_AUTH,
    verbose: bool = True,
):
    if auth.token.endswith("00example00"):
        raise RuntimeError(f"invalid auth key for restcountries api: {auth.token!r}")

    # get total country count
    response = get_request(api=api, headers=auth.header, params={"limit": 1})
    total: int = response["data"]["meta"]["total"]

    response_fields = ",".join(
        [
            "names.common",
            "names.official",
            "codes.alpha_2",
            "area.kilometers",
            "tlds",
            "flag.emoji",
            "population",
            "links.google_maps",
            "links.open_street_maps",
            "region",
            "subregion",
            "currencies",
            "languages.name",
            "continents",
        ]
    )

    objects: list[dict[str, Any]] = []
    limit, offset = 100, 0
    while True:
        response = (
            get_request(
                api,
                params={
                    "limit": limit,
                    "offset": offset,
                    "response_fields": response_fields,
                },
                headers=auth.header,
            )
            if auth
            else get_request(api)
        )
        data: dict[str, Any] = response["data"]
        objects.extend(data["objects"])

        if len(objects) == total:
            break

        if verbose:
            print(f"retreived {len(objects)}/{total} items...", end="\r")
        offset += limit

    if verbose:
        print(f"retreived {total}/{total} items...{Fore.GREEN}DONE{Style.RESET_ALL}")

    return CountriesData(objects=objects, total=total, timestamp=int(dt.now().timestamp()))


def get_initial_data(file: Path = app_config.paths.files.init_data, verbose: bool = True):
    if file.exists():
        now = dt.now()
        existing_data = load_json(file)
        last_update = dt.fromtimestamp(existing_data["meta"]["timestamp"])

        last_updated = now - last_update

        if last_updated.total_seconds() < 3600:
            print(
                f"{Fore.YELLOW}warning: the last update was done only",
                f"{format_timedelta(last_updated)} ago!{Style.RESET_ALL}",
            )
            user_confirm = input("are you sure you want to update again? [y/N]: ").strip().lower()
            if user_confirm not in ("y", "yes"):
                print("data update cancelled.")
                return None

    term_width = get_term_width() if verbose else 80
    if verbose:
        print_headline("collecting data...", term_width)

    countries_data_full: CountriesData = get_countries_data(
        auth=RESTCOUNTRIES_API_AUTH, verbose=verbose
    )

    print_headline("processing data...", term_width)

    countries_data: list[dict[str, Any]] = countries_data_full["objects"]

    continents: list[str] = []
    regions: dict[str, list[str]] = {}
    currencies: list[dict[str, str]] = []
    languages: list[str] = []
    countries: list[dict[str, Any]] = []

    for country_data in countries_data:
        continents_data: list[str] | None = country_data.get("continents")
        if continents_data:
            for continent in continents_data:
                if continent not in continents:
                    continents.append(continent)

        region_data: str | None = country_data.get("region")
        subregion_data: str | None = country_data.get("subregion")
        if region_data:
            if region_data not in regions:
                if not subregion_data:
                    if region_data == "Antarctic":
                        regions[region_data] = [region_data]
                    else:
                        regions[region_data] = []
                else:
                    regions[region_data] = [subregion_data]
            else:
                if subregion_data and subregion_data not in regions[region_data]:
                    regions[region_data].append(subregion_data)

        currencies_data: list[dict[str, str]] | None = country_data.get("currencies")
        if currencies_data:
            for currency_data in currencies_data:
                if currency_data["code"] not in [c["code"] for c in currencies]:
                    currencies.append(currency_data)

        languages_data: list[dict[str, str]] | None = country_data.get("languages")
        if languages_data:
            langs_names = [ld["name"] for ld in languages_data]
            for ln in langs_names:
                if ln not in languages:
                    languages.append(ln)

        countries.append(country_data)

    continents.sort()
    currencies.sort(key=lambda c: c["code"])
    languages.sort()

    initial_data = {
        "meta": {
            "total": countries_data_full["total"],
            "timestamp": countries_data_full["timestamp"],
        },
        "objects": {
            "continents": continents,
            "regions": regions,
            "currencies": currencies,
            "languages": languages,
            "countries": countries,
        },
    }

    if verbose:
        print(f"data stored in file: {file}...{Fore.GREEN}DONE{Style.RESET_ALL}")

    save_json(file, initial_data)
