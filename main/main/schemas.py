from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import *

#frontend inputs
class Post(BaseModel):
    post: str

class Signup(BaseModel):
    username: str
    studentnr: int
    password: str

class Update(BaseModel):
    post: str   

class Token_data(BaseModel):
    studentnr : Optional[int] = None

#Response structures

class Comment(BaseModel):
    coomment: str
    class Config:
        orm_mode = True

class Return(BaseModel):
    username: str
    post: str
    class Config:
        orm_mode = True

class Return2(Return):
    pass
    pid: int
    comment: Comment
    class Config:
        orm_mode = True


class MyPost(BaseModel):
    pid: int
    post: str
    created_at: datetime
    class Config:
        orm_mode = True
