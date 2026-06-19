from .index import router as web_index_router
from .settings import router as web_settings_router
from .weather import router as web_weather_router

__all__ = ["web_index_router", "web_weather_router", "web_settings_router"]
