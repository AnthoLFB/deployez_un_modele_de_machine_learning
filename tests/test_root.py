# Vérifie que la route racine affiche bien le message de bienvenue et la liste des routes
def test_root(client):

    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "routes" in data
    assert "health" in data["routes"]
    assert "train" in data["routes"]
    assert "predict" in data["routes"]
