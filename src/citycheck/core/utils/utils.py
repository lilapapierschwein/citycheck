import json
import os
import tomllib
from datetime import datetime as dt
from datetime import timedelta as td
from pathlib import Path
from typing import Any, TypedDict

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from requests.exceptions import ConnectionError


def validate_file(file: Path, suffix: str | None = None) -> bool:
    if not file.exists():
        raise FileNotFoundError(f"File {file} does not exist.")
    if not file.is_file():
        raise ValueError(f"{file} is not a file.")
    if suffix and file.suffix.lower() != suffix.lower():
        raise ValueError(f"File {file} is not a {suffix} file.")
    return True


class APIDefaults(TypedDict):
    version: str
    port: int


class DefaultConfigs(TypedDict):
    api: APIDefaults


class AppConfig(BaseModel):
    data_dir: str = Field(pattern=r"^[-a-zA-Z0-9_]+$", validation_alias="data_dir_name")
    init_data_file: str = Field(
        pattern=r"^[-a-zA-Z0-9_]+\.json$", validation_alias="init_data_file_name"
    )
    dotenv_file: str = Field(pattern=r"^[-a-zA-Z0-9_]?\.env$", validation_alias="dotenv_file_name")
    default_api_version: str = Field(pattern=r"^[0-9]+(\.{1}[0-9]+){0,2}$", default="1")
    default_api_port: int = Field(ge=3000, le=9999, default=8000)

    @property
    def defaults(self) -> DefaultConfigs:
        return {"api": {"version": self.default_api_version, "port": self.default_api_port}}


def load_toml_data(file: Path) -> Any:
    try:
        _ = validate_file(file, suffix=".toml")
        with file.open("rb") as f:
            return tomllib.load(f)
    except Exception as err:
        print(f"Error loading file: {err}")


def load_app_config(file: Path) -> AppConfig:
    cfg_data = load_toml_data(file)
    return AppConfig.model_validate(cfg_data)


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


def get_project_root(
    file: Path, root_markers: list[str], project_name: str, user_home: Path
) -> Path:
    if not file.is_dir():
        file = file.parent

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
