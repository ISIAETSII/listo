from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.features.auth import auth_bp, services
from app.features.auth.forms import LoginForm, RegisterForm


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        if services.get_user_by_email(form.email.data) is not None:
            flash("Ya existe una cuenta con ese correo electrónico.", "danger")
        else:
            user = services.create_user(form.name.data, form.email.data, form.password.data)
            login_user(user)
            flash(f"Te damos la bienvenida, {user.name}. Tu cuenta se ha creado.", "success")
            return redirect(url_for("tasks.index"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("tasks.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = services.authenticate(form.email.data, form.password.data)
        if user is None:
            flash("Correo electrónico o contraseña incorrectos.", "danger")
        else:
            login_user(user, remember=form.remember.data)
            flash(f"Hola de nuevo, {user.name}.", "success")
            return redirect(safe_next_url())

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("home.index"))


def safe_next_url():
    """Flask-Login añade `?next=/pagina` al redirigir al login. Volvemos a esa página
    después de entrar, pero solo si es una ruta de esta aplicación (empieza por una sola
    barra); así nadie puede usar el login para redirigir a otro sitio web."""
    next_url = request.args.get("next", "")
    if next_url.startswith("/") and not next_url.startswith("//"):
        return next_url
    return url_for("tasks.index")
