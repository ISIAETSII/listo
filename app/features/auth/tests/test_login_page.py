def test_login_page(client):
    resp = client.get("/auth/login")
    assert resp.status_code == 200
    assert "Recordarme" in resp.text
