"""Datos de ejemplo de la feature auth (se cargan con `flask seed-db`)."""

from app.features.auth import services

DEMO_USERS = [
    {"name": "Demo", "email": "demo@listo.app", "password": "demo1234"},
    {"name": "Ana Torres", "email": "ana@listo.app", "password": "ana1234"},
]


def seed():
    """Crea los usuarios de ejemplo (si todavía no existen)."""
    for data in DEMO_USERS:
        if services.get_user_by_email(data["email"]) is None:
            services.create_user(data["name"], data["email"], data["password"])
