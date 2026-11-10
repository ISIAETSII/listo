def test_register_page(client):
    resp = client.get("/auth/register")
    assert resp.status_code == 200
    assert "Crear" in resp.text
