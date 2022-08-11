from typing import Dict, Any

from fastapi.testclient import TestClient

from src import crud
from src.core.config import settings
from src.models.room import RoomInfo
from src.schemas.room import RoomCreate, RoomUpdate
from src.tests.utils.utils import random_room_name, random_room_type


def create_test_room(db: Any) -> RoomInfo:
    test_room = crud.room.get_by_uuid(db, username=settings.TEST_USER)
    if test_room is None:
        room_create = RoomCreate(
            room_name=settings.TEST_ROOM_NAME,
            room_type=settings.TEST_ROOM_TYPE,
            uuid=settings.TEST_USER_EMAIL,
        )
        test_room = crud.room.create(db=db, obj_in=room_create)

    return test_room

def create_random_room(db: Any) -> RoomInfo:
    room_name = random_room_name()
    room_type = random_room_type()
    room_create = RoomCreate(
        room_name=room_name,
        room_type=room_type
    )
    new_room = crud.room.create(db=db, obj_in=room_create)
    return new_room