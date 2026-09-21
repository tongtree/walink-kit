import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test.sqlite3"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    with TestClient(app) as test_client:
        yield test_client


def test_create_and_get_link(client):
    response = client.post("/api/links", json={"phone": "+1 555 123 4567", "message": "hi"})
    assert response.status_code == 200
    body = response.json()
    assert body["whatsapp_url"] == "https://wa.me/15551234567?text=hi"

    fetched = client.get(f"/api/links/{body['slug']}")
    assert fetched.status_code == 200
    assert fetched.json()["slug"] == body["slug"]


def test_custom_slug_conflict(client):
    first = client.post("/api/links", json={"phone": "15551234567", "custom_slug": "promo"})
    assert first.status_code == 200
    second = client.post("/api/links", json={"phone": "15557654321", "custom_slug": "promo"})
    assert second.status_code == 409


def test_redirect_records_click_and_stats(client):
    created = client.post("/api/links", json={"phone": "15551234567"}).json()
    redirect = client.get(f"/{created['slug']}", follow_redirects=False)
    assert redirect.status_code == 302
    assert redirect.headers["location"] == "https://wa.me/15551234567"

    stats = client.get(f"/api/links/{created['slug']}/stats")
    assert stats.status_code == 200
    payload = stats.json()
    assert payload["clicks"] == 1
    assert len(payload["daily"]) == 1
    assert payload["daily"][0]["clicks"] == 1


def test_missing_link_returns_404(client):
    assert client.get("/api/links/nope/stats").status_code == 404
    assert client.get("/nope", follow_redirects=False).status_code == 404
