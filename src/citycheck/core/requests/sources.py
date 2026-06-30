from dataclasses import dataclass
from typing import Literal

from citycheck import get_config

app_config = get_config()


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
RESTCOUNTRIES_API_AUTH = APIAuth(token=app_config.secrets.restcountries_api)
