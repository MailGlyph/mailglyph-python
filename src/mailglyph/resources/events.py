from __future__ import annotations

from typing import Any

from ..http_client import HttpClient
from ..models import TrackEventResult
from ._utils import compact_dict, unwrap_data


class EventsResource:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def track(
        self,
        *,
        email: str,
        event: str,
        data: dict[str, Any] | None = None,
        subscribed: bool | None = None,
    ) -> TrackEventResult:
        payload = compact_dict(
            {
                "email": email,
                "event": event,
                "data": data,
                "subscribed": subscribed,
            }
        )
        response = self._http_client.request("POST", "/v1/track", json_body=payload)
        return TrackEventResult.model_validate(unwrap_data(response))

    def get_names(self) -> list[str]:
        response = self._http_client.request("GET", "/events/names")
        if not isinstance(response, dict):
            return []
        names = response.get("eventNames", [])
        if not isinstance(names, list):
            return []
        return [name for name in names if isinstance(name, str)]


class AsyncEventsResource:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    async def track(
        self,
        *,
        email: str,
        event: str,
        data: dict[str, Any] | None = None,
        subscribed: bool | None = None,
    ) -> TrackEventResult:
        payload = compact_dict(
            {
                "email": email,
                "event": event,
                "data": data,
                "subscribed": subscribed,
            }
        )
        response = await self._http_client.arequest("POST", "/v1/track", json_body=payload)
        return TrackEventResult.model_validate(unwrap_data(response))

    async def get_names(self) -> list[str]:
        response = await self._http_client.arequest("GET", "/events/names")
        if not isinstance(response, dict):
            return []
        names = response.get("eventNames", [])
        if not isinstance(names, list):
            return []
        return [name for name in names if isinstance(name, str)]
