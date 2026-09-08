"""Tests de los datos de ejemplo y de los comandos `flask seed-db` y `flask reset-db`."""

from app.features.auth import services as auth_services
from app.features.tasks import services


def test_seed_db_creates_demo_data_only_once(app):
    runner = app.test_cli_runner()

    assert runner.invoke(args=["seed-db"]).exit_code == 0
    assert runner.invoke(args=["seed-db"]).exit_code == 0  # repetirlo no duplica nada

    demo = auth_services.get_user_by_email("demo@listo.app")
    assert demo is not None
    assert auth_services.authenticate("demo@listo.app", "demo1234") is demo
    assert len(services.list_tasks(demo)) == 5


def test_reset_db_starts_from_scratch(app, user):
    services.create_task(user, "Se borrará")
    runner = app.test_cli_runner()

    result = runner.invoke(args=["reset-db", "--yes"])

    assert result.exit_code == 0
    assert auth_services.get_user_by_email("ana@example.com") is None
    assert auth_services.get_user_by_email("demo@listo.app") is not None
