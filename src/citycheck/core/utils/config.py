from pathlib import Path
from typing import Annotated, Any, TypedDict, override

from pydantic import (
    BaseModel,
    BeforeValidator,
    Field,
    field_serializer,
)
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    EnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from .utils import get_project_root


class APIDefaults(TypedDict):
    version: str
    port: int


def find_config_file(pattern: str, allow_multiple: bool = False) -> Path:
    candidates: list[Path] = list(Path.cwd().rglob(pattern=pattern))
    # for p in Path.cwd().rglob(pattern=pattern):
    #     cfg_file = p
    #     break
    if not candidates:
        raise RuntimeError(f"No config file found matching pattern {repr(pattern)}.")
    if candidates and len(candidates) != 1:
        if allow_multiple:
            return candidates[0]
        raise RuntimeError(
            f"Multiple config files found matching pattern {repr(pattern)}: {[str(p) for p in candidates]}.\n"
            + "Make sure there is only one config file matching the pattern in the CWD and/or its subdirectories."
        )
    return candidates[0]


# def load_app_config(file: Path) -> AppConfigBase:
#     cfg_data = load_toml_data(file)
#     return AppConfigBase.model_validate(cfg_data)


# def get_app_config_base(filename: str, allow_multiple: bool = False) -> AppConfigBase:
#     file = find_config_file(filename, allow_multiple=allow_multiple)
#     return load_app_config(file)


# def get_app_config(base: AppConfigBase) -> AppConfig:
#     root = base.root
#
#     base_dirs_dump: dict[str, str] = base.files.dirs.model_dump()
#     dirs_paths = AppDirectories.model_validate({k: (root / v) for k, v in base_dirs_dump.items()})
#
#     base_files_dump: dict[str, str] = base.files.paths.model_dump()
#     fpaths = {k: (root / v) for k, v in base_files_dump.items()}
#     fpaths["root"] = root
#     filepaths = AppFilePaths.model_validate(fpaths)
#
#     app_files = AppFiles(root_markers=base.files.root_markers, dirs=dirs_paths, paths=filepaths)
#
#     return AppConfig(general=base.general, files=app_files, api=base.api)


# def load_config(filename: str, allow_multiple: bool = False) -> AppConfig:
#     """Load the app config from a file and return an AppConfig instance.
#
#     Args:
#         filename (`str`): The name of the configuration file to load.
#         allow_multiple (`bool`): If True, allows multiple config files to match the pattern. This will result in the
#                                first match being selected if more than 1 file is found. Defaults to False.
#     Returns:
#         `AppConfig`: An instance of AppConfig containing the loaded configuration.
#
#     Raises:
#         `RuntimeError`: If the configuration file cannot be found or loaded.
#     """
#     base_config = get_app_config_base(filename, allow_multiple)
#     return get_app_config(base_config)


def validate_path(obj: object) -> Path:
    if not isinstance(obj, (str, Path)):
        raise TypeError(f"File object must be of type `str` or `Path`, found {type(obj)!r}")
    return obj if isinstance(obj, Path) else Path(obj)


ValidPath = Annotated[Path, BeforeValidator(validate_path)]


class Secrets(BaseModel):
    restcountries_api: str = Field(validation_alias="restcountries_api_key")

    @field_serializer("restcountries_api")
    def serialize_secrets(self, s: str) -> str:
        return "???" if len(s) == 0 else "xxx"


class GeneralConfig(BaseModel):
    app_name: str = Field(default="citycheck")
    version: str = Field(pattern=r"^[0-9]+(\.{1}[0-9]+){0,2}$")


class Security(BaseModel):
    jwt_secret_key: str
    jwt_algorithm: str

    @field_serializer("jwt_secret_key", "jwt_algorithm")
    def serialize_secrets(self, s: str) -> str:
        return "???" if len(s) == 0 else "xxx"


class DirectoriesConfig(BaseModel):
    data: ValidPath
    backups: ValidPath
    db_backups: ValidPath
    src: ValidPath
    api: ValidPath
    web: ValidPath
    static: ValidPath
    templates: ValidPath


class FilesConfig(BaseModel):
    config: ValidPath
    db: ValidPath
    init_data: ValidPath
    dotenv: ValidPath


class PathsConfig(BaseModel):
    root_markers: list[str]
    root: Path = Field(default_factory=lambda data: get_project_root(data["root_markers"]))

    directories: DirectoriesConfig
    files: FilesConfig

    @override
    def model_post_init(self, context: Any, /) -> None:
        for field in self.directories.model_fields_set:
            d = getattr(self.directories, field)
            setattr(self.directories, field, self.root / d)
        for field in self.files.model_fields_set:
            d = getattr(self.files, field)
            setattr(self.files, field, self.root / d)


class ApiConfigVersions(BaseModel):
    available: list[str] = Field(min_length=1, default=["1"])
    default: str = Field(pattern=r"^[0-9]+(\.{1}[0-9]+){0,2}$")


class ApiConfigSettings(BaseModel):
    access_token_expire_minutes: int = Field(ge=1, le=1440, default=30)


class ApiConfigPorts(BaseModel):
    min: int = Field(ge=1024, le=49151, default=8000)
    max: int = Field(ge=1024, le=49151, default=8080)
    default: int = Field(ge=1024, le=49151, default=8000)

    @override
    def model_post_init(self, context: Any, /) -> None:
        if self.max < self.min:
            raise RuntimeError(
                f"Max port number ({self.max}) cannot be greater than min port number ({self.min})"
            )
        if not (self.min <= self.default <= self.max):
            raise RuntimeError(
                f"Default port number ({self.default}) must be within range {self.min}–{self.max}"
            )
        return None


class ApiConfig(BaseModel):
    prefix: str = Field(default="api")
    versions: ApiConfigVersions
    ports: ApiConfigPorts
    settings: ApiConfigSettings


class Config(BaseSettings):
    general: GeneralConfig
    secrets: Secrets
    security: Security
    paths: PathsConfig
    api: ApiConfig

    model_config: SettingsConfigDict = SettingsConfigDict(  # pyright: ignore[reportIncompatibleVariableOverride]
        env_file="t.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        toml_file="config.toml",
    )

    @override
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            # order determines evaluation priority
            EnvSettingsSource(settings_cls),
            DotEnvSettingsSource(settings_cls),
            TomlConfigSettingsSource(settings_cls),
        )


app_config = Config()  # pyright: ignore[reportCallIssue]
