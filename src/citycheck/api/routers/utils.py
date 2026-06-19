from typing import TypedDict

from fastapi import APIRouter


class RoutersDict(TypedDict):
    api_routers: list[APIRouter]
    web_routers: list[APIRouter]
