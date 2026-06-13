from fastapi import APIRouter, Request

from citycheck.api import crud
from citycheck.api.filters_forms import CountryQueryFilters
from citycheck.api.utils import CRUDSession, HxReq
from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


@router.get("/countries")
async def countries_page(
    request: Request,
    session: CRUDSession,
    query_params: CountryQueryFilters,
    is_hx: HxReq,
):
    countries = await crud.read_countries(session, query_params)
    template = "countries/_list.html" if is_hx else "countries/index.html"
    return templates.TemplateResponse(request, template, {"countries": countries})
