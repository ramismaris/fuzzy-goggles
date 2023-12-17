from conftest import client


def test_register() -> None:
    response = client.post('/api/auth/', json={'username': 'test_user', 'password': 'password'})

    assert response.status_code == 200
    body = response.json()
    assert body['id'] == 1
    assert body['username'] == 'test_user'


def test_login() -> None:
    response = client.post(
        "/api/auth/login",
        data={"username": "test_user", "grant_type": "password", "password": "password"},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    assert response.status_code == 200
    body = response.json()
    assert body['token_type'] == 'bearer'

    response = client.get('/api/auth/', headers={'Authorization': f'Bearer {body["access_token"]}'})

    assert response.status_code == 200
    assert response.json()['username'] == 'test_user'


def test_info_about_user() -> None:
    user_data = {"username": "testuser", "password": "testpassword"}
    client.post("/api/auth/", json=user_data)
    login_response = client.post("/api/auth/login", data=user_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/auth/", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]
