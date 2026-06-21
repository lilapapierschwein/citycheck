import json
import os
import tomllib
from datetime import datetime as dt
from datetime import timedelta as td
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError


def validate_file(file: Path, suffix: str | None = None) -> bool:
    if not file.exists():
        raise FileNotFoundError(f"File {file} does not exist.")
    if not file.is_file():
        raise ValueError(f"{file} is not a file.")
    if suffix and file.suffix.lower() != suffix.lower():
        raise ValueError(f"File {file} is not a {suffix} file.")
    return True


def load_toml_data(file: Path) -> Any:
    try:
        _ = validate_file(file, suffix=".toml")
        with file.open("rb") as f:
            return tomllib.load(f)
    except Exception as err:
        print(f"Error loading file: {err}")


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


def get_env_var(name: str, dotenv_file: Path | None) -> str:
    if dotenv_file:
        _ = validate_file(dotenv_file)
        _ = load_dotenv(dotenv_file)
    v = os.getenv(name, None)
    if v is None:
        raise RuntimeError(f"Unable to load env var: {name!r}")
    return v


def get_current_datetime(microseconds: bool = True) -> dt:
    return dt.now() if microseconds else dt.now().replace(microsecond=0)


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


def get_project_root(
    root_markers: list[str],
    file: Path | None = None,
    project_name: str | None = None,
    user_home: Path | None = None,
) -> Path:
    file, user_home = file or Path.cwd(), user_home or Path.home()

    if file.is_dir() and (
        any((file / rm).exists() for rm in root_markers) or file.name == project_name
    ):
        return file

    for fp in file.parents:
        if fp == user_home:
            break
        if any((fp / rm).exists() for rm in root_markers) or fp.name == project_name:
            return fp
    raise RuntimeError("Unable to find project root.")


def api_is_running(url: str = "http://localhost:8000/api/v1/health") -> tuple[bool, str]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.status_code == 200, response.json()["status"]
    except ConnectionError as err:
        return False, str(err)


def init_api_shutdown(url: str = "http://localhost:8000/api/v1/shutdown") -> tuple[bool, str]:
    try:
        response = requests.post(url)
        response.raise_for_status()
        return response.status_code == 200, response.json()["message"]
    except Exception as err:
        return False, str(err)
