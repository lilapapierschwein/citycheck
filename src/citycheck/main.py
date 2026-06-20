# from citycheck.core.cli.main import run_cli


from citycheck.api.models.country import CountryCreate, CountryIn
from citycheck.db.db import init_db
from citycheck.db.models import Country

germany_data = {
    "names": {"common": "Germany", "official": "Federal Republic of Germany"},
    "codes": {"alpha_2": "DE"},
    "flag": {"emoji": "🇩🇪"},
    "region": "Europe",
    "subregion": "Western Europe",
    "area": {"kilometers": 357114},
    "continents": ["Europe"],
    "currencies": [{"code": "EUR", "name": "Euro", "symbol": "€"}],
    "languages": [{"name": "German"}],
    "links": {
        "google_maps": "https://goo.gl/maps/mD9FBMq1nvXUBrkv6",
        "open_street_maps": "https://www.openstreetmap.org/relation/51477",
    },
    "population": 83497147,
    "tlds": [".de"],
    "_meta": {"lastUpdatedTimestamp": 1781804758},
}

paliwood = {
    "names": {"common": "Palestine", "official": "State of Palestine"},
    "codes": {"alpha_2": "PS"},
    "flag": {"emoji": "🇵🇸"},
    "region": "Asia",
    "subregion": "Western Asia",
    "area": {"kilometers": 6220},
    "continents": ["Asia"],
    "currencies": [
        {"code": "EGP", "name": "Egyptian pound", "symbol": "E£"},
        {"code": "ILS", "name": "Israeli new shekel", "symbol": "₪"},
        {"code": "JOD", "name": "Jordanian dinar", "symbol": "JD"},
    ],
    "languages": [{"name": "Arabic"}],
    "links": {
        "google_maps": "https://goo.gl/maps/QvTbkRdmdWEoYAmt5",
        "open_street_maps": "https://www.openstreetmap.org/relation/1703814",
    },
    "population": 5483450,
    "tlds": [".ps", "فلسطين."],
    "_meta": {"lastUpdatedTimestamp": 1781804766},
}

antarctica = {
    "names": {"common": "Antarctica", "official": "Antarctica"},
    "codes": {"alpha_2": "AQ"},
    "flag": {"emoji": "🇦🇶"},
    "region": "Antarctic",
    "subregion": "",
    "area": {"kilometers": 14000000},
    "continents": ["Antarctica"],
    "currencies": [],
    "languages": [],
    "links": {
        "google_maps": "https://goo.gl/maps/kyBuJriu4itiXank7",
        "open_street_maps": "https://www.openstreetmap.org/node/36966060",
    },
    "population": 1300,
    "tlds": [".aq"],
    "_meta": {"lastUpdatedTimestamp": 1781804763},
}


def run_stuff() -> None:
    try:
        country_in = CountryIn.model_validate(antarctica)
        db = init_db()
        with db.get_session() as Session:
            _ = country_in.get_junctions(Session)
        country_create = CountryCreate.model_validate(country_in.model_dump())
        _ = Country(**country_create.model_dump())
    except Exception as err:
        print("error:", err)


def main() -> None:
    run_stuff()
    # print(APP_CONFIG)

    # db = init_db()
    # with db.get_session() as Session:
    #     countries = Session.scalars(select(Country.code)).all()
    #     codes: dict[str, tuple[str, str, int]] = {}
    #
    #     nope: list[str] = []
    #     for c in countries:
    #         d = get_request(GEOCODING_API, params={"name": c, "count": 1})
    #         res = d.get("results", None)
    #         if not res or not isinstance(res, list):
    #             nope.append(c)
    #             continue
    #         data = res[0]
    #         codes[c] = (
    #             data.get("name", None),
    #             data.get("country_code", None),
    #             data.get("country_id", None),
    #         )
    #
    # cwd = Path.cwd()
    # with open(cwd / "codes2.json", "w", encoding="utf-8") as f:
    #     json.dump(codes, f, ensure_ascii=False, indent=2)
    #
    # if nope:
    #     with open(cwd / "nope2.json", "w", encoding="utf-8") as f:
    #         json.dump(nope, f, ensure_ascii=False, indent=2)

    # print("\n".join(countries))

    # run_cli()
    # backup = create_db_backup()
    # if not backup:
    #     return None
    # print(f"database backup successfully created at ./{backup.relative_to(ROOT)}")

    # cfg = AppConfigNew.model_validate(load_toml_data(Path.cwd() / "cfg.toml"))
    # print(cfg.root)
    # root = get_project_root(Path.cwd(), cfg.files.root_markers, cfg.general.app_name, Path.home())
