"""Tests de las vistas HTML y de la API JSON, usando el cliente de pruebas de Flask."""

from app.features.auth import services as auth_services
from app.features.tasks import services


def test_tasks_require_login(client):
    response = client.get("/tasks/")

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_empty_list(logged_client):
    html = logged_client.get("/tasks/").get_data(as_text=True)

    assert "Todavía no tienes tareas" in html


def test_create_task(logged_client, user):
    response = logged_client.post(
        "/tasks/new",
        data={"title": "Estudiar Flask", "description": "Blueprints y plantillas"},
        follow_redirects=True,
    )
    html = response.get_data(as_text=True)

    assert "Tarea creada" in html
    assert "Estudiar Flask" in html
    assert len(services.list_tasks(user)) == 1


def test_create_task_requires_title(logged_client, user):
    response = logged_client.post("/tasks/new", data={"title": "", "description": "x"})

    assert response.status_code == 200
    assert "is-invalid" in response.get_data(as_text=True)
    assert services.list_tasks(user) == []


def test_edit_task(logged_client, user):
    task = services.create_task(user, "Antes")

    response = logged_client.get(f"/tasks/{task.id}/edit")
    assert "Antes" in response.get_data(as_text=True)

    response = logged_client.post(
        f"/tasks/{task.id}/edit", data={"title": "Después"}, follow_redirects=True
    )
    assert "Tarea actualizada" in response.get_data(as_text=True)
    assert task.title == "Después"


def test_delete_task(logged_client, user):
    task = services.create_task(user, "Borrar")

    response = logged_client.post(f"/tasks/{task.id}/delete", follow_redirects=True)

    assert "Tarea eliminada" in response.get_data(as_text=True)
    assert services.list_tasks(user) == []


def test_cannot_touch_other_users_tasks(logged_client):
    other = auth_services.create_user("Otro", "otro@example.com", "secreto123")
    foreign = services.create_task(other, "De otro")

    assert logged_client.get(f"/tasks/{foreign.id}/edit").status_code == 404
    assert logged_client.post(f"/tasks/{foreign.id}/delete").status_code == 404
    assert logged_client.post(f"/api/tasks/{foreign.id}/toggle").status_code == 404
    assert foreign.done is False


def test_api_list_tasks(logged_client, user):
    services.create_task(user, "Una", "desc")

    response = logged_client.get("/api/tasks")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Una"
    assert data[0]["description"] == "desc"
    assert data[0]["done"] is False


def test_api_toggle_task(logged_client, user):
    task = services.create_task(user, "Una")

    response = logged_client.post(f"/api/tasks/{task.id}/toggle")

    assert response.status_code == 200
    assert response.get_json()["done"] is True
    assert task.done is True


def test_api_requires_login(client):
    assert client.get("/api/tasks").status_code == 302


def test_post_without_csrf_token_is_rejected(app, logged_client, user):
    task = services.create_task(user, "Una")
    app.config["WTF_CSRF_ENABLED"] = True  # como en la aplicación real

    assert logged_client.post(f"/tasks/{task.id}/delete").status_code == 400
    assert logged_client.post(f"/api/tasks/{task.id}/toggle").status_code == 400
    assert services.list_tasks(user) == [task]
