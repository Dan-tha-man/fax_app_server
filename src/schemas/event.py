from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import datetime

class EventBase(BaseModel):
    pass

class EventCreate(EventBase):
    UUID: Optional[UUID4] = None
    event_type: str
    created_at: Optional[datetime] = None
    event_creator: str

class EventUpdate(EventBase):
    viewed_by: list
    screenshot_by: list

class EventInDBBase(EventBase):
    PK: Optional[str] = None
    SK: Optional[str] = None

class Event(EventInDBBase):
    UUID: UUID4
    event_type: str
    created_at: datetime
    event_creator: str
    viewed_by: list
    screenshot_by: list