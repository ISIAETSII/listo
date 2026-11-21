"""Feature tasks: cada usuario gestiona su propia lista de tareas."""

from flask import Blueprint

# Vistas HTML (/tasks/...)
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks", template_folder="templates")

# API JSON (/api/tasks/...), usada por el JavaScript de la página de tareas
tasks_api_bp = Blueprint("tasks_api", __name__, url_prefix="/api/tasks")

# Se importan al final, a propósito: routes.py y api.py necesitan que los
# blueprints ya existan para poder asociarles sus rutas.
from app.features.tasks import api, routes  # noqa: E402, F401
