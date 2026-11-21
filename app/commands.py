"""
Comandos de consola propios. Se ejecutan con `flask <comando>`:

    flask init-db     → crea las tablas de la base de datos
    flask seed-db     → inserta datos de ejemplo (usuarios y tareas)
    flask reset-db    → borra todo, crea las tablas y vuelve a insertar los datos de ejemplo
"""

import click

from app.extensions import db
from app.features.auth import seeders as auth_seeders
from app.features.tasks import seeders as tasks_seeders


def seed_all():
    """Cada feature tiene su propio `seeders.py`. El orden importa: las tareas
    pertenecen a usuarios, así que primero se crean los usuarios."""
    auth_seeders.seed()
    tasks_seeders.seed()


def register_commands(app):
    @app.cli.command("init-db")
    def init_db():
        """Crea las tablas de la base de datos (si no existen).

        Solo se crean las tablas de los modelos que la aplicación ha importado al arrancar
        (en cada feature, routes.py importa services.py y este importa models.py)."""
        db.create_all()
        click.echo("Tablas creadas.")

    @app.cli.command("seed-db")
    def seed_db():
        """Inserta datos de ejemplo (usuarios y tareas)."""
        seed_all()
        click.echo("Datos de ejemplo insertados.")

    @app.cli.command("reset-db")
    @click.confirmation_option(prompt="Esto borra TODOS los datos de la base de datos. ¿Continuar?")
    def reset_db():
        """Borra todas las tablas, las vuelve a crear e inserta los datos de ejemplo."""
        db.drop_all()
        db.session.remove()  # olvida los objetos cargados en memoria, que ya no existen
        db.create_all()
        seed_all()
        click.echo("Base de datos reiniciada.")
