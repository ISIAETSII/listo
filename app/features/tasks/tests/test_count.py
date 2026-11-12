"""Tests de /tasks/count."""

from app.features.tasks import services


def test_count_requires_login(client):
    assert client.get("/tasks/count").status_code == 302

def test_count_pending_by_default(logged_client, user):
    services.create_task(user, "Una")
    services.toggle_task(services.create_task(user, "Otra"))

    assert logged_client.get("/tasks/count").get_data(as_text=True) == "1 de 2"