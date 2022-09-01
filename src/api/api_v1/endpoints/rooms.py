from typing import Any

from fastapi import APIRouter
from pydantic import UUID4

from src import  crud
from src.db import table as db
from src.models.event import EventInfo
from src.schemas.event import EventCreate

router = APIRouter()


@router.post("/{room_uuid}/{user_name}", response_model=str)
def test_room(
    room_uuid: UUID4,
    user_name: str
) -> EventInfo:
    
    new_event = EventCreate(event_creator=user_name, event_type='TEST')
    test_event = crud.event.create(db, new_event, room_uuid)
    return test_event.UUID