from typing import Optional, Any, Dict, List
from datetime import datetime
from uuid import uuid4

from src.core.security import get_password_hash, verify_password
from src.crud.base import CRUDBase
from src.models import RoomInfo, EventInfo
from src.schemas.room import RoomCreate, RoomUpdate

from boto3.dynamodb.conditions import Key


class CRUDRoomInfo(CRUDBase[RoomCreate, RoomUpdate]):

    default_settings = {"placeholder": "placeholder_setting"}
    def get_by_uuid(self, db: Any, uuid: str) -> Optional[RoomInfo]:
        response = db.get_item(Key={"PK": f"ROOM#{uuid}", "SK": "INFO"})
        if "Item" not in response:
            return None
        else:
            return RoomInfo(response["Item"])

    def get_events_by_user(self, db: Any, room_uuid: str, username: str) -> List[EventInfo]:
        room_PK = f"ROOM#{room_uuid}"
        return db.query(EventInfo).filter(EventInfo.PK == room_PK and EventInfo.event_creator == username)

    def get_event_by_uuid(self, db: Any, room_uuid: str, event_uuid: str) -> Optional[EventInfo]:
        room_PK = f"ROOM#{room_uuid}"
        room_item_list = db.query(KeyConditionExpression=Key("PK").eq(room_PK))['Items']

        for room_entry in room_item_list:
            if room_entry['uuid'] == event_uuid:
                return room_entry
        
        return None

    def create(self, db: Any, obj_in: RoomCreate) -> RoomInfo:
        model = RoomInfo()

        new_uuid = obj_in.UUID
        if new_uuid is None:
            new_uuid = uuid4()
            while self.get_by_uuid(db, str(new_uuid)) is not None:
                new_uuid = uuid4()

        model.uuid = str(new_uuid)
        model.PK = f"ROOM#{model.uuid}"
        model.SK = "INFO"
        model.room_name = obj_in.room_name
        model.created_at = datetime.now().isoformat()
        model.room_type = obj_in.room_type

        if obj_in.settings is None:
            model.settings = self.default_settings
        else:
            model.settings = obj_in.settings

        db.put_item(Item=model.to_dict())
        return model

    def create_event(self, db: Any, room_uuid: str, creator: str) -> Optional[EventInfo]:
        event = EventInfo()
        
        room_to_update = self.get_by_uuid(db, room_uuid)
        if room_to_update == None:
            return None

        event.uuid = str(uuid4())
        event.PK = f"ROOM#{room_uuid}"
        event.SK = f"EVENT#{datetime.now().isoformat()}#EVENT#{event.uuid}#TYPE#TEST"
        event.event_creator = creator
        event.viewed_by = [creator]

        db.put_item(Item=event.to_dict())
        return event

    def update(
        self, db: Any, db_obj: RoomInfo, obj_in: RoomUpdate | Dict[str, Any]
    ) -> RoomInfo:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

room = CRUDRoomInfo()
