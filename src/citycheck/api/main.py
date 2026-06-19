import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from citycheck.api.routers import ROUTERS
from citycheck.settings import APP_CONFIG

API_CONFIG = {"title": "citycheck", "version": "0.1.0"}

# args = parse_args()


def get_app(
    api_routers: list[APIRouter],
    web_routers: list[APIRouter],
    title: str = APP_CONFIG.general.app_name,
    version: str = "0.1.0",
    api_version: str = APP_CONFIG.api.default_version,
    api_router_name: str | None = "api",
) -> FastAPI:
    api_prefix = f"/{api_router_name}/v{api_version}" if api_router_name else f"/v{api_version}"
    app = FastAPI(title=title, version=version, docs_url=f"{api_prefix}/docs")

    app.mount("/static", StaticFiles(directory=APP_CONFIG.files.dirs.static), name="static")

    for router in api_routers:
        app.include_router(router, prefix=api_prefix)

    for router in web_routers:
        app.include_router(router)

    return app


app = get_app(**ROUTERS, **API_CONFIG)


def main() -> None:
    uvicorn.run(
        app="main:app",
        app_dir=str(APP_CONFIG.files.paths.root / "src" / "citycheck" / "api"),
        port=APP_CONFIG.api.default_port,
    )


if __name__ == "__main__":
    main()
