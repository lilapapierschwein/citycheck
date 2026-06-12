import json
from pathlib import Path
from typing import Any


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
