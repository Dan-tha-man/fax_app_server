from typing import Optional, Any, Dict, List
from datetime import datetime
from uuid import uuid4

from src.crud.base import CRUDBase
from src.models import RoomInfo, EventInfo
from src.schemas.event import EventCreate, EventUpdate

from boto3.dynamodb.conditions import Key


class CRUDEventInfo(CRUDBase[EventCreate, EventUpdate]):

    def get_events_by_user(self, db: Any, room_uuid: str, username: str) -> List[EventInfo]:
        room_PK = f"ROOM#{room_uuid}"
        events_list = db.query(EventInfo).filter(EventInfo.PK == room_PK and EventInfo.event_creator == username)
        return [EventInfo(e) for e in events_list]

    def get_by_uuid(self, db: Any, room_uuid: str, event_uuid: str) -> Optional[EventInfo]:
        room_PK = f"ROOM#{room_uuid}"
        room_item_list = db.query(KeyConditionExpression=Key("PK").eq(room_PK))['Items']

        for room_entry in room_item_list:
            if 'event_creator' in room_entry:
                this_event = EventInfo(room_entry)
                if this_event.UUID == event_uuid:
                    return this_event
        
        return None

    def create(self, db: Any, obj_in: EventCreate, room_uuid: str) -> EventInfo:
        event = EventInfo()

        event.uuid = str(uuid4())
        event.PK = f"ROOM#{room_uuid}"
        event.SK = f"EVENT#{datetime.now().isoformat()}#EVENT#{event.uuid}#TYPE#{obj_in.event_type}"
        event.event_creator = obj_in.event_creator
        event.viewed_by = [obj_in.event_creator]

        db.put_item(Item=event.to_dict())
        return event


    def update(
        self, db: Any, db_obj: EventInfo, obj_in: EventUpdate | Dict[str, Any]
    ) -> EventInfo:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return EventInfo(super().update(db, db_obj=db_obj, obj_in=update_data))

event = CRUDEventInfo()
