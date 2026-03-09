from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from mailglyph.client import AsyncMailGlyph, MailGlyph
from mailglyph.exceptions import ValidationError


def parse_request_json(route: respx.Route) -> dict[str, object]:
    return json.loads(route.calls.last.request.content.decode("utf-8"))


VERIFY_VALID_RESPONSE = {
    "success": True,
    "data": {
        "email": "user@gmail.com",
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
        "reasons": ["Email appears to be valid"],
    },
}


@respx.mock
def test_send_simple_string_to_from() -> None:
    client = MailGlyph("sk_test")
    route = respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": {
                    "emails": [
                        {"contact": {"id": "ct_1", "email": "user@example.com"}, "email": "em_1"}
                    ],
                    "timestamp": "2026-01-01T00:00:00Z",
                },
            },
        )
    )

    result = client.emails.send(
        to="user@example.com",
        from_="hello@example.com",
        subject="Hello",
        body="<h1>Hello</h1>",
    )

    assert result.emails[0].email == "em_1"
    request_payload = parse_request_json(route)
    assert request_payload["to"] == "user@example.com"
    assert request_payload["from"] == "hello@example.com"
    client.close()


@respx.mock
def test_send_object_to_from_with_names() -> None:
    client = MailGlyph("sk_test")
    route = respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(200, json={"success": True, "data": {"emails": [], "timestamp": "t"}})
    )

    client.emails.send(
        to={"name": "Jane", "email": "jane@example.com"},
        from_={"name": "App", "email": "hello@example.com"},
        subject="Welcome",
        body="<p>Hi</p>",
    )

    request_payload = parse_request_json(route)
    assert isinstance(request_payload["to"], dict)
    assert isinstance(request_payload["from"], dict)
    assert request_payload["to"]["name"] == "Jane"
    assert request_payload["from"]["name"] == "App"
    client.close()


@respx.mock
def test_send_array_of_recipients() -> None:
    client = MailGlyph("sk_test")
    route = respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(200, json={"success": True, "data": {"emails": [], "timestamp": "t"}})
    )

    client.emails.send(
        to=["one@example.com", {"email": "two@example.com", "name": "Two"}],
        from_="hello@example.com",
        subject="Update",
        body="<p>Hi</p>",
    )

    request_payload = parse_request_json(route)
    assert isinstance(request_payload["to"], list)
    assert len(request_payload["to"]) == 2
    client.close()


@respx.mock
def test_send_template_with_data() -> None:
    client = MailGlyph("sk_test")
    route = respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(200, json={"success": True, "data": {"emails": [], "timestamp": "t"}})
    )

    client.emails.send(
        to="user@example.com",
        from_="hello@example.com",
        template="tmpl_123",
        data={"name": "John"},
    )

    request_payload = parse_request_json(route)
    assert request_payload["template"] == "tmpl_123"
    assert isinstance(request_payload["data"], dict)
    assert request_payload["data"]["name"] == "John"
    client.close()


@respx.mock
def test_send_with_attachments() -> None:
    client = MailGlyph("sk_test")
    route = respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(200, json={"success": True, "data": {"emails": [], "timestamp": "t"}})
    )

    client.emails.send(
        to="user@example.com",
        from_="hello@example.com",
        subject="Invoice",
        body="<p>Attached</p>",
        attachments=[
            {
                "filename": "invoice.pdf",
                "content": "JVBERi0xLjQK",
                "contentType": "application/pdf",
            }
        ],
    )

    request_payload = parse_request_json(route)
    assert isinstance(request_payload["attachments"], list)
    assert request_payload["attachments"][0]["filename"] == "invoice.pdf"
    client.close()


@respx.mock
def test_send_includes_text_when_provided() -> None:
    client = MailGlyph("sk_test")
    route = respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(200, json={"success": True, "data": {"emails": [], "timestamp": "t"}})
    )

    client.emails.send(
        to="user@example.com",
        from_="hello@example.com",
        subject="Welcome",
        body="<p>Hello</p>",
        text="Hello",
    )

    request_payload = parse_request_json(route)
    assert request_payload["text"] == "Hello"
    client.close()


@respx.mock
def test_send_omits_text_when_undefined() -> None:
    client = MailGlyph("sk_test")
    route = respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(200, json={"success": True, "data": {"emails": [], "timestamp": "t"}})
    )

    client.emails.send(
        to="user@example.com",
        from_="hello@example.com",
        subject="Welcome",
        body="<p>Hello</p>",
    )

    request_payload = parse_request_json(route)
    assert "text" not in request_payload
    client.close()


@respx.mock
def test_send_includes_empty_text_string() -> None:
    client = MailGlyph("sk_test")
    route = respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(200, json={"success": True, "data": {"emails": [], "timestamp": "t"}})
    )

    client.emails.send(
        to="user@example.com",
        from_="hello@example.com",
        subject="Welcome",
        body="<p>Hello</p>",
        text="",
    )

    request_payload = parse_request_json(route)
    assert request_payload["text"] == ""
    client.close()


@respx.mock
def test_send_validation_error_missing_to() -> None:
    client = MailGlyph("sk_test")
    respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(400, json={"message": "to is required"})
    )

    with pytest.raises(ValidationError):
        client.emails.send(to=None, from_="hello@example.com")  # type: ignore[arg-type]

    client.close()


@respx.mock
def test_verify_valid_email_full_result() -> None:
    client = MailGlyph("sk_test")
    respx.post("https://api.mailglyph.com/v1/verify").mock(
        return_value=Response(200, json=VERIFY_VALID_RESPONSE)
    )

    result = client.emails.verify("user@gmail.com")

    assert result.valid is True
    assert result.is_random_input is False
    client.close()


@respx.mock
def test_verify_typo_with_suggestion() -> None:
    client = MailGlyph("sk_test")
    respx.post("https://api.mailglyph.com/v1/verify").mock(
        return_value=Response(
            200,
            json={
                "success": True,
                "data": {
                    "email": "user@gmial.com",
                    "valid": False,
                    "isDisposable": False,
                    "isAlias": False,
                    "isTypo": True,
                    "isPlusAddressed": False,
                    "isRandomInput": False,
                    "isPersonalEmail": False,
                    "domainExists": False,
                    "hasWebsite": False,
                    "hasMxRecords": False,
                    "suggestedEmail": "user@gmail.com",
                    "reasons": ["Possible typo detected"],
                },
            },
        )
    )

    result = client.emails.verify("user@gmial.com")

    assert result.is_typo is True
    assert result.suggested_email == "user@gmail.com"
    client.close()


@respx.mock
def test_verify_validation_error() -> None:
    client = MailGlyph("sk_test")
    respx.post("https://api.mailglyph.com/v1/verify").mock(
        return_value=Response(400, json={"message": "invalid email"})
    )

    with pytest.raises(ValidationError):
        client.emails.verify("invalid")

    client.close()


@pytest.mark.asyncio
@respx.mock
async def test_async_send_and_verify() -> None:
    send_route = respx.post("https://api.mailglyph.com/v1/send").mock(
        return_value=Response(200, json={"success": True, "data": {"emails": [], "timestamp": "t"}})
    )
    verify_route = respx.post("https://api.mailglyph.com/v1/verify").mock(
        return_value=Response(200, json=VERIFY_VALID_RESPONSE)
    )

    async with AsyncMailGlyph("sk_test") as client:
        await client.emails.send(to="user@example.com", from_="hello@example.com")
        verification = await client.emails.verify("user@gmail.com")

    assert send_route.called
    assert verify_route.called
    assert verification.valid is True
