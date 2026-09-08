"""Tests de la lógica de negocio (services.py), sin pasar por HTTP."""

from app.features.auth import services


def test_create_user_normalizes_email(app):
    user = services.create_user("  Luis ", " Luis@Example.com ", "secreto123")

    assert user.name == "Luis"
    assert user.email == "luis@example.com"  # el correo se guarda en minúsculas y sin espacios
    assert user.password_hash != "secreto123"  # nunca se guarda la contraseña en claro
    assert user.check_password("secreto123")


def test_get_user_by_email_ignores_case(user):
    assert services.get_user_by_email("ANA@example.com") is user
    assert services.get_user_by_email("nadie@example.com") is None


def test_authenticate(user):
    assert services.authenticate("ana@example.com", "secreto123") is user
    assert services.authenticate("ANA@example.com", "secreto123") is user
    assert services.authenticate("ana@example.com", "otra") is None
    assert services.authenticate("nadie@example.com", "secreto123") is None
