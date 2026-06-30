from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from citycheck.api.security import WebCurrentUser
from citycheck.api.utils import HxReq
from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/settings")
async def settings_page(request: Request, is_hx: HxReq, current_user: WebCurrentUser):
    if not current_user:
        return RedirectResponse("/login", status_code=303)
    template = "settings/_user_data.html" if is_hx else "settings/index.html"
    return templates.TemplateResponse(
        request, template, context={"page_name": "settings", "user": current_user}
    )
