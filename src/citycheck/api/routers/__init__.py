from .api import (
    auth_router,
    continents_router,
    countries_router,
    currencies_router,
    languages_router,
    locations_router,
    misc_router,
    regions_router,
    subregions_router,
    users_router,
    users_locations_router,
)
from .utils import RoutersDict
from .web import web_auth_router, web_index_router, web_settings_router, web_weather_router

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
        users_locations_router,
        misc_router,
        auth_router,
    ],
    web_routers=[web_index_router, web_weather_router, web_settings_router, web_auth_router],
)
