from fastapi import APIRouter, BackgroundTasks

from citycheck.api.utils import shutdown

router = APIRouter(prefix="", tags=["api"])


@router.get("/health", status_code=200)
async def check_health() -> dict[str, str]:
    return {"status": "healthy"}


@router.post("/shutdown")
async def shutdown_server(background_tasks: BackgroundTasks) -> dict[str, str]:
    background_tasks.add_task(shutdown)
    return {"message": "Server shutting down..."}
