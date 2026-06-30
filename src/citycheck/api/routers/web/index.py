from fastapi import APIRouter, Request

from citycheck.api.security import WebCurrentUser
from citycheck.api.utils import HxReq
from citycheck.db.models import User
from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/")
async def home(request: Request, current_user: WebCurrentUser, is_hx: HxReq):
    if not current_user:
        return templates.TemplateResponse(request, "login/index.html", status_code=303)

    template = "index/_index_page.html" if is_hx else "index/index.html"
    context: dict[str, User | bool] = {"user": current_user}
    response = templates.TemplateResponse(request, template, context=context, status_code=200)
    # if sum([1 for act in current_user.activities if act.id == UserAction.LOGIN], 0) <= 1:
    #     response.headers["is_new_user"] = "1"
    return response
