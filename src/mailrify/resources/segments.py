from __future__ import annotations

from typing import Any

from ..http_client import HttpClient
from ..models import FilterCondition, Segment, SegmentContactsPage
from ._utils import compact_dict


def _serialize_filter_condition(
    condition: FilterCondition | dict[str, Any] | None,
) -> dict[str, Any] | None:
    if condition is None:
        return None
    if isinstance(condition, FilterCondition):
        return condition.model_dump(by_alias=True, exclude_none=True)
    return condition


class SegmentsResource:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def list(self) -> list[Segment]:
        response = self._http_client.request("GET", "/segments")
        if not isinstance(response, list):
            return []
        return [Segment.model_validate(item) for item in response]

    def create(
        self,
        *,
        name: str,
        condition: FilterCondition | dict[str, Any],
        description: str | None = None,
        track_membership: bool | None = None,
    ) -> Segment:
        payload = compact_dict(
            {
                "name": name,
                "description": description,
                "condition": _serialize_filter_condition(condition),
                "trackMembership": track_membership,
            }
        )
        response = self._http_client.request("POST", "/segments", json_body=payload)
        return Segment.model_validate(response)

    def get(self, segment_id: str) -> Segment:
        response = self._http_client.request("GET", f"/segments/{segment_id}")
        return Segment.model_validate(response)

    def update(
        self,
        segment_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        condition: FilterCondition | dict[str, Any] | None = None,
        track_membership: bool | None = None,
    ) -> Segment:
        payload = compact_dict(
            {
                "name": name,
                "description": description,
                "condition": _serialize_filter_condition(condition),
                "trackMembership": track_membership,
            }
        )
        response = self._http_client.request("PATCH", f"/segments/{segment_id}", json_body=payload)
        return Segment.model_validate(response)

    def delete(self, segment_id: str) -> None:
        self._http_client.request("DELETE", f"/segments/{segment_id}")

    def list_contacts(
        self,
        segment_id: str,
        *,
        page: int | None = None,
        page_size: int | None = None,
    ) -> SegmentContactsPage:
        params = compact_dict({"page": page, "pageSize": page_size})
        response = self._http_client.request(
            "GET", f"/segments/{segment_id}/contacts", params=params
        )
        return SegmentContactsPage.model_validate(response)


class AsyncSegmentsResource:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    async def list(self) -> list[Segment]:
        response = await self._http_client.arequest("GET", "/segments")
        if not isinstance(response, list):
            return []
        return [Segment.model_validate(item) for item in response]

    async def create(
        self,
        *,
        name: str,
        condition: FilterCondition | dict[str, Any],
        description: str | None = None,
        track_membership: bool | None = None,
    ) -> Segment:
        payload = compact_dict(
            {
                "name": name,
                "description": description,
                "condition": _serialize_filter_condition(condition),
                "trackMembership": track_membership,
            }
        )
        response = await self._http_client.arequest("POST", "/segments", json_body=payload)
        return Segment.model_validate(response)

    async def get(self, segment_id: str) -> Segment:
        response = await self._http_client.arequest("GET", f"/segments/{segment_id}")
        return Segment.model_validate(response)

    async def update(
        self,
        segment_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        condition: FilterCondition | dict[str, Any] | None = None,
        track_membership: bool | None = None,
    ) -> Segment:
        payload = compact_dict(
            {
                "name": name,
                "description": description,
                "condition": _serialize_filter_condition(condition),
                "trackMembership": track_membership,
            }
        )
        response = await self._http_client.arequest(
            "PATCH",
            f"/segments/{segment_id}",
            json_body=payload,
        )
        return Segment.model_validate(response)

    async def delete(self, segment_id: str) -> None:
        await self._http_client.arequest("DELETE", f"/segments/{segment_id}")

    async def list_contacts(
        self,
        segment_id: str,
        *,
        page: int | None = None,
        page_size: int | None = None,
    ) -> SegmentContactsPage:
        params = compact_dict({"page": page, "pageSize": page_size})
        response = await self._http_client.arequest(
            "GET",
            f"/segments/{segment_id}/contacts",
            params=params,
        )
        return SegmentContactsPage.model_validate(response)
