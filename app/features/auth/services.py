"""
Lógica de negocio de la feature auth.

Las rutas (routes.py) no hablan directamente con la base de datos: llaman a estas
funciones. Así la lógica se puede reutilizar desde otros sitios (seeders, tests,
otras features) y las rutas se mantienen cortas.
"""

from app.extensions import db
from app.features.auth.models import User


def normalize_email(email):
    return email.strip().lower()


def get_user_by_email(email):
    return db.session.scalar(db.select(User).where(User.email == normalize_email(email)))


def create_user(name, email, password):
    user = User(name=name.strip(), email=normalize_email(email))
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(email, password):
    """Devuelve el usuario si el correo y la contraseña son correctos; si no, None."""
    user = get_user_by_email(email)
    if user is not None and user.check_password(password):
        return user
    return None
