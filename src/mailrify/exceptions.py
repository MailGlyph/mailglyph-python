from __future__ import annotations

from typing import Any


class MailrifyError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        payload: Any = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload


class AuthenticationError(MailrifyError):
    pass


class ValidationError(MailrifyError):
    pass


class NotFoundError(MailrifyError):
    pass


class RateLimitError(MailrifyError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        payload: Any = None,
        retry_after: float | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, payload=payload)
        self.retry_after = retry_after


class ApiError(MailrifyError):
    pass
