from fastapi import APIRouter, Request

from citycheck.web.templates import templates

router = APIRouter(tags=["web"])


@router.get("/weather")
async def weather_page(
    request: Request,
    # session: CRUDSession,
    # is_hx: HxReq,
):
    template = "weather/index.html"
    return templates.TemplateResponse(
        request,
        template,
    )
