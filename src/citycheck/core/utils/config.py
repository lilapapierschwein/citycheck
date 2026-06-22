import sys
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


def validate_path(obj: object) -> Path:
    if not isinstance(obj, (str, Path)):
        raise TypeError(f"File object must be of type `str` or `Path`, found {type(obj)!r}")
    return obj if isinstance(obj, Path) else Path(obj)


ValidPath = Annotated[Path, BeforeValidator(validate_path)]


class GeneralConfig(BaseModel):
    app_name: str = Field(default="citycheck")
    version: str = Field(pattern=r"^[0-9]+(\.{1}[0-9]+){0,2}$")


class Secrets(BaseModel):
    restcountries_api: str = Field(
        validation_alias="restcountries_api_key", pattern=r"^rc_live_[0-9a-z]+$"
    )

    @field_serializer("restcountries_api")
    def serialize_secrets(self, s: str) -> str:
        return "???" if len(s) == 0 else "xxx"


class Security(BaseModel):
    jwt_secret_key: str = Field(pattern=r"^[0-9a-z]{64}$")
    jwt_algorithm: str = Field(pattern=r"^HS(256|384|512)$", default="HS256")

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
        env_file=".env",
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


def get_config() -> Config:
    try:
        cfg = Config()  # pyright: ignore[reportCallIssue]
        return cfg
    except RuntimeError as err:
        print("error:", err)
        sys.exit(1)
    except Exception as err:
        print("error:", err)
        sys.exit(1)


app_config = get_config()
