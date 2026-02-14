from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from mailrify.client import AsyncMailrify, Mailrify
from mailrify.exceptions import AuthenticationError


def parse_request_json(route: respx.Route) -> dict[str, object]:
    return json.loads(route.calls.last.request.content.decode("utf-8"))


@respx.mock
def test_track_simple_event() -> None:
    client = Mailrify("pk_test")
    route = respx.post("https://api.mailrify.com/v1/track").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": {"contact": "ct_1", "event": "ev_1", "timestamp": "2026-01-01T00:00:00Z"},
            },
        )
    )

    result = client.events.track(email="user@example.com", event="purchase")

    assert result.contact == "ct_1"
    assert parse_request_json(route)["event"] == "purchase"
    client.close()


@respx.mock
def test_track_with_custom_data() -> None:
    client = Mailrify("pk_test")
    route = respx.post("https://api.mailrify.com/v1/track").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": {"contact": "ct_1", "event": "ev_1", "timestamp": "2026-01-01T00:00:00Z"},
            },
        )
    )

    client.events.track(email="user@example.com", event="purchase", data={"amount": 99})

    payload = parse_request_json(route)
    assert isinstance(payload["data"], dict)
    assert payload["data"]["amount"] == 99
    client.close()


def test_track_rejects_sk_key() -> None:
    client = Mailrify("sk_test")
    with pytest.raises(AuthenticationError):
        client.events.track(email="user@example.com", event="purchase")
    client.close()


@respx.mock
def test_list_names_returns_names_array() -> None:
    client = Mailrify("sk_test")
    respx.get("https://api.mailrify.com/events/names").mock(
        return_value=Response(200, json={"eventNames": ["purchase", "signup"]})
    )

    names = client.events.get_names()

    assert names == ["purchase", "signup"]
    client.close()


def test_list_names_rejects_pk_key() -> None:
    client = Mailrify("pk_test")
    with pytest.raises(AuthenticationError):
        client.events.get_names()
    client.close()


@pytest.mark.asyncio
@respx.mock
async def test_async_track_and_get_names() -> None:
    respx.post("https://api.mailrify.com/v1/track").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": {"contact": "ct_1", "event": "ev_1", "timestamp": "2026-01-01T00:00:00Z"},
            },
        )
    )

    async with AsyncMailrify("pk_test") as client:
        result = await client.events.track(email="user@example.com", event="purchase")

    assert result.event == "ev_1"
