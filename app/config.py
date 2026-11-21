"""
Configuración de la aplicación.

Los valores se leen de variables de entorno. En desarrollo, esas variables
se definen en el fichero `.env` (copia `.env.example` y ajústalo).
"""

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()  # carga el fichero .env si existe (no sobrescribe variables ya definidas)


class Config:
    APP_NAME = "Listo"

    # Clave con la que Flask firma las sesiones y los tokens CSRF
    SECRET_KEY = os.getenv("SECRET_KEY", "clave-de-desarrollo-cambiame")

    # Los formularios (WTForms) muestran sus mensajes de error en español
    # (ver `class Meta` en los forms.py de cada feature)
    WTF_I18N_ENABLED = False

    # Conexión a MariaDB
    MARIADB_HOSTNAME = os.getenv("MARIADB_HOSTNAME", "localhost")
    MARIADB_PORT = os.getenv("MARIADB_PORT", "3306")
    MARIADB_DATABASE = os.getenv("MARIADB_DATABASE", "listo_db")
    MARIADB_USER = os.getenv("MARIADB_USER", "listo_user")
    MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "listo_password")

    # SQLAlchemy usa una URL de conexión. Se puede fijar directamente con DATABASE_URL
    # (por ejemplo, `sqlite:///dev.db` para probar sin MariaDB: el fichero se crea en la
    # carpeta instance/, que está en .gitignore); si no, se construye a partir de las
    # variables MARIADB_* de arriba. quote_plus() escapa caracteres como @ o # en la contraseña.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or (
        f"mysql+pymysql://{quote_plus(MARIADB_USER)}:{quote_plus(MARIADB_PASSWORD)}"
        f"@{MARIADB_HOSTNAME}:{MARIADB_PORT}/{MARIADB_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
