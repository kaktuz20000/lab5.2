from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'Sergey Sergeev',
        'email': 's.sergeev@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == new_user['name']
    assert data['email'] == new_user['email']
    assert 'id' in data

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_email_user = {
        'name': 'Duplicate User',
        'email': users[0]['email']
    }
    response = client.post("/api/v1/user", json=existing_email_user)
    assert response.status_code == 400
    assert response.json() == {'detail': 'User with this email already exists'}

def test_delete_user():
    '''Удаление пользователя'''
    user_to_delete = {
        'name': 'To Delete',
        'email': 'delete.me@mail.com'
    }
    create_response = client.post("/api/v1/user", json=user_to_delete)
    user_id = create_response.json()['id']

    delete_response = client.delete(f"/api/v1/user/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {'detail': 'User deleted'}

    get_response = client.get("/api/v1/user", params={'email': user_to_delete['email']})
    assert get_response.status_code == 404
