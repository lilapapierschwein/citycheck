from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from citycheck.api.security import create_access_token, verify_credentials
from citycheck.api.utils import CRUDSession
from citycheck.web.templates import templates

router = APIRouter(tags=["web", "auth"])


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login/index.html", {})


@router.post("/login")
async def login_submit(request: Request, session: CRUDSession):
    form = await request.form()
    user = await verify_credentials(str(form["username"]), str(form["password"]), session)
    if not user:
        return templates.TemplateResponse(
            request, "login/index.html", {"error": "Invalid credentials"}, status_code=401
        )
    token = create_access_token({"sub": user.username})
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie("access_token", token, httponly=True, samesite="lax")
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response
