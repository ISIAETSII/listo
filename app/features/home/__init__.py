"""Feature home: la página de inicio."""

from flask import Blueprint

home_bp = Blueprint("home", __name__, template_folder="templates")

# Se importa al final, a propósito: routes.py necesita que `home_bp` ya exista
# para poder asociarle sus rutas.
from app.features.home import routes  # noqa: E402, F401
