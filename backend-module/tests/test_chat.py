from conftest import client


def test_request_offer(auth):
    client_data = {'gender': 'female', 'age': 18.0, 'username': 'john_doe'}
    client.post('/api/client/', headers={'Authorization': f'Bearer {auth.access_token}'}, json=client_data)
    question_data = {"product_id": 1, "channel_id": 1, "client_id": 1}
    response = client.post("/api/chat/", json=question_data, headers={"Authorization": f"Bearer {auth.access_token}"})
    assert response.status_code == 200
    assert "text" in response.json()
    assert response.json()["text"] == "Привет, это бот, я отвечу на все твои вопросы :)"


def test_mark_answer(auth):
    # Создаем тестовый вопрос
    question_data = {"product_id": 1, "channel_id": 1, "client_id": 1}
    response = client.post("/api/chat/", json=question_data, headers={"Authorization": f"Bearer {auth.access_token}"})
    assert response.status_code == 200
    question_id = response.json()["id"]

    # Пытаемся пометить ответ для несуществующего вопроса
    answer_patch_data = {"is_marked": True}
    response = client.patch(f"/api/chat/{question_id + 1}", json=answer_patch_data,
                            headers={"Authorization": f"Bearer {auth.access_token}"})
    assert response.status_code == 422

    answer_patch_data = {"is_liked": True}
    # Пытаемся пометить ответ не от текущего пользователя
    response = client.patch(f"/api/chat/{question_id}", json=answer_patch_data,
                            headers={"Authorization": f"Bearer test"})
    assert response.status_code == 401

    # Помечаем ответ текущего пользователя
    response = client.patch(f"/api/chat/{question_id}", json=answer_patch_data,
                            headers={"Authorization": f"Bearer {auth.access_token}"})
    assert response.status_code == 200
