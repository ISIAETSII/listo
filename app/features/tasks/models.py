from datetime import datetime, timezone

from app.extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    done = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    # Cada tarea pertenece a un usuario (clave ajena a la tabla users)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # Relación en los dos sentidos: task.user devuelve el usuario y user.tasks sus tareas.
    # Las vistas no la usan (consultan por user_id para poder ordenar), pero es útil
    # en las plantillas y en `flask shell`.
    user = db.relationship("User", backref="tasks")

    def to_dict(self):
        """Representación en JSON de la tarea (la usa la API)."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self):
        return f"<Task {self.id} {self.title!r}>"
