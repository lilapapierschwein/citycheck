from dataclasses import dataclass
from typing import Literal

from citycheck import app_config
from citycheck.core.utils import get_env_var


@dataclass
class SourceAPI:
    base_url: str
    api_version: str
    endpoint: str | None = None

    @property
    def url(self) -> str:
        if not self.endpoint:
            return f"{self.base_url}/v{self.api_version}"
        return f"{self.base_url}/v{self.api_version}/{self.endpoint}"


@dataclass
class APIAuth:
    token: str
    auth_type: Literal["Bearer"] = "Bearer"
    content_type: Literal["application/json"] = "application/json"

    @property
    def header(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": self.content_type,
        }


GEOCODING_API = SourceAPI("https://geocoding-api.open-meteo.com", "1", "search")
FORECAST_API = SourceAPI("https://api.open-meteo.com", "1", "forecast")
HISTORICAL_WEATHER_API = SourceAPI("https://archive-api.open-meteo.com", "1", "archive")
SEASONAL_FORECAST_API = SourceAPI("https://seasonal-api.open-meteo.com", "1", "seasonal")

RESTCOUNTRIES_API = SourceAPI("https://api.restcountries.com/countries", "5")

rc_api_token = get_env_var("RESTCOUNTRIES_API_KEY", app_config.paths.files.dotenv)
if not rc_api_token:
    raise RuntimeError("Unable to retreive restcountries api token")
RESTCOUNTRIES_API_AUTH = APIAuth(token=rc_api_token)
