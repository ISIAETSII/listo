"""Tests de la página «Tu progreso» y de su versión JSON."""

from app.features.tasks import services


def test_stats_page(logged_client, user):
    services.create_task(user, "Pendiente")
    services.toggle_task(services.create_task(user, "Hecha"))

    html = logged_client.get("/tasks/stats").get_data(as_text=True)

    assert "50 %" in html
    assert "Has terminado 1 de 2 tareas." in html
    assert "<li>Pendiente</li>" in html
    assert "<li>Hecha</li>" not in html


def test_stats_page_without_tasks(logged_client):
    assert "Todavía no tienes tareas." in logged_client.get(
        "/tasks/stats"
    ).get_data(as_text=True)

def test_stats_page_escapes_html(logged_client, user):
    services.create_task(user, "<b>Urgente</b>")
    html = logged_client.get("/tasks/stats").get_data(as_text=True)
    assert "&lt;b&gt;Urgente&lt;/b&gt;" in html

def test_flash_shows_the_title(logged_client):
    response = logged_client.post("/tasks/new", data={"title": "Leer"}, follow_redirects=
    True)
    assert "Tarea creada: «Leer»." in response.get_data(as_text=True)