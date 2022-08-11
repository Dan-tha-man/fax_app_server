from typing import Optional, Any, Dict
from datetime import datetime
from uuid import uuid4

from src.core.security import get_password_hash, verify_password
from src.crud.base import CRUDBase
from src.models import RoomModel
from src.schemas.room import RoomCreate, RoomUpdate


class CRUDRoomModel(CRUDBase[RoomCreate, RoomUpdate]):

    default_settings = {"placeholder": "placeholder_setting"}
    def get_by_uuid(self, db: Any, *, uuid: str) -> Optional[RoomModel]:
        response = db.get_item(Key={"PK": f"USER#{uuid}", "SK": "MODEL"})
        if "Item" not in response:
            return None
        else:
            return RoomModel(response["Item"])

    def create(self, db: Any, *, obj_in: RoomCreate) -> RoomModel:
        model = RoomModel()

        new_uuid = obj_in.UUID
        if new_uuid is None:
            new_uuid = uuid4()
            while self.get_by_uuid(db, str(new_uuid)) is not None:
                new_uuid = uuid4()

        model.PK = f"ROOM#{str(new_uuid)}"
        model.SK = "MODEL"
        model.name = obj_in.name
        model.created_at = datetime.now().isoformat()
        model.room_type = obj_in.room_type

        if obj_in.settings is None:
            model.settings = self.default_settings
        else:
            model.settings = obj_in.settings

        db.put_item(Item=model.to_dict())
        return model

    def update(
        self, db: Any, *, db_obj: RoomModel, obj_in: RoomUpdate | Dict[str, Any]
    ) -> RoomModel:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

room = CRUDRoomModel()
