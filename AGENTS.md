# AGENTS.md

## Project
This is the official MailGlyph Python SDK. See `./docs/` for the full specification.

## Context Files (read these FIRST)
1. [sdk-plan.md](./docs/sdk-plan.md) — Shared API spec, all 22 endpoints, auth rules, error hierarchy, testing strategy, release-please setup
2. [sdk-plan-python.md](./docs/sdk-plan-python.md) — Python-specific implementation plan (structure, Pydantic models, workflows)
3. [openapi.json](./docs/openapi.json) — OpenAPI 3.0.3 specification (source of truth for schemas)

## Build Order
1. Scaffold: `pyproject.toml` (name: `mailglyph`), `src/mailglyph/__init__.py`, `.gitignore`
2. Exceptions (`src/mailglyph/exceptions.py`) — `MailGlyphError`, `AuthenticationError`, `ValidationError`, `NotFoundError`, `RateLimitError`, `ApiError`
3. Models (`src/mailglyph/models.py`) — Pydantic BaseModel DTOs: `Contact`, `Segment`, `Campaign`, `SendEmailResult`, `VerifyEmailResult`, `TrackEventResult`
4. HttpClient (`src/mailglyph/http_client.py`) — httpx transport, Bearer auth, JSON parsing, error mapping, retry with exponential backoff for 429/5xx
5. Client (`src/mailglyph/client.py`) — sync `MailGlyph` + async `AsyncMailGlyph`, accepts API key + config, exposes `.emails`, `.events`, `.contacts`, `.campaigns`, `.segments`
6. Resources one at a time with pytest tests:
   - Emails (send, verify) → tests
   - Events (track with `pk_*` support, get_names) → tests
   - Contacts (list, create, get, update, delete, count) → tests
   - Campaigns (list, create, get, update, send, cancel, test, stats) → tests
   - Segments (list, create, get, update, delete, list_contacts) → tests
7. CI: [.github/workflows/ci.yml](cci:7://file:///Users/sharo/Library/CloudStorage/Dropbox/Projects/Plunk/plunk/.github/workflows/ci.yml:0:0-0:0), `release-please.yml`, `publish.yml`
8. README with install + usage examples
9. Run `pytest` — all tests must pass

## Standards
- Python 3.9+ with type hints everywhere
- httpx for HTTP (sync + async with same codebase)
- Pydantic v2 for models with camelCase aliases
- pytest + respx for testing with mocked HTTP responses
- Snake_case method names (`list_contacts`, not `listContacts`)
- `from_` parameter name to avoid Python `from` keyword collision
- Conventional Commits for all commit messages
