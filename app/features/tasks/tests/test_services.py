"""Tests de la lógica de negocio (services.py), sin pasar por HTTP."""

from app.features.auth import services as auth_services
from app.features.tasks import services


def test_create_and_list_tasks(user):
    services.create_task(user, "Primera", "Descripción")
    services.create_task(user, "Segunda")

    tasks = services.list_tasks(user)

    assert [task.title for task in tasks] == ["Segunda", "Primera"]  # las más recientes antes
    assert tasks[1].description == "Descripción"
    assert tasks[0].description is None
    assert all(not task.done for task in tasks)


def test_done_tasks_go_last(user):
    first = services.create_task(user, "Primera")
    services.create_task(user, "Segunda")
    services.toggle_task(first)

    services.create_task(user, "Tercera")
    tasks = services.list_tasks(user)

    assert [task.title for task in tasks] == ["Tercera", "Segunda", "Primera"]


def test_toggle_task(user):
    task = services.create_task(user, "Tarea")

    assert services.toggle_task(task).done is True
    assert services.toggle_task(task).done is False


def test_update_and_delete_task(user):
    task = services.create_task(user, "Antes", "algo")

    services.update_task(task, "Después", "")
    assert task.title == "Después"
    assert task.description is None

    services.delete_task(task)
    assert services.list_tasks(user) == []


def test_get_task_only_returns_own_tasks(user):
    other = auth_services.create_user("Otro", "otro@example.com", "secreto123")
    own = services.create_task(user, "Mía")
    foreign = services.create_task(other, "De otro")

    assert services.get_task(user, own.id) is own
    assert services.get_task(user, foreign.id) is None
    assert services.get_task(user, 9999) is None
