import re
from pathlib import Path
from time import sleep
from typing import Literal

from citycheck import app_config
from citycheck.api.main import main as api_main
from citycheck.core.utils import get_current_datetime, validate_file
from citycheck.core.utils.utils import api_is_running, init_api_shutdown

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
    db_file: Path = app_config.paths.files.db,
    backup_dir: Path = app_config.paths.directories.db_backups,
    backup_name: str | None = None,
    suffix: Literal[".bak"] | None = ".bak",
    remove_existing: bool = False,
) -> Path | None:
    try:
        _ = validate_file(db_file)
        if not backup_dir.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)

        if remove_existing:
            root = app_config.paths.root
            for f in backup_dir.iterdir():
                if f.is_file() and ".db" in f.name and (suffix and (f.suffix == suffix)):
                    f.unlink()
                    print(f"file removed: ./{f.relative_to(root)}")

        ts = re.sub(r"[-:]", "", get_current_datetime(microseconds=False).isoformat())
        name = backup_name or f"{db_file.stem}_{ts}"
        backup_file_path = backup_dir / f"{name}{db_file.suffix}{suffix or ''}"
        backup_file = db_file.copy(backup_file_path)

        if not backup_file.exists():
            raise FileNotFoundError(f"Backup could not be verified at {repr(str(backup_file))}")
        return backup_file
    except (FileNotFoundError, ValueError) as err:
        print("error:", err)
