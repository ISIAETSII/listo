"""Tests de /tasks/count."""

from app.features.tasks import services


def test_count_requires_login(client):
    assert client.get("/tasks/count").status_code == 302


def test_count_pending_by_default(logged_client, user):
    services.create_task(user, "Una")
    services.toggle_task(services.create_task(user, "Otra"))

    assert logged_client.get("/tasks/count").get_data(as_text=True) == "1 de 2"


def test_count_done_and_all(logged_client, user):
    services.create_task(user, "Una")
    services.toggle_task(services.create_task(user, "Otra"))
    assert logged_client.get("/tasks/count?state=done").get_data(as_text=True) == "1 de 2"
    assert logged_client.get("/tasks/count?state=all").get_data(as_text=True) == "2 de 2"


def test_count_invalid_state(logged_client):
    response = logged_client.get("/tasks/count?state=raro")
    assert response.status_code == 400
    assert "Estado no válido: usa pending, done o all." in response.get_data(as_text=True)
