"""
Extensiones de Flask que usa toda la aplicación.

Se crean aquí sin aplicación y se enlazan en `create_app()` con `init_app(app)`.
Así cualquier módulo puede hacer `from app.extensions import db` sin importar
la aplicación (evita importaciones circulares).
"""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()  # acceso a la base de datos (modelos y consultas)
csrf = CSRFProtect()  # protege los formularios contra ataques CSRF
login_manager = LoginManager()  # gestiona la sesión del usuario

# Si una página requiere login y el usuario no lo ha hecho, se le envía aquí
login_manager.login_view = "auth.login"
login_manager.login_message = "Inicia sesión para acceder a esta página."
login_manager.login_message_category = "warning"
