import json
import os
from datetime import datetime as dt
from datetime import timedelta as td
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from citycheck.settings import DOTENV_FILE


def validate_file(file: Path, suffix: str | None = None) -> bool:
    if not file.exists():
        raise FileNotFoundError(f"File {file} does not exist.")
    if not file.is_file():
        raise ValueError(f"{file} is not a file.")
    if suffix and file.suffix.lower() != suffix.lower():
        raise ValueError(f"File {file} is not a {suffix} file.")
    return True


def load_json(file: Path) -> Any:
    try:
        _ = validate_file(file, suffix=".json")
        with file.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as err:
        print(f"Error loading file: {err}")


def save_json(file: Path, data: Any) -> None:
    try:
        with file.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as err:
        print(f"Error saving file: {err}")


def get_env_var(name: str, dotenv_file: Path | None = DOTENV_FILE) -> str:
    if dotenv_file:
        _ = validate_file(dotenv_file)
        _ = load_dotenv(dotenv_file)
    v = os.getenv(name, None)
    if v is None:
        raise RuntimeError(f"Unable to load env var: {name!r}")
    return v


def get_current_datetime() -> dt:
    return dt.now()


def get_timestamp() -> float:
    return dt.now().timestamp()


def format_timedelta(t: td) -> str:
    fmt: list[str] = []

    seconds = int(t.total_seconds())
    if seconds >= 86400:
        days = seconds // 86400
        fmt.append(f"{days}d")
        seconds = seconds % 86400
    if seconds >= 3600:
        hours = seconds // 3600
        fmt.append(f"{hours}h")
        seconds = seconds % 3600
    if seconds >= 60:
        minutes = seconds // 60
        fmt.append(f"{minutes}m")
        seconds = seconds % 60
    fmt.append(f"{seconds}s")

    return " ".join(fmt)
