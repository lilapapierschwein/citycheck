from time import sleep

from citycheck.api.main import main as api_main
from citycheck.core.utils.utils import api_is_running, init_api_shutdown

PROG = "citycheck"
VERSION = "0.1.0"


def start_api(port: int | None = None) -> None:
    is_running, msg = api_is_running()
    if is_running:
        print(f"API is already running (status: {repr(msg)})")
        return

    print(f"Starting API on port {port or 8000}...")
    api_main(port)


def shutdown_api() -> None:
    is_running, msg = api_is_running()
    if not is_running:
        print("api is not running")
        return
    print("Shutting down server...")

    is_shutting_down, msg = init_api_shutdown()
    if is_shutting_down:
        print(msg)
    else:
        print("error:", msg)
        return

    while True:
        sleep(1)
        is_running, msg = api_is_running()
        if not is_running:
            print("Server shutdown successfully.")
            break
        print("error:", msg)
    return None
