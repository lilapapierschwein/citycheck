from dataclasses import dataclass


@dataclass
class SourceAPI:
    base_url: str
    api_version: str
    endpoint: str

    @property
    def url(self) -> str:
        return f"{self.base_url}/v{self.api_version}/{self.endpoint}"


GEOCODING_API = SourceAPI("https://geocoding-api.open-meteo.com", "1", "search")
FORECAST_API = SourceAPI("https://api.open-meteo.com", "1", "forecast")
HISTORICAL_WEATHER_API = SourceAPI("https://archive-api.open-meteo.com", "1", "archive")
SEASONAL_FORECAST_API = SourceAPI(
    "https://seasonal-api.open-meteo.com", "1", "seasonal"
)

RESTCOUNTRIES_API_NAME = SourceAPI("https://restcountries.com", "3.1", "name")
RESTCOUNTRIES_API_CODE = SourceAPI("https://restcountries.com", "3.1", "alpha")
