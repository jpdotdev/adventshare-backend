from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_create_user(client):
    res = client.post('/users/', json={"email": "testuser@test.com",
                                       "display_name": "TestUser",
                                       "password": "test123"})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.display_name == "TestUser"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@test.com', 'test123', 403),
    ('test@test.com', 'wrongpassword', 403),
    ('wrongemail@test.com', 'wrongpassword', 403),
    (None, 'test123', 422),
    ('test@test.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={"username": email, "password": password})

    assert res.status_code == status_code


# def test_root(client):
#     res = client.get('/')
#     print(res.json())
#     assert res.json().get('message') == 'Welcome to my FastAPI project.'
#     assert res.status_code == 200