from .base import BaseDBModel
from pydantic import UUID4

# EVENT#TIME#EVENT#UUID#TYPE#EVENT_TYPE		
		
class EventInfo(BaseDBModel):
    event_creator: str
    viewed_by: list
    screenshot_by: list

    def __init__(self, attrs: dict = None):
        if attrs is not None:
            super().__init__(attrs)

    def created_at(self) -> str:
        tokenized_fields = self.SK.split('#')
        return tokenized_fields[1]

    @property
    def UUID(self) -> str:
        tokenized_fields = self.SK.split('#')
        return tokenized_fields[3]

    @property
    def event_type(self) -> str:
        tokenized_fields = self.SK.split('#')
        return tokenized_fields[5]