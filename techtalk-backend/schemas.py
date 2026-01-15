# Pydantic schemas for request/response validation
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    security_question: Optional[str] = "What is your favorite programming language?"
    security_answer: Optional[str] = ""

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    bio: Optional[str] = None
    profile_pic: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    bio: str
    profile_pic: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    content: str
    image_url: Optional[str] = ""
    tags: Optional[str] = ""  # Comma-separated tags

class PostUpdate(BaseModel):
    content: str
    image_url: Optional[str] = None

class PostResponse(BaseModel):
    id: int
    user_id: int
    content: str
    image_url: str
    timestamp: datetime
    author: UserResponse
    likes_count: int = 0
    comments_count: int = 0
    reposts_count: int = 0
    is_liked: bool = False
    is_reposted: bool = False
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    timestamp: datetime
    author: UserResponse
    
    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    message: str
    read: bool
    timestamp: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Message schemas
class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    read: bool
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    user: UserResponse
    last_message: str
    last_message_time: datetime
    unread_count: int
