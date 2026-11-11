import pytest

from shortener.models import Link

pytestmark = pytest.mark.django_db


def test_redirects_to_original_url(client):
    Link.objects.create(original_url="https://example.com/target", code="abc1234")

    response = client.get("/abc1234")

    assert response.status_code == 302
    assert response["Location"] == "https://example.com/target"


def test_click_counter_increments(client):
    link = Link.objects.create(original_url="https://example.com", code="abc1234")

    for _ in range(3):
        client.get("/abc1234")

    link.refresh_from_db()
    assert link.click_count == 3


def test_unknown_code_returns_404(client):
    assert client.get("/yokbulunmaz").status_code == 404
