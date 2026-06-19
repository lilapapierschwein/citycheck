from fastapi import APIRouter, Request

from citycheck.api.crud import read_user
from citycheck.api.filters_forms.users import UserQueryFilters
from citycheck.api.utils import CRUDSession, HxReq
from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/settings")
async def settings_page(
    request: Request, session: CRUDSession, query_params: UserQueryFilters, is_hx: HxReq
):
    user = await read_user(1, session)

    template = "settings/_user_data.html" if is_hx else "settings/index.html"
    return templates.TemplateResponse(request, template, context={"user": user})
