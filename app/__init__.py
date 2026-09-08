"""
Punto de entrada de la aplicación: la *fábrica de aplicaciones* (application factory).

`create_app()` construye la aplicación Flask paso a paso:

1. Carga la configuración (`app/config.py`).
2. Inicializa las extensiones (`app/extensions.py`): base de datos, login y CSRF.
3. Registra los *blueprints* de cada feature (`app/features/<feature>/__init__.py`).
4. Registra las páginas de error y los comandos de consola (`app/commands.py`).

Cada funcionalidad ("feature") vive en su propia carpeta dentro de `app/features/`
con sus modelos, formularios, servicios, rutas, plantillas y tests.
"""

from flask import Flask, render_template

from app.commands import register_commands
from app.config import Config
from app.extensions import csrf, db, login_manager
from app.features.auth import auth_bp
from app.features.home import home_bp
from app.features.tasks import tasks_api_bp, tasks_bp


def create_app(config_overrides=None):
    """Crea y configura la aplicación. `config_overrides` permite cambiar la configuración
    (por ejemplo, los tests la usan para trabajar con SQLite en memoria)."""
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)
    app.json.ensure_ascii = False  # las respuestas JSON muestran tildes y eñes tal cual

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    """Cada feature aporta uno o más blueprints. Para añadir una feature nueva,
    impórtala arriba y regístrala aquí."""
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(tasks_api_bp)


def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(error):
        return render_template(
            "errors/error.html", code=403, message="No tienes permiso para ver esta página."
        ), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template(
            "errors/error.html", code=404, message="La página que buscas no existe."
        ), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # deshace cualquier transacción a medias
        return render_template(
            "errors/error.html", code=500, message="Algo ha fallado en el servidor."
        ), 500
