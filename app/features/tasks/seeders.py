"""Datos de ejemplo de la feature tasks (se cargan con `flask seed-db`)."""

from app.features.auth import services as auth_services
from app.features.tasks import services

DEMO_TASKS = [
    {
        "title": "Leer el README del proyecto",
        "description": "Entender la estructura de carpetas y cómo se arranca la aplicación.",
        "done": True,
    },
    {
        "title": "Crear el entorno virtual e instalar las dependencias",
        "description": "python -m venv .venv && pip install -r requirements.txt",
        "done": True,
    },
    {
        "title": "Configurar el fichero .env",
        "description": "Copiar .env.example a .env y ajustar la conexión a MariaDB.",
        "done": False,
    },
    {
        "title": "Añadir una nueva feature",
        "description": "Crear una carpeta en app/features siguiendo el patrón de tasks.",
        "done": False,
    },
    {"title": "Escribir tests para la nueva feature", "description": None, "done": False},
]


def seed():
    """Crea las tareas de ejemplo para el usuario demo (si todavía no tiene ninguna)."""
    user = auth_services.get_user_by_email("demo@listo.app")
    if user is None or services.list_tasks(user):
        return

    for data in DEMO_TASKS:
        task = services.create_task(user, data["title"], data["description"])
        if data["done"]:
            services.toggle_task(task)
