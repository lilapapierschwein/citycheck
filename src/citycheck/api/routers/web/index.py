from fastapi import APIRouter, Request

from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})
