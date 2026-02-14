# Mailrify Python SDK Plan

> Shared spec: [sdk-plan.md](./sdk-plan.md) · Repo: [Mailrify/mailrify-python](https://github.com/Mailrify/mailrify-python) · Registry: [PyPI `mailrify`](https://pypi.org/project/mailrify/) · Min: Python 3.9+

---

## Tech Stack

| Concern | Choice |
|---------|--------|
| Language | Python 3.9+ |
| HTTP | `httpx` (sync + async) |
| Models | `pydantic` v2 |
| Testing | `pytest` + `pytest-asyncio` + `respx` (mock) |
| Linting | `ruff` |
| Type checking | `mypy` (strict) |
| Packaging | `hatch` / `pyproject.toml` |

---

## Repository Structure

```
mailrify-python/
├── src/mailrify/
│   ├── __init__.py              # Mailrify + AsyncMailrify exports
│   ├── client.py                # Client config
│   ├── http_client.py           # httpx sync + async transport
│   ├── errors.py                # Exception hierarchy
│   ├── types.py                 # Pydantic models
│   └── resources/
│       ├── __init__.py
│       ├── emails.py
│       ├── events.py
│       ├── contacts.py
│       ├── campaigns.py
│       └── segments.py
├── tests/
│   ├── unit/
│   │   ├── test_emails.py
│   │   ├── test_events.py
│   │   ├── test_contacts.py
│   │   ├── test_campaigns.py
│   │   ├── test_segments.py
│   │   ├── test_http_client.py
│   │   └── test_errors.py
│   └── integration/
│       └── test_api.py
├── openapi.json
├── pyproject.toml
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── release-please.yml
│       └── publish.yml
├── release-please-config.json
├── .release-please-manifest.json
├── AGENTS.md
├── README.md
├── LICENSE
└── CHANGELOG.md
```

---

## Key Models (`src/mailrify/types.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional

class VerifyEmailResult(BaseModel):
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
    suggested_email: Optional[str] = Field(None, alias="suggestedEmail")
    reasons: list[str]

class Contact(BaseModel):
    id: str
    email: str
    subscribed: bool
    data: dict
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")

class Segment(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    condition: dict
    track_membership: bool = Field(alias="trackMembership")
    member_count: int = Field(alias="memberCount")

class Campaign(BaseModel):
    id: str
    name: str
    subject: str
    type: str  # ALL | SEGMENT | FILTERED
    status: str  # DRAFT | SCHEDULED | SENDING | SENT
    scheduled_at: Optional[str] = Field(None, alias="scheduledAt")
```

---

## Sync + Async API

```python
# Sync
from mailrify import Mailrify
client = Mailrify("sk_your_key")
result = client.emails.send(to="user@example.com", ...)

# Async
from mailrify import AsyncMailrify
client = AsyncMailrify("sk_your_key")
result = await client.emails.send(to="user@example.com", ...)
```

Both share the same resource classes internally, backed by `httpx.Client` (sync) and `httpx.AsyncClient` (async).

---

## Test Commands

| Scope | Command |
|-------|---------|
| Unit | `pytest tests/unit` |
| Integration | `MAILRIFY_API_KEY=sk_... pytest tests/integration` |
| Lint | `ruff check src/ tests/` |
| Type check | `mypy src/` |
| Build | `hatch build` |

---

## `pyproject.toml` key fields

```toml
[project]
name = "mailrify"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = [
    "httpx>=0.25",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "respx>=0.21",
    "ruff>=0.1",
    "mypy>=1.0",
]
```

---

## Usage Examples (for README)

```python
from mailrify import Mailrify

client = Mailrify("sk_your_api_key")

# Send email
result = client.emails.send(
    to="user@example.com",
    from_={"name": "My App", "email": "hello@myapp.com"},
    subject="Welcome!",
    body="<h1>Hello {{name}}</h1>",
    data={"name": "John"},
)

# Verify email
verification = client.emails.verify("user@example.com")
print(verification.data.valid, verification.data.is_random_input)

# Track event (public key)
from mailrify import Mailrify
tracker = Mailrify("pk_your_public_key")
tracker.events.track(
    email="user@example.com",
    event="purchase",
    data={"product": "Premium", "amount": 99},
)

# Contacts
contacts = client.contacts.list(limit=50)
contact = client.contacts.create(email="new@example.com", data={"plan": "premium"})
client.contacts.update(contact.id, subscribed=False)
client.contacts.delete(contact.id)

# Segments
segment = client.segments.create(
    name="Premium Users",
    condition={"operator": "AND", "conditions": [{"field": "data.plan", "operator": "equals", "value": "premium"}]},
    track_membership=True,
)
members = client.segments.list_contacts(segment.id, page=1)

# Campaigns
campaign = client.campaigns.create(
    name="Product Launch",
    subject="Introducing our new feature!",
    body="<h1>Big news!</h1><p>Check out our latest feature.</p>",
    from_email="hello@myapp.com",
    audience_type="ALL",
)

# Schedule for later
client.campaigns.send(campaign.id, scheduled_for="2026-03-01T10:00:00Z")

# Send test email first
client.campaigns.test(campaign.id, email="preview@myapp.com")

# Get stats
stats = client.campaigns.stats(campaign.id)

# Cancel scheduled campaign
client.campaigns.cancel(campaign.id)
```

> **Note:** `from_` uses trailing underscore to avoid Python reserved keyword collision.

---

## Release Automation

### `release-please-config.json`

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json",
  "packages": {
    ".": {
      "release-type": "python",
      "bump-minor-pre-major": true,
      "bump-patch-for-minor-pre-major": true
    }
  }
}
```

### `.release-please-manifest.json`

```json
{
  ".": "0.1.0"
}
```

### `.github/workflows/release-please.yml`

```yaml
name: Release Please

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    outputs:
      release_created: ${{ steps.release.outputs.release_created }}
      tag_name: ${{ steps.release.outputs.tag_name }}
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
        with:
          release-type: python
```

### `.github/workflows/publish.yml`

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write  # for trusted publishing
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install hatch
      - run: hatch build
      - uses: pypa/gh-action-pypi-publish@release/v1
        # Uses trusted publishing (OIDC) — no API token needed
```

> **Tip:** Configure [PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/) for the repo to avoid managing API tokens.
