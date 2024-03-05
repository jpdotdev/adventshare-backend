from .. import models, schemas, oauth2
from fastapi import status, HTTPException, Depends, APIRouter, Response
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from sqlalchemy import func

router = APIRouter(prefix='/stories',
                   tags=['Stories'])


@router.get('/', response_model=List[schemas.StoryLikes])
def get_stories(db: Session = Depends(get_db),
                limit: Optional[int] = None, skip: int = 0, search: Optional[str] = ""):

    stories = db.query(models.Story, func.count(models.Like.story_id).label('likes')).join(
                models.Like, models.Like.story_id == models.Story.id, isouter=True).group_by(models.Story.id).filter(models.Story.character.contains(search)).limit(limit).offset(skip).all()

    return stories

# def get_posts():
#     cursor.execute(""" SELECT * FROM posts """)
#     posts = cursor.fetchall()
#     return {'data': posts}
    

@router.get('/{id}', response_model=schemas.StoryLikes)
def get_story(id: int, db: Session = Depends(get_db)):
    story = db.query(models.Story, func.count(models.Like.story_id).label('likes')).join(
                models.Like, models.Like.story_id == models.Story.id, isouter=True).group_by(models.Story.id).filter(models.Story.id == id).first()

    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"Story with id: {id} was not found")
    return story

# cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
# post = cursor.fetchone()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.StoryResponse)
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):

    new_story = models.Story(user_id=current_user.id, **story.dict()) #unpack the post incase we add more fields to model
    db.add(new_story)
    db.commit()
    db.refresh(new_story)
    return new_story

# cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
#                (post.title, post.content, post.published))
# new_post = cursor.fetchone()
# connect.commit()



@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_story(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Story).filter(models.Story.id == id)

    deleted_story = post_query.first()

    if deleted_story == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"There is no story with id: {id} to delete")
    
    if deleted_story.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
# deleted_post = cursor.fetchone()
# connect.commit()


@router.put('/{id}', response_model=schemas.StoryResponse)
def update_story(id: int, story: schemas.StoryCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    story_query = db.query(models.Story).filter(models.Story.id == id)
    updated_story = story_query.first()

    if updated_story == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Story with id: {id} does not exist")
    
    if updated_story.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    
    story_query.update(story.dict(), synchronize_session=False)
    db.commit()
    
    return story_query.first()

# cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
#                (post.title, post.content, post.published, str(id)))
# updated_post = cursor.fetchone()
# connect.commit()


