"""
Lógica de negocio de la feature tasks.

Las rutas (routes.py y api.py) llaman a estas funciones; ellas son las únicas
que hablan con la base de datos.
"""

from app.extensions import db
from app.features.tasks.models import Task


def list_tasks(user):
    """Tareas del usuario: primero las pendientes y, dentro de cada grupo, las más recientes.
    El id desempata cuando varias tareas se crearon en el mismo segundo (MariaDB guarda
    las fechas sin fracciones de segundo)."""
    query = (
        db.select(Task)
        .where(Task.user_id == user.id)
        .order_by(Task.done, Task.created_at.desc(), Task.id.desc())
    )
    return db.session.scalars(query).all()


def get_task(user, task_id):
    """Una tarea concreta del usuario, o None si no existe o pertenece a otra persona."""
    task = db.session.get(Task, task_id)
    if task is None or task.user_id != user.id:
        return None
    return task


def create_task(user, title, description=None):
    # El formulario envía "" cuando la descripción está vacía; guardamos NULL en su lugar
    task = Task(title=title, description=description or None, user_id=user.id)
    db.session.add(task)
    db.session.commit()
    return task


def update_task(task, title, description=None):
    task.title = title
    task.description = description or None
    db.session.commit()
    return task


def toggle_task(task):
    """Marca la tarea como completada si estaba pendiente, y viceversa."""
    task.done = not task.done
    db.session.commit()
    return task


def delete_task(task):
    db.session.delete(task)
    db.session.commit()
