from .client import AsyncMailrify, Mailrify
from .exceptions import (
    ApiError,
    AuthenticationError,
    MailrifyError,
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

__version__ = "1.1.0"

__all__ = [
    "ApiError",
    "AsyncMailrify",
    "AuthenticationError",
    "Campaign",
    "Contact",
    "FilterCondition",
    "FilterGroup",
    "Mailrify",
    "MailrifyError",
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
