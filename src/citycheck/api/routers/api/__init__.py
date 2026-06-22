from .auth import router as auth_router
from .continents import router as continents_router
from .countries import router as countries_router
from .currencies import router as currencies_router
from .languages import router as languages_router
from .locations import router as locations_router
from .misc import router as misc_router
from .regions import regions_router as regions_router
from .regions import subregions_router as subregions_router
from .users import router as users_router

__all__ = [
    "locations_router",
    "continents_router",
    "users_router",
    "countries_router",
    "subregions_router",
    "regions_router",
    "languages_router",
    "currencies_router",
    "misc_router",
    "auth_router",
]
