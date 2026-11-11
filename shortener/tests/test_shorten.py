import pytest

from shortener.models import Link

pytestmark = pytest.mark.django_db


def test_shorten_valid_url(api_client):
    response = api_client.post("/api/shorten", {"url": "https://example.com/a?x=1"}, format="json")

    assert response.status_code == 201
    code = response.json()["code"]
    assert response.json()["short_url"].endswith(f"/{code}")
    assert Link.objects.get(code=code).original_url == "https://example.com/a?x=1"


@pytest.mark.parametrize(
    "payload",
    [
        {"url": "ftp://example.com/file"},
        {"url": "javascript:alert(1)"},
        {"url": "not-a-url"},
        {"url": ""},
        {},
    ],
)
def test_shorten_rejects_invalid_input(api_client, payload):
    response = api_client.post("/api/shorten", payload, format="json")

    assert response.status_code == 400
    assert Link.objects.count() == 0


def test_shorten_retries_on_code_collision(api_client, monkeypatch):
    Link.objects.create(original_url="https://old.example", code="dup")
    codes = iter(["dup", "fresh"])
    monkeypatch.setattr("shortener.views.generate_code", lambda: next(codes))

    response = api_client.post("/api/shorten", {"url": "https://new.example"}, format="json")

    assert response.status_code == 201
    assert response.json()["code"] == "fresh"
    assert Link.objects.count() == 2


def test_shorten_gives_up_after_repeated_collisions(api_client, monkeypatch):
    Link.objects.create(original_url="https://old.example", code="dup")
    monkeypatch.setattr("shortener.views.generate_code", lambda: "dup")

    response = api_client.post("/api/shorten", {"url": "https://new.example"}, format="json")

    assert response.status_code == 503
    assert Link.objects.count() == 1
