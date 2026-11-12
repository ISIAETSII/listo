// Valida el formulario de registro en el navegador, antes de enviarlo.
// El servidor lo vuelve a comprobar todo (forms.py): esto es solo una comodidad.
const formulario = document.getElementById("registro");
const campoNombre = document.getElementById("name");
const campoEmail = document.getElementById("email");
const campoDni = document.getElementById("dni");
const campoClave = document.getElementById("password");
const campoRepetida = document.getElementById("confirm");

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
// Ocho dígitos y una letra mayúscula
function formatoDni(dni) {
  return /^[0-9]{8}[A-Z]$/.test(dni);
}

// La letra sale del resto de dividir el número entre 23
function letraDni(numero) {
  const letras = "TRWAGMYFPDXBNJZSQVHLCKE";
  return letras[numero % 23];
}

formulario.addEventListener("submit", (evento) => {
  limpiarErrores();
  let hayErrores = false;

  if (campoNombre.value.trim() === "") {
    mostrarError(campoNombre, "El nombre es obligatorio.");
    hayErrores = true;
  }
  if (!campoEmail.value.includes("@")) {
    mostrarError(campoEmail, "El correo debe contener una arroba.");
    hayErrores = true;
  }
    const dni = campoDni.value.trim();
  if (!formatoDni(dni)) {
    mostrarError(campoDni, "Escribe ocho dígitos y una letra mayúscula.");
    hayErrores = true;
  } else if (dni[8] !== letraDni(Number(dni.slice(0, 8)))) {
    mostrarError(campoDni, "La letra del DNI no es correcta.");
    hayErrores = true;
  }
  if (campoClave.value.length < 6) {
    mostrarError(campoClave, "La contraseña necesita al menos 6 caracteres.");
    hayErrores = true;
  }
  if (campoClave.value !== campoRepetida.value) {
    mostrarError(campoRepetida, "Las contraseñas no coinciden.");
    hayErrores = true;
  }

  if (hayErrores) {
    evento.preventDefault();
  }
});

// Avisa mientras se escribe: compara las dos contraseñas a cada tecla
function comprobarClaves() {
  limpiarErrores(); // en cuanto vuelve a escribir, fuera los avisos del último envío
  const escrita = campoRepetida.value !== "";
  const distintas = campoRepetida.value !== campoClave.value;
  campoRepetida.classList.toggle("error", escrita && distintas);
  campoRepetida.classList.toggle("correcto", escrita && !distintas);
}

campoRepetida.addEventListener("input", comprobarClaves);
campoClave.addEventListener("input", comprobarClaves);