def test_login_success(client):
    resp = client.post(
        "/api/v1/auth/login", json={"username": "admin", "password": "test-admin-pass"}
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client):
    resp = client.post("/api/v1/auth/login", json={"username": "admin", "password": "wrong"})
    assert resp.status_code == 401


def test_login_wrong_username(client):
    resp = client.post(
        "/api/v1/auth/login", json={"username": "nope", "password": "test-admin-pass"}
    )
    assert resp.status_code == 401
