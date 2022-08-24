from typing import Any

from fastapi import APIRouter
from pydantic import UUID4

from src import  crud
from src.db import table as db
from src.models.event import EventInfo

router = APIRouter()


@router.post("/{room_uuid}/{user_name}", response_model=str)
def test_room(
    room_uuid: UUID4,
    user_name: str
) -> EventInfo:
    
    test_event = crud.room.create_event(db, room_uuid, user_name)
    return test_event.UUID()