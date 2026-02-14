from __future__ import annotations

from typing import Any

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class MailrifyModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class ContactRef(MailrifyModel):
    id: str
    email: str


class SendEmailItem(MailrifyModel):
    contact: ContactRef
    email: str


class SendEmailResult(MailrifyModel):
    emails: list[SendEmailItem] = Field(default_factory=list)
    timestamp: str | None = None


class VerifyEmailResult(MailrifyModel):
    email: str
    valid: bool
    is_disposable: bool = Field(alias="isDisposable")
    is_alias: bool = Field(alias="isAlias")
    is_typo: bool = Field(alias="isTypo")
    is_plus_addressed: bool = Field(alias="isPlusAddressed")
    is_random_input: bool = Field(alias="isRandomInput")
    is_personal_email: bool = Field(alias="isPersonalEmail")
    domain_exists: bool = Field(alias="domainExists")
    has_website: bool = Field(alias="hasWebsite")
    has_mx_records: bool = Field(alias="hasMxRecords")
    suggested_email: str | None = Field(default=None, alias="suggestedEmail")
    reasons: list[str] = Field(default_factory=list)


class TrackEventResult(MailrifyModel):
    contact: str
    event: str
    timestamp: str


class ContactMeta(MailrifyModel):
    is_new: bool | None = Field(default=None, alias="isNew")
    is_update: bool | None = Field(default=None, alias="isUpdate")


class Contact(MailrifyModel):
    id: str
    email: str
    subscribed: bool
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = Field(default=None, alias="createdAt")
    updated_at: str | None = Field(default=None, alias="updatedAt")
    meta: ContactMeta | None = Field(default=None, alias="_meta")


class Segment(MailrifyModel):
    id: str
    name: str | None = None
    description: str | None = None
    condition: FilterCondition | None = None
    track_membership: bool | None = Field(default=None, alias="trackMembership")
    member_count: int | None = Field(default=None, alias="memberCount")
    project_id: str | None = Field(default=None, alias="projectId")
    created_at: str | None = Field(default=None, alias="createdAt")
    updated_at: str | None = Field(default=None, alias="updatedAt")


class SegmentFilter(MailrifyModel):
    field: str
    operator: str
    value: Any | None = None
    unit: str | None = None


class FilterGroup(MailrifyModel):
    filters: list[SegmentFilter] = Field(default_factory=list)
    conditions: FilterCondition | None = None


class FilterCondition(MailrifyModel):
    logic: str
    groups: list[FilterGroup] = Field(default_factory=list)


class Campaign(MailrifyModel):
    id: str
    name: str | None = None
    description: str | None = None
    subject: str | None = None
    body: str | None = None
    from_email: str | None = Field(default=None, alias="from")
    from_name: str | None = Field(default=None, alias="fromName")
    reply_to: str | None = Field(default=None, alias="replyTo")
    audience_type: str | None = Field(
        default=None,
        validation_alias=AliasChoices("audienceType", "type"),
        serialization_alias="audienceType",
    )
    audience_condition: FilterCondition | None = Field(default=None, alias="audienceCondition")
    segment_id: str | None = Field(default=None, alias="segmentId")
    status: str | None = None
    total_recipients: int | None = Field(default=None, alias="totalRecipients")
    sent_count: int | None = Field(default=None, alias="sentCount")
    delivered_count: int | None = Field(default=None, alias="deliveredCount")
    opened_count: int | None = Field(default=None, alias="openedCount")
    clicked_count: int | None = Field(default=None, alias="clickedCount")
    bounced_count: int | None = Field(default=None, alias="bouncedCount")
    scheduled_for: str | None = Field(
        default=None,
        validation_alias=AliasChoices("scheduledFor", "scheduledAt"),
        serialization_alias="scheduledFor",
    )
    sent_at: str | None = Field(default=None, alias="sentAt")
    created_at: str | None = Field(default=None, alias="createdAt")
    updated_at: str | None = Field(default=None, alias="updatedAt")
    segment: Segment | None = None


class ContactsPage(MailrifyModel):
    contacts: list[Contact] = Field(default_factory=list)
    cursor: str | None = None
    has_more: bool = Field(default=False, alias="hasMore")
    total: int | None = None


class CampaignsPage(MailrifyModel):
    data: list[Campaign] = Field(default_factory=list)
    page: int | None = None
    page_size: int | None = Field(default=None, alias="pageSize")
    total: int | None = None
    total_pages: int | None = Field(default=None, alias="totalPages")

    @property
    def campaigns(self) -> list[Campaign]:
        return self.data


class SegmentContactsPage(MailrifyModel):
    data: list[Contact] = Field(default_factory=list)
    total: int | None = None
    page: int | None = None
    page_size: int | None = Field(default=None, alias="pageSize")
    total_pages: int | None = Field(default=None, alias="totalPages")


FilterCondition.model_rebuild()
