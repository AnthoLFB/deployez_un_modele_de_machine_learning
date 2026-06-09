# Vérifie que la route racine redirige vers /docs
def test_root(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"
