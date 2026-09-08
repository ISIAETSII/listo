# Listo

**Listo** es el proyecto base de la asignatura. Es un gestor de tareas pequeño, hecho con Flask y MariaDB,
pensado para ser vistoso y muy fácil de entender. Sobre él se hacen las prácticas (instalación del sistema
base, gestión del código fuente, integración continua, contenedores y aislamiento, JavaScript y Flask)
y sirve de punto de partida para los proyectos.

Los usuarios se registran, inician sesión y gestionan su propia lista de tareas. Es poca funcionalidad
a propósito. Lo importante es **cómo está organizado el código**.

## Estructura del proyecto

```
listo/
├── app/
│   ├── __init__.py            ← create_app(), la fábrica de la aplicación; registra los blueprints
│   ├── config.py              ← configuración (lee el fichero .env)
│   ├── extensions.py          ← db (SQLAlchemy), login_manager (Flask-Login), csrf (Flask-WTF)
│   ├── commands.py            ← comandos flask init-db, seed-db y reset-db
│   ├── templates/             ← base.html, macros y páginas de error (comunes a todas las features)
│   ├── static/                ← CSS y JavaScript
│   └── features/              ← UNA CARPETA POR FUNCIONALIDAD
│       ├── home/              ← página de inicio
│       ├── auth/              ← registro, login y logout
│       └── tasks/             ← gestor de tareas
│           ├── __init__.py    ← define el blueprint (agrupa las rutas de la feature)
│           ├── models.py      ← tabla tasks (SQLAlchemy)
│           ├── forms.py       ← formulario (WTForms)
│           ├── services.py    ← lógica de negocio; las rutas llaman aquí y aquí se usa la base de datos
│           ├── routes.py      ← vistas HTML
│           ├── api.py         ← endpoints JSON (los usa el JavaScript)
│           ├── seeders.py     ← datos de ejemplo
│           ├── templates/     ← plantillas Jinja de la feature
│           └── tests/         ← tests de la feature
├── conftest.py                ← fixtures compartidas por los tests (app, client, user...)
├── requirements.txt           ← dependencias de Python
├── pyproject.toml             ← configuración de ruff (linter) y pytest
├── .env.example               ← plantilla de configuración (copiar a .env)
├── .flaskenv                  ← variables del comando flask (FLASK_APP y FLASK_DEBUG)
├── Dockerfile                 ← imagen de la aplicación
├── docker-compose.yml         ← aplicación + MariaDB con un solo comando
└── .github/workflows/ci.yml   ← integración continua (GitHub Actions)
```

### Cómo fluye una petición

```
navegador ──► routes.py (vista) ──► services.py (lógica) ──► models.py (base de datos)
                  │
                  └──► templates/ (HTML)      o      jsonify() (API)
```

* El `__init__.py` de cada feature crea el *blueprint* e importa `routes.py` al final del fichero.
* `app/__init__.py` importa los blueprints de todas las features y los registra en `create_app()`.
* Las rutas son cortas. Validan el formulario, llaman a un servicio y devuelven una plantilla o una redirección.
* Los servicios contienen la lógica y son los únicos que tocan la base de datos. Por eso se pueden
  reutilizar desde los seeders, desde los tests y desde otras features.

## Puesta en marcha en tu máquina

Necesitas tener instalados Python 3.12 o superior, MariaDB y git.

1. **Entorno virtual y dependencias.** El entorno virtual aísla las librerías de este proyecto de las
   del resto del sistema.

   ```bash
   python3 -m venv .venv          # en Windows, py -m venv .venv
   source .venv/bin/activate      # en Windows, .venv\Scripts\activate
   pip install -r requirements.txt
   ```

   En PowerShell, si al activar el entorno sale un error de permisos, ejecuta antes
   `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.

2. **MariaDB instalado y arrancado.**

   * Linux (Ubuntu o Debian). `sudo apt install mariadb-server` y entra en la consola con `sudo mariadb`.
   * macOS. `brew install mariadb`, `brew services start mariadb` y entra con `mariadb -u root`.
   * Windows. Instalador de mariadb.org y entra desde el acceso directo "Command Prompt (MariaDB)"
     con `mariadb -u root -p`.

3. **Base de datos y usuario.** Solo hay que hacerlo una vez, desde la consola de MariaDB.

   ```sql
   CREATE DATABASE listo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'listo_user'@'localhost' IDENTIFIED BY 'listo_password';
   GRANT ALL PRIVILEGES ON listo_db.* TO 'listo_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. **Configuración.** Copia `.env.example` a `.env` (`cp .env.example .env`; en Windows,
   `copy .env.example .env`) y comprueba que los valores `MARIADB_*` coinciden con lo que has creado
   en el paso anterior.

5. **Tablas y datos de ejemplo.**

   ```bash
   flask init-db
   flask seed-db
   ```

6. **Arrancar.** Ejecuta `flask run` y abre en el navegador la dirección que aparece en la terminal
   (localhost, puerto 5000). Puedes entrar con el usuario `demo@listo.app` y la contraseña `demo1234`.
   Si el puerto 5000 está ocupado (en macOS suele usarlo AirPlay), arranca con `flask run --port 5001`.

## Puesta en marcha con Docker

Con Docker no hace falta instalar Python ni MariaDB. Solo necesitas Docker Desktop.

```bash
cp .env.example .env
docker compose up --build
```

Se construye la imagen de la aplicación, se arranca MariaDB en otro contenedor, se crean las tablas y se
cargan los datos de ejemplo. La aplicación queda en localhost, puerto 5000. El código está montado dentro
del contenedor, así que los cambios se ven al recargar la página.

Para pararlo, `docker compose down`. Si además quieres borrar la base de datos, `docker compose down -v`.

Si ya tienes algo escuchando en el puerto 3306 o en el 5000, cambia `MARIADB_PORT` o `WEB_PORT` en `.env`
(estas dos variables solo afectan a Docker).

En Linux, los ficheros que crea el contenedor dentro del proyecto (por ejemplo `.pytest_cache` al ejecutar
`docker compose exec web pytest`) pertenecen a root. Si después `pytest` o `ruff` fallan en tu máquina con
un error de permisos, borra esas carpetas con `sudo rm -rf .pytest_cache .ruff_cache`.

## Comandos útiles

| Comando           | Qué hace                                                       |
| ----------------- | -------------------------------------------------------------- |
| `flask run`       | Arranca el servidor de desarrollo                              |
| `flask init-db`   | Crea las tablas (si no existen)                                |
| `flask seed-db`   | Inserta los datos de ejemplo (si no están ya)                  |
| `flask reset-db`  | Borra todo, crea las tablas e inserta los datos de ejemplo     |
| `flask routes`    | Lista todas las rutas de la aplicación                         |
| `flask shell`     | Consola Python con la aplicación cargada                       |
| `pytest`          | Ejecuta los tests                                              |
| `ruff check .`    | Pasa el linter (`ruff check --fix .` corrige lo que puede)     |
| `ruff format .`   | Formatea el código                                             |

Con Docker, antepón `docker compose exec web` (por ejemplo, `docker compose exec web pytest`).

## Tests

Los tests viven **dentro de cada feature** (`app/features/<feature>/tests/`) y usan una base de datos
SQLite en memoria, así que no necesitan MariaDB ni Docker. Las fixtures comunes (`app`, `client`,
`user` y `logged_client`) están en `conftest.py`. En cada feature, `test_services.py` prueba la lógica
sin pasar por HTTP y `test_routes.py` prueba las vistas con el cliente de pruebas de Flask.

```bash
pytest                       # todos
pytest -v                    # con el nombre de cada test
pytest app/features/tasks    # solo una feature
```

## Integración continua

En cada `push` y `pull request`, GitHub Actions ([.github/workflows/ci.yml](.github/workflows/ci.yml))
instala las dependencias, pasa el linter (`ruff check .`), comprueba el formato (`ruff format --check .`)
y ejecuta los tests (`pytest`). Antes de subir cambios, ejecuta esos tres comandos en tu máquina.

## Cómo añadir una feature

Supongamos que quieres añadir `notes`.

1. Crea `app/features/notes/` copiando la estructura de `tasks` (`__init__.py`, `models.py`, `forms.py`,
   `services.py`, `routes.py`, `templates/notes/` y `tests/`).
2. En `app/features/notes/__init__.py` define el blueprint e importa las rutas al final del fichero,
   igual que hace `tasks`. El comentario `noqa` evita que el linter se queje de que ese import no está
   al principio del fichero.

   ```python
   from flask import Blueprint

   notes_bp = Blueprint("notes", __name__, url_prefix="/notes", template_folder="templates")

   from app.features.notes import routes  # noqa
   ```

3. En `app/__init__.py` impórtalo y regístralo en `register_blueprints()`.
4. Si tiene modelos nuevos, ejecuta `flask init-db` para crear las tablas. Ojo, solo se crean las tablas
   de los modelos que la aplicación importa al arrancar; en cada feature eso ocurre porque `routes.py`
   importa `services.py` y este importa `models.py`, así que escribe esos ficheros antes de ejecutar
   el comando. Si cambias una tabla que ya existe, `flask reset-db` la vuelve a crear desde cero.
5. Si quieres datos de ejemplo, añade `seeders.py` y llámalo desde `seed_all()` en `app/commands.py`.
6. Escribe sus tests en `app/features/notes/tests/`.

## Tecnologías

* Flask, con *blueprints* y *application factory*
* Flask-SQLAlchemy y PyMySQL para MariaDB
* Flask-Login (sesiones) y Flask-WTF (formularios y CSRF)
* Bootstrap 5 e iconos de Bootstrap, cargados desde CDN
* pytest y ruff
* Docker y GitHub Actions
