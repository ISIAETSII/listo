from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.features.tasks import services, tasks_bp
from app.features.tasks.forms import TaskForm


@tasks_bp.route("/")
@login_required
def index():
    tasks = services.list_tasks(current_user)
    pending = len([task for task in tasks if not task.done])
    return render_template(
        "tasks/index.html", tasks=tasks, pending=pending, done=len(tasks) - pending
    )


@tasks_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = TaskForm()
    if form.validate_on_submit():
        services.create_task(current_user, form.title.data, form.description.data)
        flash("Tarea creada.", "success")
        return redirect(url_for("tasks.index"))
    return render_template("tasks/form.html", form=form, title="Nueva tarea")


@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit(task_id):
    task = services.get_task(current_user, task_id)
    if task is None:
        abort(404)

    form = TaskForm(obj=task)  # rellena el formulario con los datos de la tarea
    if form.validate_on_submit():
        services.update_task(task, form.title.data, form.description.data)
        flash("Tarea actualizada.", "success")
        return redirect(url_for("tasks.index"))
    return render_template("tasks/form.html", form=form, title="Editar tarea")


@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
@login_required
def delete(task_id):
    task = services.get_task(current_user, task_id)
    if task is None:
        abort(404)

    services.delete_task(task)
    flash("Tarea eliminada.", "info")
    return redirect(url_for("tasks.index"))
