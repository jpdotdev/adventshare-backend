from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(prefix='/likes',
                   tags=['Likes'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db), 
         current_user: int = Depends(oauth2.get_current_user)):
    
    story = db.query(models.Story).filter(models.Story.id == like.story_id).first()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Story does not exist")
    
    like_query = db.query(models.Like).filter(models.Like.story_id == like.story_id,
                            models.Like.user_id == current_user.id)
    
    found_like = like_query.first()
    if (like.direction == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already liked this post")
        new_like = models.Like(story_id = like.story_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Succesfully liked this post"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Like does not exist")
        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Succesfully unliked this post"}
    
