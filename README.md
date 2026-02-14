# Mailrify Python SDK

Official Python SDK for the Mailrify API.

## Installation

```bash
pip install mailrify
```

## Quick Start (Sync)

```python
from mailrify import Mailrify

client = Mailrify("sk_your_api_key")
```

## Quick Start (Async)

```python
from mailrify import AsyncMailrify

client = AsyncMailrify("sk_your_api_key")
```

## Emails

```python
from mailrify import Mailrify

client = Mailrify("sk_your_api_key")

result = client.emails.send(
    to="user@example.com",
    from_={"name": "My App", "email": "hello@myapp.com"},
    subject="Welcome!",
    body="<h1>Hello {{name}}</h1>",
    data={"name": "John"},
)

verification = client.emails.verify("user@example.com")
print(verification.valid, verification.is_random_input)
```

## Events

```python
from mailrify import Mailrify

tracker = Mailrify("pk_your_public_key")
tracker.events.track(
    email="user@example.com",
    event="purchase",
    data={"product": "Premium", "amount": 99},
)

client = Mailrify("sk_your_api_key")
names = client.events.get_names()
```

## Contacts

```python
from mailrify import Mailrify

client = Mailrify("sk_your_api_key")

contacts = client.contacts.list(limit=50)
contact = client.contacts.create(email="new@example.com", data={"plan": "premium"})
client.contacts.update(contact.id, subscribed=False)
client.contacts.delete(contact.id)
count = client.contacts.count()
```

## Segments

```python
from mailrify import Mailrify

client = Mailrify("sk_your_api_key")

segment = client.segments.create(
    name="Premium Users",
    condition={
        "logic": "AND",
        "groups": [
            {
                "filters": [
                    {"field": "data.plan", "operator": "equals", "value": "premium"}
                ]
            }
        ],
    },
    track_membership=True,
)
members = client.segments.list_contacts(segment.id, page=1)
```

## Campaigns

```python
from mailrify import Mailrify

client = Mailrify("sk_your_api_key")

campaign = client.campaigns.create(
    name="Product Launch",
    subject="Introducing our new feature!",
    body="<h1>Big news!</h1><p>Check out our latest feature.</p>",
    from_email="hello@myapp.com",
    audience_type="ALL",
)

campaigns_page = client.campaigns.list(page=1, page_size=20, status="DRAFT")
client.campaigns.send(campaign.id, scheduled_for="2026-03-01T10:00:00Z")
client.campaigns.test(campaign.id, email="preview@myapp.com")
stats = client.campaigns.stats(campaign.id)
client.campaigns.cancel(campaign.id)
```

## Async Example

```python
import asyncio

from mailrify import AsyncMailrify


async def main() -> None:
    async with AsyncMailrify("sk_your_api_key") as client:
        verification = await client.emails.verify("user@example.com")
        print(verification.valid)


asyncio.run(main())
```

## Configuration

```python
from mailrify import Mailrify

client = Mailrify(
    "sk_your_api_key",
    base_url="https://api.mailrify.com",
    timeout=30.0,
    max_retries=3,
)
```

## Development

```bash
pip install -e .[dev]
ruff check .
mypy src/
pytest
hatch build
```
