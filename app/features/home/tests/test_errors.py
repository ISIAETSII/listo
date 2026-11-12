"""Tests de páginas de error."""


def test_method_not_allowed_page(client):
    response = client.get("/auth/logout")
    html = response.get_data(as_text=True)

    assert response.status_code == 405
    assert "405" in html
    assert "Método no permitido." in html
    assert "Volver al inicio" in html
