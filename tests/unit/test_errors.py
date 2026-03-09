from mailglyph.exceptions import (
    ApiError,
    AuthenticationError,
    MailGlyphError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


def test_exception_hierarchy() -> None:
    err = ValidationError("invalid", status_code=400, payload={"message": "invalid"})
    assert isinstance(err, MailGlyphError)
    assert err.status_code == 400
    assert err.payload == {"message": "invalid"}


def test_rate_limit_error_retry_after() -> None:
    err = RateLimitError("slow down", status_code=429, retry_after=1.5)
    assert isinstance(err, MailGlyphError)
    assert err.retry_after == 1.5


def test_specialized_errors_are_mailglyph_errors() -> None:
    errors = [AuthenticationError("auth"), NotFoundError("missing"), ApiError("server")]
    assert all(isinstance(error, MailGlyphError) for error in errors)
