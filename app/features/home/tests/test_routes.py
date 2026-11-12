def test_index_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Listo" in response.get_data(as_text=True)
    assert "proyecto base de la asignatura" in response.get_data(as_text=True)


def test_index_shows_login_links_to_anonymous_users(client):
    html = client.get("/").get_data(as_text=True)

    assert "Crear cuenta" in html
    assert "Mis tareas" not in html


def test_index_shows_tasks_link_to_logged_users(logged_client):
    html = logged_client.get("/").get_data(as_text=True)

    assert "Mis tareas" in html


def test_about_page(client):
    response = client.get("/about")

    assert response.status_code == 200
    assert "Acerca de Listo" in response.get_data(as_text=True)


def test_hello_in_the_path(client):
    assert client.get("/hello/Marta").get_data(as_text=True) == "Hola, Marta"


def test_hello_in_the_query_string(client):
    assert client.get("/hello?name=Marta").get_data(as_text=True) == "Hola, Marta"
    assert client.get("/hello").get_data(as_text=True) == "Hola, desconocido"


def test_hello_escapes_html(client):
    html = client.get("/hello?name=<b>Marta</b>").get_data(as_text=True)

    assert "<b>" not in html
    assert "&lt;b&gt;" in html


def test_method_not_allowed(client):
    response = client.post("/about")
    assert response.status_code == 405
    assert "405" in response.get_data(as_text=True)
