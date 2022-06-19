from pydantic import BaseModel, EmailStr
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(Post):
    pass

class UpdatePost(Post):
    pass

class PostResponse(Post):
    id: int
    created_at = datetime

    class Config:
        orm_mode = True



class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
