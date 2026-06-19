from .api import (
    continents_router,
    countries_router,
    currencies_router,
    languages_router,
    locations_router,
    misc_router,
    regions_router,
    subregions_router,
    users_router,
)
from .utils import RoutersDict
from .web import web_index_router, web_settings_router, web_weather_router

ROUTERS = RoutersDict(
    api_routers=[
        continents_router,
        countries_router,
        currencies_router,
        languages_router,
        locations_router,
        regions_router,
        subregions_router,
        users_router,
        misc_router,
    ],
    web_routers=[web_index_router, web_weather_router, web_settings_router],
)
