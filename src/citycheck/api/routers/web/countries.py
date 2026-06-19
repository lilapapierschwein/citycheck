from fastapi import APIRouter, Request

from citycheck.api import crud
from citycheck.api.filters_forms.countries import CountryQueryFilters
from citycheck.api.utils import CRUDSession, HxReq
from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/countries")
async def countries_page(
    request: Request,
    session: CRUDSession,
    query_params: CountryQueryFilters,
    is_hx: HxReq,
):
    query_params.limit = -1
    countries, _ = await crud.read_countries(session, query_params)
    template = "countries/_list.html" if is_hx else "countries/index.html"
    return templates.TemplateResponse(request, template, {"countries": countries})
