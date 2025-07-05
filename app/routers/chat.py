from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

router = APIRouter()

@router.post("/rooms", response_model=schemas.RoomRead)
def create_room(room: schemas.RoomCreate, db: Session = Depends(get_db), current_user=Depends(auth.admin_required)):
    new_room = models.Room(name=room.name, description=room.description)
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room
