"""Feature auth: registro de usuarios, inicio y cierre de sesión."""

from flask import Blueprint

auth_bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates")

# Se importa al final, a propósito: routes.py necesita que `auth_bp` ya exista
# para poder asociarle sus rutas.
from app.features.auth import routes  # noqa: E402, F401
