from flask import render_template, request
from markupsafe import escape

from app.features.home import home_bp


@home_bp.route("/")
def index():
    return render_template("home/index.html")


@home_bp.route("/about")
def about():
    return "<h1>Acerca de Listo</h1><p>El proyecto base de ISIA.</p>"


@home_bp.route("/hello/<name>")
def hello(name):
    return f"Hola, {escape(name)}"


@home_bp.route("/hello")
def hello_query():
    name = request.args.get("name", "desconocido")
    return f"Hola, {escape(name)}"
