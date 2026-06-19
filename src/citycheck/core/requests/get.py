from typing import Any

import requests

from .sources import SourceAPI


def get_request(
    api: SourceAPI,
    uid: str | None = None,
    params: dict[str, Any] | None = None,
    headers: dict[str, Any] | None = None,
) -> Any:
    url = api.url if uid is None else f"{api.url}/{uid}"
    response = requests.get(url=url, params=params, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    return response.json()
