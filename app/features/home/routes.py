from flask import render_template

from app.features.home import home_bp


@home_bp.route("/")
def index():
    return render_template("home/index.html")


@home_bp.route("/about")
def about():
    return "<h1>Acerca de Listo</h1><p>El proyecto base de ISIA.</p>"

def test_about_page(client):
    response = client.get("/about")
    
    assert response.status_code == 200
    assert "Acerca de Listo" in response.get_data(as_text=True)