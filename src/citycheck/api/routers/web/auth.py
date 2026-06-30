from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse

from citycheck.api.crud import create_user
from citycheck.api.crud.user import add_user_activity, get_user_by_username, set_password
from citycheck.api.models.user import UserCreate
from citycheck.api.security import (
    WebCurrentUser,
    create_access_token,
    hash_password,
    password_is_valid,
    verify_credentials,
)
from citycheck.api.utils import CRUDSession, HxReq
from citycheck.core.utils.enums import UserAction
from citycheck.db.models import User
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
    _ = await add_user_activity(user, UserAction.LOGIN, session)
    return response


@router.get("/logout")
async def logout(request: Request, current_user: WebCurrentUser, session: CRUDSession):
    if not current_user:
        response = RedirectResponse(url="/login", status_code=303)
        if request.cookies.get("access_token"):
            response.delete_cookie("access_token")
        return response

    template = "logout/index.html"
    response = templates.TemplateResponse(
        request, template, context={"page_name": "logout", "redirect_seconds": 15}
    )
    response.delete_cookie("access_token")
    _ = await add_user_activity(current_user, UserAction.LOGOUT, session)
    return response


@router.get("/signup")
async def signup_page(request: Request):
    template = "signup/index.html"
    response = templates.TemplateResponse(request, template, context={"page_name": "Signup"})
    return response


@router.post("/signup")
async def signup_submit(request: Request, session: CRUDSession):
    target, status_code = "signup/index.html", 400
    context: dict[str, str | User | bool | None] = {"page_name": "Signup"}
    form = await request.form()

    username = str(form["username"])
    if await get_user_by_username(username, session):
        context["error"] = "username is already taken"
        return templates.TemplateResponse(
            request, target, context=context, status_code=status_code
        )

    pw, pw_confirm = str(form["password"]), str(form["password2"])
    if pw != pw_confirm:
        context["error"] = "passwords do not match"
        return templates.TemplateResponse(
            request, target, context=context, status_code=status_code
        )

    if not password_is_valid(pw):
        print("invalid password")
        context["error"] = "password is invalid"
        return templates.TemplateResponse(
            request, target, context=context, status_code=status_code
        )

    user = await create_user(
        UserCreate.model_validate({"username": username, "email": f"{username}@example.com"}),
        session,
    )
    pw_hash = hash_password(pw)

    _ = await set_password(user, pw_hash, session)
    token = create_access_token({"sub": user.username})
    target, status_code = "/", 303

    response = RedirectResponse("/", status_code=303)

    response.set_cookie("access_token", token, httponly=True, samesite="lax")
    _ = await add_user_activity(user, UserAction.SIGNUP, session)
    return response


@router.get("/redirect")
async def redirect(request: Request, is_hx: HxReq):
    target = "/"
    if is_hx:
        current_url = request.headers.get("hx-current-url", "/")
        if current_url.endswith("/logout"):
            target = "/"
    return Response(headers={"HX-Redirect": target})
