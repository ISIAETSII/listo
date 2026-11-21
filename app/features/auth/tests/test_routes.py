"""Tests de las vistas de registro, login y logout, usando el cliente de pruebas de Flask."""

from app.features.auth import services


def test_register_creates_user_and_logs_in(client):
    response = client.post(
        "/auth/register",
        data={
            "name": "Luis",
            "email": "luis@example.com",
            "password": "secreto123",
            "confirm": "secreto123",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Tu cuenta se ha creado" in response.get_data(as_text=True)
    assert services.get_user_by_email("luis@example.com") is not None


def test_register_rejects_duplicate_email(client, user):
    response = client.post(
        "/auth/register",
        data={
            "name": "Otra",
            "email": user.email,
            "password": "secreto123",
            "confirm": "secreto123",
        },
    )

    assert response.status_code == 200
    assert "Ya existe una cuenta" in response.get_data(as_text=True)


def test_register_shows_validation_errors_in_spanish(client):
    response = client.post(
        "/auth/register",
        data={"name": "", "email": "no-es-un-correo", "password": "a1b2c3", "confirm": "x"},
    )
    html = response.get_data(as_text=True)

    assert "Este campo es obligatorio." in html
    assert "Email inválido." in html
    assert "Las contraseñas no coinciden." in html
    assert services.get_user_by_email("no-es-un-correo") is None


def test_login_with_correct_password(client, user):
    response = client.post(
        "/auth/login",
        data={"email": user.email, "password": "secreto123"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert "Hola de nuevo, Ana" in response.get_data(as_text=True)


def test_login_with_wrong_password(client, user):
    response = client.post("/auth/login", data={"email": user.email, "password": "mal"})

    assert response.status_code == 200
    assert "incorrectos" in response.get_data(as_text=True)


def test_login_redirects_to_next_page(client, user):
    response = client.post(
        "/auth/login?next=/tasks/", data={"email": user.email, "password": "secreto123"}
    )

    assert response.status_code == 302
    assert response.headers["Location"] == "/tasks/"


def test_login_ignores_next_pages_outside_the_app(client, user):
    for next_url in ["https://otro-sitio.com", "https:otro-sitio.com", "//otro-sitio.com"]:
        response = client.post(
            f"/auth/login?next={next_url}", data={"email": user.email, "password": "secreto123"}
        )
        client.post("/auth/logout")

        assert response.status_code == 302
        assert response.headers["Location"] == "/tasks/"


def test_logout(logged_client):
    response = logged_client.post("/auth/logout", follow_redirects=True)

    assert "Has cerrado sesión" in response.get_data(as_text=True)
    assert logged_client.get("/tasks/").status_code == 302  # vuelve a pedir login
