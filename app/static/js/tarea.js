// Formulario de tareas: cuenta los caracteres del título y valida antes de enviar.
const formulario = document.getElementById("tarea");
const campoTitulo = document.getElementById("title");
const contador = document.getElementById("contador");
const maximo = 120;

// Borra las marcas y los mensajes del intento anterior
function limpiarErrores() {
  for (const campo of formulario.querySelectorAll(".is-invalid")) {
    campo.classList.remove("is-invalid");
  }
  for (const aviso of formulario.querySelectorAll(".invalid-feedback")) {
    aviso.remove();
  }
}

// Marca un campo en rojo y escribe el mensaje debajo de él
function mostrarError(campo, mensaje) {
  campo.classList.add("is-invalid");
  const aviso = document.createElement("div");
  aviso.classList.add("invalid-feedback");
  aviso.textContent = mensaje;
  campo.parentElement.appendChild(aviso);
}

function actualizarContador() {
  const largo = campoTitulo.value.length;
  contador.textContent = `${largo}/${maximo}`;
  contador.classList.toggle("contador-pasado", largo > maximo);
}

// Al cargar la página (al editar, el título ya trae texto) y a cada tecla
actualizarContador();
campoTitulo.addEventListener("input", actualizarContador);

formulario.addEventListener("submit", (evento) => {
  limpiarErrores();
  const titulo = campoTitulo.value.trim();
  if (titulo === "") {
    mostrarError(campoTitulo, "Escribe un título: solo con espacios no vale.");
    evento.preventDefault();
  } else if (titulo.length > maximo) {
    mostrarError(campoTitulo, `El título no puede pasar de ${maximo} caracteres.`);
    evento.preventDefault();
  }
});