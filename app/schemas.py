from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint
from typing import Optional


# User model and User response model
class UserCreate(BaseModel):
    email: EmailStr
    display_name: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    display_name: str
    created_at: datetime

    class Config:
        orm_mode = True


#User login     
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Post model / Post response model
class StoryBase(BaseModel):
    character: str
    party: str
    story: str  
    published: bool = True


class StoryCreate(StoryBase):
    pass 


class StoryResponse(StoryBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
        orm_mode = True


class StoryLikes(BaseModel):
    Story: StoryResponse 
    likes: int

    class Config:
        orm_mode = True


# Token verification
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Like(BaseModel):
    story_id: int
    direction: conint(le=1, ge=0)
    

# Token
# username: EmailStr
# password: str