import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from citycheck.api.routers import ROUTERS
from citycheck.settings import ROOT, STATIC_DIR

APP_CONFIG = {"title": "citycheck", "version": "0.1.0"}


def get_app(
    api_routers: list[APIRouter],
    web_routers: list[APIRouter],
    title: str = "citycheck",
    version: str = "0.1.0",
) -> FastAPI:
    app = FastAPI(title=title, version=version, docs_url="/api/v1/docs")

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    for router in api_routers:
        app.include_router(router, prefix="/api/v1")

    for router in web_routers:
        app.include_router(router)

    return app


app = get_app(**ROUTERS, **APP_CONFIG)


def main() -> None:
    uvicorn.run(
        app="main:app",
        app_dir=str(ROOT / "src" / "citycheck" / "api"),
        port=8000,
    )


if __name__ == "__main__":
    main()
