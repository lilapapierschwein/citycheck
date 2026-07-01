import asyncio


from citycheck import get_config
from citycheck.api.crud import create_user_location, read_user
from citycheck.api.models.user import UserLocationCreate
from citycheck.db.db import init_db

app_config = get_config()

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


# def run_stuff() -> None:
#     try:
#         country_in = CountryIn.model_validate(antarctica)
#         db = init_db()
#         with db.get_session() as Session:
#             _ = country_in.get_junctions(Session)
#         country_create = CountryCreate.model_validate(country_in.model_dump())
#         _ = Country(**country_create.model_dump())
#     except Exception as err:
#         print("error:", err)


# def format_validation_error(err: ValidationError) -> str:
#     title, count, errors = err.title, err.error_count, err.errors()
#     fmt: list[str] = [
#         f"{'1 validation error' if count == 1 else f'{count} validation errors'} for {title}"
#     ]
#     for e in errors:
#         loc = ":".join(e["loc"])
#         fmt.append("")


async def create_loc():
    # pw = "NaziPunks#66*%!!"
    # print(password_is_valid(pw))
    db = init_db()
    with db.get_session() as Session:
        user = await read_user(1, Session)
        if not user:
            print("no user")
            return

        _ = await create_user_location(
            UserLocationCreate.model_validate({"user_id": 1, "location_id": 2}), Session
        )

        # le = await read_locations(Session)
        # await delete_user(user.id, Session)

        # await delete_user(user.id, Session)
        #     testuser = await read_user(1, Session)
        #     if not testuser:
        #         print("no user found")
        #         return None
        #
        #     print(testuser.home_location)
        #
        #     for loc in testuser.user_locations:
        #         print(loc)

        # if not testuser:
        #     print("no user found")
        #     return None
        # print(testuser)
        #
        # hal = await read_location(2, Session)
        # if not hal:
        #     print("no location found")
        #     return None
        # print(hal)
        #
        # user_location = await create_user_location(
        #     UserLocationCreate(user_id=testuser.id, location_id=hal.id), Session
        # )
        # print(user_location)

        # halle = Session.scalar()
        # hal_req = get_request(
        #     GEOCODING_API,
        #     params={"name": "Leipzig", "count": 1},
        # )
        # hal_data = hal_req["results"][0]
        # pprint(hal_data)
        # country = await read_country_by_code(hal_data["country_code"], Session)
        # if not country:
        #     return None
        # hal_data["country_id"] = country.id
        # hal_in = LocationCreate.model_validate(hal_data, from_attributes=True)
        # hal = await create_location(hal_in, Session)
        # print(hal)
    return None


def run_stuff() -> None:
    asyncio.run(create_loc())


def main() -> None:
    run_stuff()
    # pw = "test_passwort@123!!"
    # hash = hash_password(pw)
    # print("hash:", hash)
    # print(
    #     verify_password(
    #         "test_passwort@123!!",
    #         "$argon2id$v=19$m=65536,t=3,p=4$soGpNcfLKPZy9hHP/5+v9A$PZd79f85lEnVx00SRpN/+RSDoYNLlyF2pSErQKwgNzY",
    #     )
    # )

    # generate_env_file = EnvFileGenerator()
    # generate_env_file()

    ...
    # run_stuff()
    # try:
    #     config = Config()  # pyright: ignore[reportCallIssue]
    #     print(config.security)
    # except ValidationError as err:
    #     print("error:", err)
    # print(config, APP_CONFIG, sep="\n\n")

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
