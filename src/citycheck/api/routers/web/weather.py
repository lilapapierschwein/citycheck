from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from citycheck.api.security import WebCurrentUser
from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/weather")
async def weather_page(
    request: Request,
    current_user: WebCurrentUser,
    # session: CRUDSession,
    # is_hx: HxReq,
):
    if not current_user:
        return RedirectResponse("/", status_code=303)
    template = "weather/index.html"
    return templates.TemplateResponse(
        request, template, context={"user": current_user, "page_name": "weather"}
    )
