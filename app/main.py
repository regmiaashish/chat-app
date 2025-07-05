from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# Local imports
from .database import Base, engine, get_db
from .models import Message, User, Room
from .schemas import MessageRead, WsMessage
from .auth import decode_token, get_current_user

app = FastAPI()

# Initialize database
Base.metadata.create_all(bind=engine)

# WebSocket connections tracker
active_connections = {}

# Include routers
from .routers import users, chat

app.include_router(users.router)
app.include_router(chat.router)


@app.get("/")
def home():
    return {"message": "FastAPI Chat is running"}


# WebSocket endpoint with full persistence
@app.websocket("/ws/{room_id}")
async def websocket_chat(
        websocket: WebSocket,
        room_id: int,
        token: str = Query(...),
        db: Session = Depends(get_db)
):
    try:
        # Authenticate using existing JWT system
        payload = decode_token(token)
        user = db.query(User).filter(User.id == payload.get("sub")).first()
        if not user:
            raise HTTPException(status_code=403, detail="Invalid user")

        await websocket.accept()

        # Track connection
        if room_id not in active_connections:
            active_connections[room_id] = {}
        active_connections[room_id][user.id] = websocket

        # Send last 10 messages
        last_messages = db.query(Message).filter(
            Message.room_id == room_id
        ).order_by(
            Message.timestamp.desc()
        ).limit(10).all()

        for msg in reversed(last_messages):
            await websocket.send_json(WsMessage(
                content=msg.content,
                sender=msg.sender.username,
                timestamp=msg.timestamp.isoformat()
            ).dict())

        # Message handling loop
        while True:
            content = await websocket.receive_text()

            # Persist message
            message = Message(
                content=content,
                user_id=user.id,
                room_id=room_id,
                timestamp=datetime.utcnow()
            )
            db.add(message)
            db.commit()

            # Broadcast with sender info
            ws_msg = WsMessage(
                content=content,
                sender=user.username,
                timestamp=message.timestamp.isoformat()
            )
            for conn in active_connections[room_id].values():
                await conn.send_json(ws_msg.dict())

    except (WebSocketDisconnect, HTTPException) as e:
        if isinstance(e, HTTPException):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        if room_id in active_connections and user.id in active_connections[room_id]:
            del active_connections[room_id][user.id]


# Message history endpoint with pagination
@app.get("/rooms/{room_id}/messages", response_model=List[MessageRead])
def get_room_messages(
        room_id: int,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, le=500),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    room = db.query(Room).filter(Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    messages = db.query(Message).join(User).filter(
        Message.room_id == room_id
    ).order_by(
        Message.timestamp.desc()
    ).offset(skip).limit(limit).all()

    return [
        MessageRead(
            id=msg.id,
            content=msg.content,
            timestamp=msg.timestamp,
            user_id=msg.user_id,
            room_id=msg.room_id,
            username=msg.sender.username
        )
        for msg in messages
    ]