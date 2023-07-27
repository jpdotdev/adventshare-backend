import pytest
from app import models

@pytest.fixture
def test_like(test_stories, session, test_user):
    new_like = models.Like(story_id=test_stories[2].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()


def test_like_story(authorized_client, test_stories):
    res = authorized_client.post('/likes/', json={"story_id": test_stories[2].id, "direction": 1})
    assert res.status_code == 201


def test_already_liked_story(authorized_client, test_stories, test_like):
    res = authorized_client.post('/likes/', json={"story_id": test_stories[2].id, "direction": 1})
    assert res.status_code == 409


def test_unlike_story(authorized_client, test_stories, test_like):
    res = authorized_client.post('/likes/', json={"story_id": test_stories[2].id, "direction": 0})
    assert res.status_code == 201


def test_unlike_story_notexist(authorized_client, test_stories):
    res = authorized_client.post('/likes/', json={"story_id": test_stories[2].id, "direction": 0})
    assert res.status_code == 404


def test_like_story_notexist(authorized_client, test_stories):
    res = authorized_client.post('/likes/', json={"story_id": 500, "direction": 1})
    assert res.status_code == 404


def test_like_story_notexist(client, test_stories):
    res = client.post('/likes/', json={"story_id": test_stories[2].id, "direction": 1})
    assert res.status_code == 401