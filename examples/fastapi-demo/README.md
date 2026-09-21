# WALink short-link backend demo

A minimal, self-hosted WhatsApp short-link service with click counting, built
with FastAPI and SQLite. This is a **demo**, not the production WALink backend:
it intentionally omits authentication, advanced routing rules, rate limiting,
abuse protection and production analytics.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs for the interactive API.

## Run with Docker

```bash
docker compose up
```

## API

| Method | Path | Description |
| ------ | ---- | ----------- |
| POST | `/api/links` | Create a link: `{ "phone": "+15551234567", "message": "hi", "custom_slug": "promo" }` |
| GET | `/api/links/{slug}` | Fetch a link |
| GET | `/api/links/{slug}/stats` | Click total and per-day counts |
| GET | `/{slug}` | Record a click, then 302 redirect to WhatsApp |

- A duplicate `custom_slug` returns `409`.
- Daily stats are grouped in UTC (the demo default).

## Tests

```bash
pytest
```

## Want more?

The hosted [WALink online generator](https://walink.wadesk.io) adds link rotators, smart rules, QR
codes, visitor analytics, dashboards and zero-maintenance hosting.
