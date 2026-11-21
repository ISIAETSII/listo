"""
API JSON de la feature tasks.

La usa el JavaScript de la página de tareas (app/static/js/tasks.js) para marcar
tareas sin recargar la página. Como el resto de la aplicación, exige tener la sesión
iniciada: con la sesión abierta, prueba a visitar /api/tasks en el navegador.
"""

from flask import jsonify
from flask_login import current_user, login_required

from app.features.tasks import services, tasks_api_bp


@tasks_api_bp.route("")  # GET /api/tasks
@login_required
def list_tasks():
    tasks = services.list_tasks(current_user)
    return jsonify([task.to_dict() for task in tasks])


@tasks_api_bp.route("/<int:task_id>/toggle", methods=["POST"])  # POST /api/tasks/3/toggle
@login_required
def toggle(task_id):
    task = services.get_task(current_user, task_id)
    if task is None:
        return jsonify(error="Tarea no encontrada."), 404

    services.toggle_task(task)
    return jsonify(task.to_dict())
