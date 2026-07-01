from fastapi import APIRouter, Request

from citycheck.api.crud.user_location import read_user_locations_by_user
from citycheck.api.filters_forms.user_location import UserLocationQueryFilters
from citycheck.api.security import CredentialsException, WebCurrentUser
from citycheck.api.utils import CRUDSession, HxReq
from citycheck.db.models import Location, User
from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/")
async def home(
    request: Request,
    current_user: WebCurrentUser,
    is_hx: HxReq,
    session: CRUDSession,
    filters: UserLocationQueryFilters,
):
    if not current_user:
        return templates.TemplateResponse(request, "login/index.html", status_code=303)

    template = "index/_index_page.html" if is_hx else "index/index.html"

    locations = [loc.location for loc in current_user.user_locations]
    if filters.q:
        locations_result = await read_user_locations_by_user(current_user, filters, session)
        locations = [loc.location for loc in locations_result]

    context: dict[str, User | list[Location] | UserLocationQueryFilters] = {
        "user": current_user,
        "locations": locations,
        "filters": filters,
    }
    response = templates.TemplateResponse(request, template, context=context, status_code=200)
    return response


@router.get("/user/locations")
async def get_user_locations(
    request: Request,
    user: WebCurrentUser,
    filters: UserLocationQueryFilters,
    session: CRUDSession,
):
    if not user:
        raise CredentialsException

    locations = await read_user_locations_by_user(user, filters, session)

    return templates.TemplateResponse(
        request,
        name="index/_index_user_locations.html",
        context={"locations": locations},
        status_code=200,
    )
