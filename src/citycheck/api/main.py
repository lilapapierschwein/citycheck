import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from citycheck import get_config
from citycheck.api.routers import ROUTERS

app_config = get_config()

API_CONFIG = {"title": "citycheck", "version": "0.1.0"}


def get_app(
    api_routers: list[APIRouter],
    web_routers: list[APIRouter],
    title: str = app_config.app_name,
    version: str = "0.1.0",
    api_version: str = app_config.api.versions.default,
    api_router_name: str | None = "api",
) -> FastAPI:
    api_prefix = f"/{api_router_name}/v{api_version}" if api_router_name else f"/v{api_version}"
    app = FastAPI(title=title, version=version, docs_url=f"{api_prefix}/docs")

    app.mount("/static", StaticFiles(directory=app_config.paths.directories.static), name="static")

    for router in api_routers:
        app.include_router(router, prefix=api_prefix)

    for router in web_routers:
        app.include_router(router)

    return app


app = get_app(**ROUTERS, **API_CONFIG)


def main() -> None:

    uvicorn.run(
        app="main:app",
        app_dir=str(app_config.paths.directories.api),
        port=app_config.api.ports.default,
    )


if __name__ == "__main__":
    main()
