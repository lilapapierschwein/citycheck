import re
from pathlib import Path
from time import sleep
from typing import Literal

from citycheck.api.main import main as api_main
from citycheck.core.utils import get_current_datetime, validate_file
from citycheck.core.utils.utils import api_is_running, init_api_shutdown
from citycheck.settings import APP_CONFIG

PROG = "citycheck"
VERSION = "0.1.0"


def start_api(port: int | None = None) -> None:
    is_running, msg = api_is_running()
    if is_running:
        print(f"API is already running (status: {repr(msg)})")
        return

    print(f"Starting API on port {port or 8000}...")
    api_main()


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


def create_db_backup(
    db_file: Path = APP_CONFIG.files.paths.db, suffix: Literal[".bak"] | None = ".bak"
) -> Path | None:
    try:
        _ = validate_file(db_file)
        backup_dir = db_file.parent / "backups" / "db"
        if not backup_dir.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)

        ts = re.sub(r"[-:]", "", get_current_datetime(microseconds=False).isoformat())
        backup_file_path = backup_dir / f"{db_file.stem}_{ts}{db_file.suffix}{suffix or ''}"
        backup_file = db_file.copy(backup_file_path)

        if not backup_file.exists():
            raise FileNotFoundError(f"Backup could not be verified at {repr(str(backup_file))}")
        return backup_file
    except (FileNotFoundError, ValueError) as err:
        print("error:", err)
