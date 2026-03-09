from __future__ import annotations

import pytest
import respx
from httpx import Response

from mailglyph.client import MailGlyph
from mailglyph.exceptions import (
    ApiError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from mailglyph.http_client import HttpClient


@respx.mock
def test_bearer_auth_and_user_agent_headers() -> None:
    client = MailGlyph("sk_test_123")
    route = respx.post("https://api.mailglyph.com/v1/verify").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": {
                    "email": "user@example.com",
                    "valid": True,
                    "isDisposable": False,
                    "isAlias": False,
                    "isTypo": False,
                    "isPlusAddressed": False,
                    "isRandomInput": False,
                    "isPersonalEmail": True,
                    "domainExists": True,
                    "hasWebsite": True,
                    "hasMxRecords": True,
                    "reasons": ["ok"],
                },
            },
        )
    )

    client.emails.verify("user@example.com")

    assert route.called
    request = route.calls.last.request
    assert request.headers["Authorization"] == "Bearer sk_test_123"
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["User-Agent"].startswith("mailglyph-python/")
    client.close()


@respx.mock
def test_custom_base_url_and_timeout() -> None:
    client = MailGlyph("sk_test_123", base_url="https://example.local", timeout=5.0)
    route = respx.post("https://example.local/v1/verify").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": {
                    "email": "user@example.com",
                    "valid": True,
                    "isDisposable": False,
                    "isAlias": False,
                    "isTypo": False,
                    "isPlusAddressed": False,
                    "isRandomInput": False,
                    "isPersonalEmail": True,
                    "domainExists": True,
                    "hasWebsite": True,
                    "hasMxRecords": True,
                    "reasons": ["ok"],
                },
            },
        )
    )

    client.emails.verify("user@example.com")

    assert route.called
    client.close()


@pytest.mark.parametrize(
    ("status_code", "exc_type"),
    [
        (400, ValidationError),
        (401, AuthenticationError),
        (404, NotFoundError),
        (429, RateLimitError),
        (500, ApiError),
    ],
)
@respx.mock
def test_error_mapping(status_code: int, exc_type: type[Exception]) -> None:
    http_client = HttpClient("sk_test")
    respx.post("https://api.mailglyph.com/v1/verify").mock(
        return_value=Response(
            status_code,
            json={"error": "bad", "message": "problem", "code": status_code},
        )
    )

    with pytest.raises(exc_type):
        http_client.request("POST", "/v1/verify", json_body={"email": "x@example.com"})

    http_client.close()


@respx.mock
def test_retry_on_429_and_respects_retry_after(monkeypatch: pytest.MonkeyPatch) -> None:
    http_client = HttpClient("sk_test", max_retries=2)
    monkeypatch.setattr("mailglyph.http_client.time.sleep", lambda _: None)

    route = respx.post("https://api.mailglyph.com/v1/verify").mock(
        side_effect=[
            Response(429, headers={"Retry-After": "0"}, json={"message": "rate limited"}),
            Response(
                200,
                json={
                    "success": True,
                    "data": {
                        "email": "user@example.com",
                        "valid": True,
                        "isDisposable": False,
                        "isAlias": False,
                        "isTypo": False,
                        "isPlusAddressed": False,
                        "isRandomInput": False,
                        "isPersonalEmail": True,
                        "domainExists": True,
                        "hasWebsite": True,
                        "hasMxRecords": True,
                        "reasons": ["ok"],
                    },
                },
            ),
        ]
    )

    payload = http_client.request("POST", "/v1/verify", json_body={"email": "user@example.com"})
    assert payload["success"] is True
    assert route.call_count == 2
    http_client.close()


def test_pk_key_restriction_for_non_track_endpoint() -> None:
    client = MailGlyph("pk_test")
    with pytest.raises(AuthenticationError):
        client.events.get_names()
    client.close()


def test_sk_key_restriction_for_track_endpoint() -> None:
    client = MailGlyph("sk_test")
    with pytest.raises(AuthenticationError):
        client.events.track(email="user@example.com", event="purchase")
    client.close()
