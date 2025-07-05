# These are the "schemas" for request and response data

from pydantic import BaseModel
from datetime import datetime

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
        orm_mode = True

# --- TOKEN ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- ROOM ---
class RoomCreate(BaseModel):
    name: str
    description: str | None = None

class RoomRead(RoomCreate):
    id: int
    class Config:
        orm_mode = True

# --- MESSAGE ---
class MessageCreate(BaseModel):
    content: str

class MessageRead(BaseModel):
    id: int
    content: str
    timestamp: datetime
    user_id: int
    room_id: int
    class Config:
        orm_mode = True
