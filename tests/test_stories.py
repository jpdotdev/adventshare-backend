import pytest
from app import schemas

# Users to not have to be authorized/logged in to view stories
def test_get_all_stories(client, test_stories):
    res = client.get('/stories/')
    print(res.json())
    assert len(res.json()) == len(test_stories)
    assert res.status_code == 200

# Find a specific post by id
def test_get_one_story(client, test_stories):
    res = client.get(f'/stories/{test_stories[0].id}')
    assert res.status_code == 200


#404 when story not found
def test_get_one_story_notexist(client):
    res = client.get(f'/stories/5000')
    assert res.status_code == 404


# Create story - users must be logged in 
@pytest.mark.parametrize("character, party, story", [
    ("Ozkaa", "TBC", "Light cleric of Mystra"),
    ("Virgil", "TBC", "Wizard man with sad story"),
    ("Svaelinn", "The Castaways", "Tiefling trying to uncover his past"),
])
def test_create_story(authorized_client, test_user, character, party, story):
    res = authorized_client.post('/stories/', json={"character": character, "party": party, "story": story})
    
    created_story = schemas.StoryResponse(**res.json())
    assert res.status_code == 201
    assert created_story.character == character
    assert created_story.party == party
    assert created_story.story == story
    assert created_story.user_id == test_user['id']


def test_create_story_default_published_true(authorized_client, test_user):
    res = authorized_client.post('/stories/', json={"character": "Test Character", "party": "Test Party", "story": "Test Story"})
    
    created_story = schemas.StoryResponse(**res.json())
    assert res.status_code == 201
    assert created_story.character == "Test Character"
    assert created_story.party == "Test Party"
    assert created_story.story == "Test Story"
    assert created_story.published == True
    assert created_story.user_id == test_user['id']


def test_unauthorized_user_create_story(client):
    res = client.post('/stories/', json={"character": "Test Character", "party": "Test Party", "story": "Test Story"})
    assert res.status_code == 401


# Delete story - users must be logged in 
def test_unauthorized_delete_story(client, test_stories):
    res = client.delete(f'/stories/{test_stories[0].id}')
    assert res.status_code == 401


def test_authorized_delete_story(authorized_client, test_stories):
    res = authorized_client.delete(f'/stories/{test_stories[0].id}')
    assert res.status_code == 204


def test_delete_story_notexist(authorized_client):
    res = authorized_client.delete('/stories/5000')
    assert res.status_code == 404


def test_delete_other_user_story(authorized_client, test_user, test_user2, test_stories):
    res = authorized_client.delete(f'/stories/{test_stories[2].id}')

    assert res.status_code == 403


# Update story - users must be logged in 
def test_update_post(authorized_client, test_user, test_stories):
    data = { "character": "Updated Test Character", 
            "party": "Updated Test Party", 
            "story": " Updated Test Story",
            "id": test_stories[0].id
    }
    res = authorized_client.put(f'/stories/{test_stories[0].id}', json=data)
    updated_story = schemas.StoryResponse(**res.json())
    assert res.status_code == 200
    assert updated_story.character == data['character']
    assert updated_story.party == data['party']
    assert updated_story.story == data['story']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_stories):
    data = { "character": "Updated Test Character", 
            "party": "Updated Test Party", 
            "story": " Updated Test Story",
            "id": test_stories[2].id
    }
    res = authorized_client.put(f'/stories/{test_stories[2].id}', json=data)
    assert res.status_code == 403


def test_unauthorized_update_story(client, test_stories):
    res = client.put(f'/stories/{test_stories[0].id}')
    assert res.status_code == 401


def test_update_story_notexist(authorized_client, test_stories):
    data = { "character": "Updated Test Character", 
            "party": "Updated Test Party", 
            "story": " Updated Test Story",
            "id": test_stories[2].id
    }
    res = authorized_client.put('/stories/5000', json=data)
    assert res.status_code == 404