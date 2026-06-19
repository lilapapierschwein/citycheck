# # pyright: reportUnknownArgumentType=false
#
# import os
# from datetime import datetime
# from pathlib import Path
# from typing import Any, Literal, TypedDict
#
# from colorama import Fore, Style
# from sqlalchemy.orm import Session
# from sqlalchemy.sql import select
#
# from citycheck.core.requests.get import get_request
# from citycheck.core.requests.sources import (
#     RESTCOUNTRIES_API,
#     RESTCOUNTRIES_API_AUTH,
#     APIAuth,
#     SourceAPI,
# )
# from citycheck.core.utils import format_timedelta, load_json, save_json
# from citycheck.db.db import init_db
# from citycheck.db.models import (
#     Continent,
#     Country,
#     Currency,
#     Language,
#     Region,
#     Subregion,
#     User,
# )
# from citycheck.settings import DB_FILE, INIT_DATA_FILE
#
#
# def get_term_width() -> int:
#     return os.get_terminal_size().columns
#
#
# def print_headline(
#     headline: str,
#     width: int = 80,
#     fillchar: str = "=",
#     color: Literal["green", "yellow", "red"] | None = None,
# ) -> None:
#     headline = f" {headline.strip()} ".center(width, fillchar)
#     if color:
#         match color:
#             case "green":
#                 headline = f"{Fore.GREEN}{headline}"
#             case "yellow":
#                 headline = f"{Fore.YELLOW}{headline}"
#             case "red":
#                 headline = f"{Fore.RED}{headline}"
#         headline = f"{headline}{Style.RESET_ALL}"
#     print(headline)
#
#
# class CountriesData(TypedDict):
#     objects: list[dict[str, Any]]
#     total: int
#     timestamp: int
#
#
# def get_countries_data(
#     api: SourceAPI = RESTCOUNTRIES_API,
#     auth: APIAuth = RESTCOUNTRIES_API_AUTH,
#     verbose: bool = True,
# ):
#     # get total country count
#     response = get_request(api=api, headers=auth.header, params={"limit": 1})
#     total: int = response["data"]["meta"]["total"]
#
#     response_fields = ",".join(
#         [
#             "names.common",
#             "names.official",
#             "codes.alpha_2",
#             "area.kilometers",
#             "tlds",
#             "flag.emoji",
#             "population",
#             "links.google_maps",
#             "links.open_street_maps",
#             "region",
#             "subregion",
#             "currencies",
#             "languages.name",
#             "continents",
#         ]
#     )
#
#     objects: list[dict[str, Any]] = []
#     limit, offset = 100, 0
#     while True:
#         response = (
#             get_request(
#                 api,
#                 params={
#                     "limit": limit,
#                     "offset": offset,
#                     "response_fields": response_fields,
#                 },
#                 headers=auth.header,
#             )
#             if auth
#             else get_request(api)
#         )
#         data: dict[str, Any] = response["data"]
#         objects.extend(data["objects"])
#
#         if len(objects) == total:
#             break
#
#         if verbose:
#             print(f"retreived {len(objects)}/{total} items...", end="\r")
#         offset += limit
#
#     if verbose:
#         print(f"retreived {total}/{total} items...{Fore.GREEN}DONE{Style.RESET_ALL}")
#
#     return CountriesData(
#         objects=objects, total=total, timestamp=int(datetime.now().timestamp())
#     )
#
#
# def get_initial_data(file: Path = INIT_DATA_FILE, verbose: bool = True):
#     if file.exists():
#         now = datetime.now()
#         existing_data = load_json(file)
#         last_update = datetime.fromtimestamp(existing_data["meta"]["timestamp"])
#
#         last_updated = now - last_update
#
#         if last_updated.total_seconds() < 3600:
#             print(
#                 f"{Fore.YELLOW}warning: the last update was done only",
#                 f"{format_timedelta(last_updated)} ago!{Style.RESET_ALL}",
#             )
#             user_confirm = (
#                 input("are you sure you want to update again? [y/N]: ").strip().lower()
#             )
#             if user_confirm not in ("y", "yes"):
#                 print("data update cancelled.")
#                 return None
#
#     term_width = get_term_width() if verbose else 80
#     if verbose:
#         print_headline("collecting data...", term_width)
#
#     countries_data_full: CountriesData = get_countries_data(
#         auth=RESTCOUNTRIES_API_AUTH, verbose=verbose
#     )
#
#     print_headline("processing data...", term_width)
#
#     countries_data: list[dict[str, Any]] = countries_data_full["objects"]
#
#     continents: list[str] = []
#     regions: dict[str, list[str]] = {}
#     currencies: list[dict[str, str]] = []
#     languages: list[str] = []
#     countries: list[dict[str, Any]] = []
#
#     for country_data in countries_data:
#         continents_data: list[str] | None = country_data.get("continents")
#         if continents_data:
#             for continent in continents_data:
#                 if continent not in continents:
#                     continents.append(continent)
#
#         region_data: str | None = country_data.get("region")
#         subregion_data: str | None = country_data.get("subregion")
#         if region_data:
#             if region_data not in regions:
#                 if not subregion_data:
#                     if region_data == "Antarctic":
#                         regions[region_data] = [region_data]
#                     else:
#                         regions[region_data] = []
#                 else:
#                     regions[region_data] = [subregion_data]
#             else:
#                 if subregion_data and subregion_data not in regions[region_data]:
#                     regions[region_data].append(subregion_data)
#
#         currencies_data: list[dict[str, str]] | None = country_data.get("currencies")
#         if currencies_data:
#             for currency_data in currencies_data:
#                 if currency_data["code"] not in [c["code"] for c in currencies]:
#                     currencies.append(currency_data)
#
#         languages_data: list[dict[str, str]] | None = country_data.get("languages")
#         if languages_data:
#             langs_names = [ld["name"] for ld in languages_data]
#             for ln in langs_names:
#                 if ln not in languages:
#                     languages.append(ln)
#
#         countries.append(country_data)
#
#     continents.sort()
#     currencies.sort(key=lambda c: c["code"])
#     languages.sort()
#
#     initial_data = {
#         "meta": {
#             "total": countries_data_full["total"],
#             "timestamp": countries_data_full["timestamp"],
#         },
#         "objects": {
#             "continents": continents,
#             "regions": regions,
#             "currencies": currencies,
#             "languages": languages,
#             "countries": countries,
#         },
#     }
#
#     if verbose:
#         print(f"data stored in file: {file}...{Fore.GREEN}DONE{Style.RESET_ALL}")
#
#     save_json(file, initial_data)
#
#
# def insert_continents(data: list[str], session: Session, verbose: bool = True) -> None:
#     id_pad = len(str(len(data)))
#
#     if verbose:
#         print("inserting countries...")
#
#     continents = [Continent(name=d) for d in data]
#     session.add_all(continents)
#     session.commit()
#
#     if verbose:
#         for cont in continents:
#             print(f"INSERT: [continent#{str(cont.id).zfill(id_pad)}] {cont}")
#         print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")
#
#
# def insert_languages(data: list[str], session: Session, verbose: bool = True) -> None:
#     id_pad = len(str(len(data)))
#
#     if verbose:
#         print("inserting languages...")
#
#     languages = [Language(name=d) for d in data]
#
#     session.add_all(languages)
#     session.commit()
#
#     if verbose:
#         for lang in languages:
#             print(f"INSERT: [language#{str(lang.id).zfill(id_pad)}] {lang}")
#         print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")
#
#
# def insert_currencies(
#     data: list[dict[str, str]], session: Session, verbose: bool = True
# ) -> None:
#     id_pad = len(str(len(data)))
#     if verbose:
#         print("inserting currencies...")
#
#     currencies = [Currency(**d) for d in data]
#
#     session.add_all(currencies)
#     session.commit()
#
#     if verbose:
#         for curr in currencies:
#             print(f"INSERT: [currency#{str(curr.id).zfill(id_pad)}] {curr}")
#         print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")
#
#
# def insert_regions_subregions(
#     data: dict[str, list[str]], session: Session, verbose: bool = True
# ) -> None:
#     regions_total = len(data.keys())
#     subregions_total = len(
#         [subregion for subregions in data.values() for subregion in subregions]
#     )
#     id_pad_region, id_pad_subregion = (
#         len(str(regions_total)),
#         len(str(subregions_total)),
#     )
#     if verbose:
#         print("inserting regions and subregions...")
#
#     for k, v in data.items():
#         region = Region(name=k)
#         session.add(region)
#         session.flush()
#         session.refresh(region)
#         if verbose:
#             print(f"INSERT: [region#{str(region.id).zfill(id_pad_region)}] {region}")
#
#         subregions = [Subregion(name=sr, region_id=region.id) for sr in v]
#         session.add_all(subregions)
#         session.commit()
#
#         if verbose:
#             for sr in subregions:
#                 print(
#                     f"INSERT: [subregion#{str(sr.id).zfill(id_pad_subregion)}] {sr} ({region})"
#                 )
#
#     if verbose:
#         print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")
#
#
# def get_country_data(json_data: dict[str, Any], session: Session) -> Country:
#     data = {
#         "name": json_data["names"]["common"],
#         "official_name": json_data["names"]["official"],
#         "code": json_data["codes"]["alpha_2"],
#         "area": float(json_data["area"]["kilometers"]),
#         "tld": json_data["tlds"][0] if len(json_data["tlds"]) > 0 else "",
#         "flag": json_data["flag"]["emoji"],
#         "population": json_data["population"],
#     }
#
#     data["googlemaps"] = json_data["links"]["google_maps"]
#     data["openstreetmaps"] = json_data["links"]["open_street_maps"]
#
#     subregion_name: str = json_data["subregion"]
#     subregion = session.scalar(
#         select(Subregion).where(Subregion.name == subregion_name)
#     )
#     if not subregion:
#         data["subregion_id"] = None
#     else:
#         data["subregion_id"] = subregion.id
#
#     country = Country(**data)
#
#     currency_codes: list[str] = [c["code"] for c in json_data["currencies"]]
#     currencies = session.scalars(
#         select(Currency).where(Currency.code.in_(currency_codes))
#     ).all()
#     country.currencies.extend(currencies)
#
#     languages_names: list[str] = [lang["name"] for lang in json_data["languages"]]
#     with session.no_autoflush:
#         languages = session.scalars(
#             select(Language).where(Language.name.in_(languages_names))
#         ).all()
#         country.languages.extend(languages)
#
#         continents_names: list[str] = [cont for cont in json_data["continents"]]
#         continents = session.scalars(
#             select(Continent).where(Continent.name.in_(continents_names))
#         ).all()
#         country.continents.extend(continents)
#
#     return country
#
#
# def insert_countries(
#     data: list[dict[str, Any]], session: Session, verbose: bool = True
# ) -> None:
#     id_pad = len(str(len(data)))
#     if verbose:
#         print("inserting countries...")
#
#     for cj in data:
#         country = get_country_data(cj, session)
#         session.add(country)
#         session.commit()
#         print(f"INSERT: [country#{str(country.id).zfill(id_pad)}] {country}")
#
#     if verbose:
#         print(f"{Fore.GREEN}DONE{Style.RESET_ALL}")
#
#
# def insert_initial_data(
#     file: Path, session: Session, text_width: int = 80, verbose: bool = True
# ) -> None:
#     if verbose:
#         print_headline("collecting data...", text_width)
#
#     if verbose:
#         print(f"loading data from file {file}...", end="\r")
#     data: dict[str, Any] = load_json(file)
#     if verbose:
#         print(f"loading data from file {file}...{Fore.GREEN}DONE{Style.RESET_ALL}")
#
#     objects: dict[str, Any] = data["objects"]
#
#     if verbose:
#         print_headline("inserting initial data into database...", text_width)
#
#     insert_continents(objects["continents"], session, verbose)
#     insert_languages(objects["languages"], session, verbose)
#     insert_currencies(objects["currencies"], session, verbose)
#     insert_regions_subregions(objects["regions"], session, verbose)
#     insert_countries(objects["countries"], session, verbose)
#
#
# def run_setup(
#     rebuild_db: bool = False,
#     update_init_data: bool = False,
#     insert_testuser: bool = False,
#     verbose: bool = True,
# ):
#     db_file, init_data_file = DB_FILE, INIT_DATA_FILE
#     text_width = 80 if not verbose else get_term_width()
#
#     if verbose:
#         print_headline("citycheck setup", text_width)
#         print(
#             "options:",
#             f"  *rebuild_db:        {rebuild_db}",
#             f"  *update_init_data:  {update_init_data}",
#             f"  *insert_testuser:   {insert_testuser}",
#             sep="\n",
#         )
#         print_headline("starting setup...", text_width)
#
#     if rebuild_db and db_file.exists():
#         if verbose:
#             print(f"deleting database file: {db_file}...", end="\r")
#         db_file.unlink()
#         if verbose:
#             print(
#                 f"deleting database file: {db_file}...{Fore.GREEN}DONE{Style.RESET_ALL}",
#             )
#     if not INIT_DATA_FILE.exists() or update_init_data:
#         if verbose:
#             print("creating/updating init data...")
#         get_initial_data(init_data_file)
#
#     print_headline("initializing database...", text_width)
#
#     db = init_db(db_file)
#     if verbose:
#         if rebuild_db:
#             print(
#                 f"database (re-)created at {db_file}...{Fore.GREEN}DONE{Style.RESET_ALL}"
#             )
#         print(f"database initialized...{Fore.GREEN}DONE{Style.RESET_ALL}")
#
#     with db.get_session() as Session:
#         insert_initial_data(
#             file=init_data_file, session=Session, text_width=text_width, verbose=verbose
#         )
#
#         if insert_testuser:
#             if verbose:
#                 print("inserting testuser...", end="\r")
#             testuser = User(username="testuser", email="testuser@example.com")
#             Session.add(testuser)
#             Session.commit()
#             if verbose:
#                 print(f"inserting testuser...{Fore.GREEN}DONE{Style.RESET_ALL}")
#                 print(f"INSERT: [user#{testuser.id}] {testuser} ({testuser.email})")
#
#     if verbose:
#         print_headline(
#             "initial data inserted successfully. setup finished.",
#             text_width,
#             color="green",
#         )
#
#
# def main() -> None:
#     run_setup(
#         rebuild_db=True, update_init_data=True, insert_testuser=True, verbose=True
#     )
#
#
# if __name__ == "__main__":
#     main()
