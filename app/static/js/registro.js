// Valida el formulario de registro en el navegador, antes de enviarlo.
// El servidor lo vuelve a comprobar todo (forms.py): esto es solo una comodidad.
const formulario = document.getElementById("registro");
const listaErrores = document.getElementById("errores");

formulario.addEventListener("submit", (evento) => {
  // 1. Leer lo que ha escrito el usuario
  const nombre = document.getElementById("name").value.trim();
  const email = document.getElementById("email").value.trim();
  const clave = document.getElementById("password").value;
  const claveRepetida = document.getElementById("confirm").value;

  // 2. Aplicar las reglas y acumular los errores
  const errores = [];
  if (nombre === "") {
    errores.push("El nombre es obligatorio.");
  }
  if (!email.includes("@")) {
    errores.push("El correo debe contener una arroba.");
  }
  if (clave.length < 6) {
    errores.push("La contraseña necesita al menos 6 caracteres.");
  }
  if (clave !== claveRepetida) {
    errores.push("Las contraseñas no coinciden.");
  }

  // 3. Mostrar los errores (primero se borran los del intento anterior)
  listaErrores.innerHTML = "";
  for (const error of errores) {
    const elemento = document.createElement("li");
    elemento.textContent = error;
    listaErrores.appendChild(elemento);
  }

  // 4. Si hay errores, cancelar el envío
  if (errores.length > 0) {
    evento.preventDefault();
  }
});