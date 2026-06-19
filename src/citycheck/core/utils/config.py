from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, override

from pydantic import BaseModel, Field, computed_field

from .utils import load_toml_data


class APIDefaults(TypedDict):
    version: str
    port: int


class DefaultConfigs(TypedDict):
    api: APIDefaults


class FileConfig(BaseModel):
    data_dir: str = Field(pattern=r"^[-a-zA-Z0-9_]+$", validation_alias="data_dir_name")
    init_data_file: str = Field(
        pattern=r"^[-a-zA-Z0-9_]+\.json$", validation_alias="init_data_file_name"
    )
    dotenv_file: str = Field(pattern=r"^[-a-zA-Z0-9_]?\.env$", validation_alias="dotenv_file_name")


class APIConfig(BaseModel):
    default_version: str = Field(pattern=r"^[0-9]+(\.{1}[0-9]+){0,2}$", default="1")
    default_port: int = Field(ge=3000, le=9999, default=8000)


class GeneralConfig(BaseModel):
    app_name: str = Field(r"^\S+$")

    @override
    def __str__(self) -> str:
        return self.app_name

    @override
    def __repr__(self) -> str:
        return f"GeneralConfig(app_name={repr(self.app_name)})"


class FileConfigDirs(BaseModel):
    data: str
    backups: str
    src: str
    web: str
    static: str
    templates: str


@dataclass
class FullPaths:
    config: Path
    db: Path
    init_data: Path
    dotenv: Path


class FileConfigPaths(BaseModel):
    config: str
    db: str
    init_data: str
    dotenv: str

    def get_full_paths(self, root: Path) -> FullPaths:
        return FullPaths(
            config=root / self.config,
            db=root / self.db,
            init_data=root / self.init_data,
            dotenv=root / self.dotenv,
        )


class AppFileConfig(BaseModel):
    root_markers: list[str] = Field(min_length=1)
    dirs: FileConfigDirs
    paths: FileConfigPaths

    def get_root(self, p: Path | None = None, project_name: str | None = None) -> Path:
        path, user_home = p or Path.cwd(), Path.home()
        if path.is_dir():
            if path == user_home:
                raise RuntimeError("Unable to find project's root directory.")
            if any((path / rm).exists() for rm in self.root_markers) or (
                project_name and (path.name == project_name)
            ):
                return path

        for fp in path.parents:
            if fp == user_home:
                break
            if any((fp / rm).exists() for rm in self.root_markers) or (
                project_name and project_name == fp.name
            ):
                return fp
        raise RuntimeError("Unable to find project's root directory.")


class ApiConfig(BaseModel):
    versions: list[str] = Field(min_length=1)
    default_version: str
    min_port: int
    max_port: int
    default_port: int

    @property
    def defaults(self) -> APIDefaults:
        return {"version": self.default_version, "port": self.default_port}


class AppConfigBase(BaseModel):
    general: GeneralConfig
    files: AppFileConfig
    api: ApiConfig

    @computed_field
    @property
    def root(self) -> Path:
        return self.files.get_root(project_name=self.general.app_name)

    @property
    def app_name(self) -> str:
        return self.general.app_name


class AppDirectories(BaseModel):
    data: Path
    backups: Path
    src: Path
    web: Path
    static: Path
    templates: Path


class AppFilePaths(BaseModel):
    root: Path
    config: Path
    db: Path
    init_data: Path
    dotenv: Path


class AppFiles(BaseModel):
    root_markers: list[str] = Field(min_length=1)
    dirs: AppDirectories
    paths: AppFilePaths


class AppConfig(BaseModel):
    general: GeneralConfig
    files: AppFiles
    api: ApiConfig


def find_config_file(pattern: str) -> Path:
    cfg_file: Path | None = None
    for p in Path.cwd().rglob(pattern=pattern):
        cfg_file = p
        break
    if not cfg_file:
        raise RuntimeError(f"Unable to locate config file {repr(pattern)}")
    return cfg_file


def load_app_config(file: Path) -> AppConfigBase:
    cfg_data = load_toml_data(file)
    return AppConfigBase.model_validate(cfg_data)


def get_app_config_base(filename: str) -> AppConfigBase:
    file = find_config_file(filename)
    return load_app_config(file)


def get_app_config(base: AppConfigBase) -> AppConfig:
    root = base.root

    base_dirs_dump: dict[str, str] = base.files.dirs.model_dump()
    dirs_paths = AppDirectories.model_validate({k: (root / v) for k, v in base_dirs_dump.items()})

    base_files_dump: dict[str, str] = base.files.paths.model_dump()
    fpaths = {k: (root / v) for k, v in base_files_dump.items()}
    fpaths["root"] = root
    filepaths = AppFilePaths.model_validate(fpaths)

    app_files = AppFiles(root_markers=base.files.root_markers, dirs=dirs_paths, paths=filepaths)

    return AppConfig(general=base.general, files=app_files, api=base.api)


def load_config(filename: str) -> AppConfig:
    base_config = get_app_config_base(filename)
    return get_app_config(base_config)
