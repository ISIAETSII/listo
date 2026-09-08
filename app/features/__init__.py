"""
Aquí viven las features de la aplicación, una por carpeta.

Estructura de una feature (por ejemplo, `tasks`):

    tasks/
    ├── __init__.py    ← define el blueprint (agrupa las rutas de la feature)
    ├── models.py      ← tablas de la base de datos (SQLAlchemy)
    ├── forms.py       ← formularios (WTForms)
    ├── services.py    ← lógica de negocio (las rutas llaman aquí)
    ├── routes.py      ← vistas HTML
    ├── api.py         ← endpoints JSON (opcional)
    ├── seeders.py     ← datos de ejemplo
    ├── templates/     ← plantillas Jinja de la feature
    └── tests/         ← tests de la feature
"""
