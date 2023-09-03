def test_ping(client):
    response = client.get("/health/ping")
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "testing": True, "ping": "pong!"}
