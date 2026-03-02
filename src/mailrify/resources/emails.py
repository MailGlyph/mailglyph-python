from __future__ import annotations

from typing import Any

from ..http_client import HttpClient
from ..models import SendEmailResult, VerifyEmailResult
from ._utils import compact_dict, unwrap_data


class EmailsResource:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def send(
        self,
        *,
        to: str | dict[str, Any] | list[str | dict[str, Any]],
        from_: str | dict[str, Any],
        subject: str | None = None,
        body: str | None = None,
        text: str | None = None,
        template: str | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        reply: str | None = None,
        attachments: list[dict[str, str]] | None = None,
        subscribed: bool | None = None,
        name: str | None = None,
    ) -> SendEmailResult:
        """Send a transactional email.

        Args:
            text: The plain text version of the message.
                If not provided, the `body` will be used to generate a plain
                text version. You can opt out of this behavior by setting value
                to an empty string.
        """
        payload = compact_dict(
            {
                "to": to,
                "from": from_,
                "subject": subject,
                "body": body,
                "text": text,
                "template": template,
                "data": data,
                "headers": headers,
                "reply": reply,
                "attachments": attachments,
                "subscribed": subscribed,
                "name": name,
            }
        )
        response = self._http_client.request("POST", "/v1/send", json_body=payload)
        return SendEmailResult.model_validate(unwrap_data(response))

    def verify(self, email: str) -> VerifyEmailResult:
        response = self._http_client.request("POST", "/v1/verify", json_body={"email": email})
        return VerifyEmailResult.model_validate(unwrap_data(response))


class AsyncEmailsResource:
    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    async def send(
        self,
        *,
        to: str | dict[str, Any] | list[str | dict[str, Any]],
        from_: str | dict[str, Any],
        subject: str | None = None,
        body: str | None = None,
        text: str | None = None,
        template: str | None = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        reply: str | None = None,
        attachments: list[dict[str, str]] | None = None,
        subscribed: bool | None = None,
        name: str | None = None,
    ) -> SendEmailResult:
        """Send a transactional email.

        Args:
            text: The plain text version of the message.
                If not provided, the `body` will be used to generate a plain
                text version. You can opt out of this behavior by setting value
                to an empty string.
        """
        payload = compact_dict(
            {
                "to": to,
                "from": from_,
                "subject": subject,
                "body": body,
                "text": text,
                "template": template,
                "data": data,
                "headers": headers,
                "reply": reply,
                "attachments": attachments,
                "subscribed": subscribed,
                "name": name,
            }
        )
        response = await self._http_client.arequest("POST", "/v1/send", json_body=payload)
        return SendEmailResult.model_validate(unwrap_data(response))

    async def verify(self, email: str) -> VerifyEmailResult:
        response = await self._http_client.arequest(
            "POST", "/v1/verify", json_body={"email": email}
        )
        return VerifyEmailResult.model_validate(unwrap_data(response))
