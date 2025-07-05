from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# --- USER ---
class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"


class UserRead(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2


# --- TOKEN ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- ROOM ---
class RoomCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoomRead(RoomCreate):
    id: int

    class Config:
        from_attributes = True


# --- MESSAGE ---
class MessageCreate(BaseModel):
    content: str


class MessageRead(BaseModel):
    id: int
    content: str
    timestamp: datetime
    user_id: int
    room_id: int
    username: str  # Added for sender info

    class Config:
        from_attributes = True


# --- WEB SOCKET ---
class WsMessage(BaseModel):
    content: str
    sender: str
    timestamp: str