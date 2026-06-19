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
    api_version: str = "1",
    api_router_name: str | None = "api",
) -> FastAPI:
    api_prefix = f"/{api_router_name}/v{api_version}" if api_router_name else f"/v{api_version}"
    app = FastAPI(title=title, version=version, docs_url=f"{api_prefix}/docs")

    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    for router in api_routers:
        app.include_router(router, prefix=api_prefix)

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
