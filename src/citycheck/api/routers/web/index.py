from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from citycheck.api.security import WebCurrentUser
from citycheck.api.utils import CRUDSession
from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/")
async def home(request: Request, session: CRUDSession, current_user: WebCurrentUser):
    if not current_user:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request, "index/index.html", {"user": current_user})
