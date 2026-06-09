import uvicorn
from fastapi import FastAPI

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

app = FastAPI()

for router in [
    continents_router,
    countries_router,
    currencies_router,
    languages_router,
    locations_router,
    regions_router,
    subregions_router,
    users_router,
]:
    app.include_router(router)


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
