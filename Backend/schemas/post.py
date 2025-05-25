from pydantic import BaseModel, EmailStr, Field  # EmailStr validates emails
from typing import Optional, List
from datetime import datetime

class CommentCreate(BaseModel):
    text: str

class CommentOut(BaseModel):
    id: str
    author_email: str
    author_name: str
    text: str
    date: datetime

class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: str
    title: str
    content: str
    author: str
    author_email: str
    date: datetime
    comments: List[CommentOut] = []
    likes_count: int = 0
    liked_users: List[str] = []
    views: int = 0 

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None