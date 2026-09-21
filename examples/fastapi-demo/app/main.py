import re
import secrets
import sqlite3
import string
from urllib.parse import quote

from collections.abc import AsyncIterator

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse

from .database import get_db, init_db
from .schemas import LinkCreate

SLUG_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,32}$")
ALPHABET = string.ascii_lowercase + string.digits

async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


app = FastAPI(
    title="WALink Kit short-link demo",
    description="Minimal self-hosted WhatsApp short link + click stats demo.",
    lifespan=lifespan,
)


def build_whatsapp_url(phone: str, message: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if not digits:
        raise HTTPException(status_code=422, detail="phone must contain digits")
    query = f"?text={quote(message)}" if message else ""
    return f"https://wa.me/{digits}{query}"


def random_slug(db: sqlite3.Connection) -> str:
    for _ in range(10):
        slug = "".join(secrets.choice(ALPHABET) for _ in range(8))
        exists = db.execute("SELECT 1 FROM links WHERE slug = ?", (slug,)).fetchone()
        if not exists:
            return slug
    raise HTTPException(status_code=500, detail="could not allocate slug")


@app.post("/api/links")
def create_link(data: LinkCreate, db: sqlite3.Connection = Depends(get_db)) -> dict:
    slug = data.custom_slug
    if slug is not None and not SLUG_PATTERN.match(slug):
        raise HTTPException(status_code=422, detail="invalid custom_slug")
    whatsapp_url = build_whatsapp_url(data.phone, data.message)
    if slug is None:
        slug = random_slug(db)
    try:
        cursor = db.execute(
            "INSERT INTO links (slug, phone, message) VALUES (?, ?, ?)",
            (slug, data.phone, data.message),
        )
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="slug already taken")
    return {"slug": slug, "short_url": f"/{slug}", "whatsapp_url": whatsapp_url, "id": cursor.lastrowid}


@app.get("/api/links/{slug}")
def get_link(slug: str, db: sqlite3.Connection = Depends(get_db)) -> dict:
    row = db.execute("SELECT * FROM links WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="link not found")
    return {"slug": row["slug"], "whatsapp_url": build_whatsapp_url(row["phone"], row["message"])}


@app.get("/api/links/{slug}/stats")
def link_stats(slug: str, db: sqlite3.Connection = Depends(get_db)) -> dict:
    row = db.execute("SELECT id FROM links WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="link not found")
    total = db.execute("SELECT COUNT(*) AS n FROM clicks WHERE link_id = ?", (row["id"],)).fetchone()["n"]
    daily_rows = db.execute(
        """
        SELECT substr(created_at, 1, 10) AS date, COUNT(*) AS clicks
        FROM clicks WHERE link_id = ?
        GROUP BY date ORDER BY date
        """,
        (row["id"],),
    ).fetchall()
    return {"slug": slug, "clicks": total, "daily": [dict(item) for item in daily_rows]}


@app.get("/{slug}")
def redirect(slug: str, request: Request, db: sqlite3.Connection = Depends(get_db)) -> RedirectResponse:
    row = db.execute("SELECT * FROM links WHERE slug = ?", (slug,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="link not found")
    ip = request.client.host if request.client else ""
    referer = request.headers.get("referer", "")
    db.execute(
        "INSERT INTO clicks (link_id, ip, referer) VALUES (?, ?, ?)",
        (row["id"], ip, referer),
    )
    return RedirectResponse(build_whatsapp_url(row["phone"], row["message"]), status_code=302)
