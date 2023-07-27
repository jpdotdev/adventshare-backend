from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models

# Create test DB
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DB_USERNAME}:%s@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}_test' % quote_plus(settings.DB_PASSWORD)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@test.com", "display_name": "Test", "password": "test123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    print(new_user)
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@test.com", "display_name": "Test 2", "password": "test123"}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    print(new_user)
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})



@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_stories(test_user, session, test_user2):
    stories_data = [{"character": "Test Character",
                     "party": "Test Party",
                     "story": "Test Story",
                     "user_id": test_user['id']
                     }, 
                     { "character": "Test Character 2",
                     "party": "Test Party 2",
                     "story": "Test Story 2",
                     "user_id": test_user['id']
                     },
                     {"character": "Test Character 3",
                     "party": "Test Party 3",
                     "story": "Test Story 3",
                     "user_id": test_user2['id']
                     }]
    
    def create_story_model(story):
        return models.Story(**story)

    story_map = map(create_story_model, stories_data)
    stories = list(story_map)
    
    session.add_all(stories)

    session.commit()
    stories = session.query(models.Story).all()
    return stories


