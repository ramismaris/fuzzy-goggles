from conftest import client


def test_create_client(auth):
    client_data = {'gender': 'female', 'age': 18.0, 'username': 'john_doe'}
    response = client.post(
        '/api/client/',
        headers={'Authorization': f'Bearer {auth.access_token}'},
        json=client_data
    )

    res_body = response.json()

    assert response.status_code == 200
    assert res_body['gender'] == client_data['gender']
    assert res_body['age'] == client_data['age']
    assert res_body['username'] == client_data['username']


def test_get_clients(auth):
    clients_data = [
        {'gender': 'female', 'age': 18.0, 'username': 'moscow'},
        {'gender': 'male', 'age': 56, 'username': 'tokyo'},
    ]
    for data in clients_data:
        client.post('/api/client/', headers={'Authorization': f'Bearer {auth.access_token}'}, json=data)

    response = client.get(
        '/api/client/',
        headers={'Authorization': f'Bearer {auth.access_token}'},
    )

    assert response.status_code == 200


def test_delete_client(auth):
    client_data = {'gender': 'female', 'age': 18.0, 'username': 'john_doe'}
    response = client.post("/api/client/", json=client_data, headers={"Authorization": f"Bearer {auth.access_token}"})
    assert response.status_code == 200
    client_id = response.json()["id"]

    response = client.delete(f"/api/client/{client_id}", headers={"Authorization": f"Bearer {auth.access_token}"})
    assert response.status_code == 204
