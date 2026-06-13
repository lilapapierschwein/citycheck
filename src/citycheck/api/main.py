import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from citycheck.api.routers import (
    continents_router,
    countries_router,
    currencies_router,
    languages_router,
    locations_router,
    regions_router,
    subregions_router,
    users_router,
)
from citycheck.settings import ROOT, STATIC_DIR
from citycheck.web.routers import countries_router as web_countries_router

APP_CONFIG = {"title": "citycheck", "version": "0.1.0"}

API_ROUTERS = [
    continents_router,
    countries_router,
    currencies_router,
    languages_router,
    locations_router,
    regions_router,
    subregions_router,
    users_router,
]

WEB_ROUTERS = [web_countries_router]


def get_app(
    api_routers: list[APIRouter],
    web_routers: list[APIRouter],
    title: str = "citycheck",
    version: str = "0.1.0",
) -> FastAPI:
    app = FastAPI(title=title, version=version)

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    for router in api_routers:
        app.include_router(router, prefix="/api")

    for router in web_routers:
        app.include_router(router)

    return app


app = get_app(API_ROUTERS, WEB_ROUTERS, **APP_CONFIG)


def main() -> None:
    uvicorn.run(
        app="main:app",
        app_dir=str(ROOT / "src" / "citycheck" / "api"),
        port=8000,
    )


if __name__ == "__main__":
    main()
