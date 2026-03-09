from .client import AsyncMailGlyph, MailGlyph
from .exceptions import (
    ApiError,
    AuthenticationError,
    MailGlyphError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from .models import (
    Campaign,
    Contact,
    FilterCondition,
    FilterGroup,
    Segment,
    SegmentFilter,
    SendEmailResult,
    StaticSegmentMembersAddResult,
    StaticSegmentMembersRemoveResult,
    TrackEventResult,
    VerifyEmailResult,
)

__version__ = "1.0.1"

__all__ = [
    "ApiError",
    "AsyncMailGlyph",
    "AuthenticationError",
    "Campaign",
    "Contact",
    "FilterCondition",
    "FilterGroup",
    "MailGlyph",
    "MailGlyphError",
    "NotFoundError",
    "RateLimitError",
    "Segment",
    "SegmentFilter",
    "SendEmailResult",
    "StaticSegmentMembersAddResult",
    "StaticSegmentMembersRemoveResult",
    "TrackEventResult",
    "ValidationError",
    "VerifyEmailResult",
    "__version__",
]
