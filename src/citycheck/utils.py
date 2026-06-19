from pathlib import Path


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
