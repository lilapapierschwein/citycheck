import uvicorn
from fastapi import FastAPI

from citycheck.api.routers import (
    currencies_router,
    languages_router,
    regions_router,
    subregions_router,
    users_router,
)
from citycheck.settings import ROOT

app = FastAPI()

for router in [
    users_router,
    regions_router,
    subregions_router,
    languages_router,
    currencies_router,
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
