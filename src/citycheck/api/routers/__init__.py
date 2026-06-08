from .currencies import router as currencies_router
from .languages import router as languages_router
from .regions import regions_router as regions_router
from .regions import subregions_router as subregions_router
from .users import router as users_router

__all__ = [
    "users_router",
    "subregions_router",
    "regions_router",
    "languages_router",
    "currencies_router",
]
