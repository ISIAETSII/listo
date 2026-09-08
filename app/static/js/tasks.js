// Marca y desmarca tareas sin recargar la página.
//
// Cuando el usuario pulsa la casilla de una tarea, se hace una petición POST
// a la API JSON (app/features/tasks/api.py) con fetch() y se actualiza la página
// con la respuesta.

document.addEventListener("DOMContentLoaded", () => {
  // Flask-WTF exige este token en las peticiones POST (protección CSRF)
  const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

  document.querySelectorAll("[data-task-toggle]").forEach((checkbox) => {
    checkbox.addEventListener("change", async () => {
      const taskId = checkbox.dataset.taskToggle;

      try {
        const response = await fetch(`/api/tasks/${taskId}/toggle`, {
          method: "POST",
          headers: { "X-CSRFToken": csrfToken },
        });
        if (!response.ok) {
          throw new Error(`El servidor ha respondido con el código ${response.status}`);
        }

        const task = await response.json();
        checkbox.closest("[data-task-item]").classList.toggle("task-done", task.done);
        updateCounters();
      } catch (error) {
        // Sin conexión, sesión caducada, error del servidor... deshacemos el cambio visual
        console.error(error);
        checkbox.checked = !checkbox.checked;
        alert("No se ha podido actualizar la tarea.");
      }
    });
  });

  function updateCounters() {
    const total = document.querySelectorAll("[data-task-item]").length;
    const done = document.querySelectorAll("[data-task-item].task-done").length;
    document.getElementById("pending-count").textContent = total - done;
    document.getElementById("done-count").textContent = done;
  }
});
