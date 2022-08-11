from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

class RoomBase(BaseModel):
    pass

class RoomCreate(RoomBase):
    UUID: Optional[UUID4] = None
    name: str
    room_type: str
    settings: Optional[dict] = None

class RoomUpdate(RoomBase):
    name: Optional[str] = None
    is_pinned: Optional[bool] = None
    last_message_sent: Optional[datetime] = None
    settings: Optional[dict] = None
    vote_kick_attempts: Optional[dict] = None
    blocked_room: Optional[list] = None

class RoomInDBBase(RoomBase):
    PK: Optional[str] = None
    SK: Optional[str] = None

class Room(RoomInDBBase):
    name: str
    created_at: datetime
    room_type: str
    settings: dict
    is_pinned: bool
    last_message_sent: Optional[datetime] = None
    vote_kick_attempts: Optional[dict] = None
    blocked_room: Optional[list] = None