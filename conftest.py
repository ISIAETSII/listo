"""
Fixtures compartidas por todos los tests (pytest carga este fichero automáticamente).

Los tests usan una base de datos SQLite en memoria en lugar de MariaDB:
así se ejecutan rápido, no necesitan nada instalado y no tocan datos reales.

Ojo: todas las peticiones de un mismo test comparten el contexto de la aplicación
y la sesión de la base de datos. Es lo que hace sencillo el fixture, a cambio de
usar un solo cliente HTTP por test.
"""

import pytest

from app import create_app
from app.extensions import db
from app.features.auth import services as auth_services


@pytest.fixture
def app():
    """Una aplicación configurada para tests, con la base de datos recién creada."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,  # simplifica el envío de formularios desde los tests
        }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
        db.engine.dispose()  # cierra la conexión de SQLite


@pytest.fixture
def client(app):
    """Cliente HTTP de pruebas: permite hacer peticiones sin levantar un servidor."""
    return app.test_client()


@pytest.fixture
def user(app):
    """Un usuario registrado (contraseña: secreto123)."""
    return auth_services.create_user("Ana", "ana@example.com", "secreto123")


@pytest.fixture
def logged_client(client, user):
    """Cliente HTTP con la sesión iniciada como `user`."""
    client.post("/auth/login", data={"email": user.email, "password": "secreto123"})
    return client
