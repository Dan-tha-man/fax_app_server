from .base import BaseDBModel
from pydantic import UUID4

class RoomInfo(BaseDBModel):
    room_name: str
    created_at: str
    is_pinned: bool | None
    last_message_sent: str
    room_type: str
    settings: dict
    vote_kick_attempts: dict | None
    blocked_room: list | None

    def __init__(self, attrs: dict = None):
        if attrs is not None:
            super().__init__(attrs)

    def UUID(self) -> str:
        return self.PK[5:]