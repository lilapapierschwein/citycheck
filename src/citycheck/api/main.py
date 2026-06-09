import uvicorn
from fastapi import APIRouter, FastAPI

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
from citycheck.settings import ROOT

APP_CONFIG = {"title": "citycheck", "version": "0.1.0"}

ROUTERS = [
    continents_router,
    countries_router,
    currencies_router,
    languages_router,
    locations_router,
    regions_router,
    subregions_router,
    users_router,
]


def get_app(
    routers: list[APIRouter], title: str = "citycheck", version: str = "0.1.0"
) -> FastAPI:
    app = FastAPI(title=title, version=version)
    for router in routers:
        app.include_router(router)
    return app


app = get_app(ROUTERS, **APP_CONFIG)


@app.get("/")
async def get_root():
    return {"Hello": "citycheck"}


def main() -> None:
    uvicorn.run(
        app="main:app",
        app_dir=str(ROOT / "src" / "citycheck" / "api"),
        port=8000,
    )


if __name__ == "__main__":
    main()
